# -*- coding: utf-8 -*-
"""
render_core.py — handwriting renderer (shared by GUI and CLI).
Turns a UTF-8 text file into a multi-page handwritten PDF using a TTF font,
honouring all 19 tunable parameters plus paper style and ink colour.

Pure file-download friendly: depends only on pillow, numpy, handright, fonttools.
"""
import os, sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from handright import Template, handwrite

try:
    from fontTools.ttLib import TTFont
    _HAVE_FT = True
except Exception:
    _HAVE_FT = False

# Traditional -> Japanese-variant fallbacks (only applied when the TC glyph is
# missing from the font but the JP variant exists — keeps the same word, no tofu).
TC2JP = {'查':'査','產':'産','說':'説','轉':'転','處':'処','對':'対','稱':'称',
         '條':'条','體':'体','區':'区','餘':'余','應':'応','經':'経','濟':'済',
         '號':'号','釋':'釈','續':'続','繼':'継','擴':'拡','顯':'顕','總':'総'}

INK_COLORS = {
    "black":     (18, 18, 22),
    "blue":      (28, 46, 130),     # blue ballpoint
    "dark-gray": (52, 52, 58),
}
PAPERS = ("blank", "lined", "grid")

# A4 canvas sizes by DPI (px)
def a4_size(dpi):
    return (round(210 / 25.4 * dpi), round(297 / 25.4 * dpi))


def default_params():
    return dict(
        font_size=73, line_spacing=74,
        top_margin=42, bottom_margin=43, left_margin=50, right_margin=50,
        line_spacing_sigma=3, font_size_sigma=3, word_spacing_sigma=3,
        perturb_x_sigma=4, perturb_y_sigma=4, perturb_theta_sigma=0.05,
        word_spacing=1,
        strike_len_sigma=2, strike_angle_sigma=2, strike_width_sigma=1,
        strike_prob=0.005, strike_width=6, ink_depth_sigma=28,
        dpi=200, ink="black", paper="blank", seed=20260605,
    )


def _prepare_text(text, font_path):
    if not _HAVE_FT:
        return text, {}, []
    cmap = TTFont(font_path).getBestCmap()
    swapped = {}
    for tc, jp in TC2JP.items():
        if ord(tc) not in cmap and ord(jp) in cmap and tc in text:
            text = text.replace(tc, jp); swapped[tc] = jp
    missing = sorted({c for c in set(text) if c != "\n" and ord(c) not in cmap})
    return text, swapped, missing


def _paper_bg(paper, W, H, p):
    """Return an RGB paper background (lines drawn in light colour)."""
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    step = max(20, int(p["line_spacing"]))
    if paper == "lined":
        y = p["top_margin"] + step
        while y < H - p["bottom_margin"]:
            d.line([(p["left_margin"], y), (W - p["right_margin"], y)],
                   fill=(200, 214, 232), width=2)
            y += step
    elif paper == "grid":
        for y in range(p["top_margin"], H - p["bottom_margin"], step):
            d.line([(p["left_margin"], y), (W - p["right_margin"], y)], fill=(214, 224, 236), width=1)
        for x in range(p["left_margin"], W - p["right_margin"], step):
            d.line([(x, p["top_margin"]), (x, H - p["bottom_margin"])], fill=(214, 224, 236), width=1)
    return img


def _vary_ink(gray, W, H, sigma, rng):
    """Lighten strokes with a smooth low-frequency field (墨汁深度标准差)."""
    a = np.asarray(gray, dtype=np.float32)
    ink = (255.0 - a) / 255.0
    small = rng.standard_normal((max(2, H // 36), max(2, W // 36))).astype(np.float32)
    field = np.asarray(Image.fromarray(small).resize((W, H), Image.BILINEAR))
    lift = np.clip(np.abs(field) * sigma, 0, 95)
    return np.clip(a + lift * ink, 0, 255).astype(np.uint8)


def _add_strikes(gray, p, rng):
    """Occasional hand cross-outs (涂改). Operates on a uint8 gray array."""
    a = gray < 128
    img = Image.fromarray(gray, "L")
    draw = ImageDraw.Draw(img)
    n = 0
    rows = np.where(a.any(axis=1))[0]
    if rows.size == 0:
        return np.asarray(img), 0
    bands, start, prev = [], rows[0], rows[0]
    for r in rows[1:]:
        if r - prev > p["font_size"] * 0.45:
            bands.append((start, prev)); start = r
        prev = r
    bands.append((start, prev))
    fs = p["font_size"]
    for y0, y1 in bands:
        cols = np.where(a[y0:y1 + 1].any(axis=0))[0]
        if cols.size == 0:
            continue
        x, xend, yc = cols.min(), cols.max(), (y0 + y1) / 2.0
        while x < xend:
            if rng.random() < p["strike_prob"]:
                L = max(10, fs + rng.gauss(0, p["strike_len_sigma"]))
                w = max(1, int(round(p["strike_width"] + rng.gauss(0, p["strike_width_sigma"]))))
                ang = math.radians(rng.gauss(0, p["strike_angle_sigma"]))
                dy = (L) * math.tan(ang)
                draw.line([(x, yc - dy / 2), (x + L, yc + dy / 2)], fill=25, width=w)
                n += 1
            x += fs
    return np.asarray(img), n


def render(text_path, font_path, out_pdf, params=None, page_dir=None, progress=None):
    """Render handwriting. Returns dict(pages, strikes, swapped, missing, pngs)."""
    p = default_params()
    if params:
        p.update({k: v for k, v in params.items() if v is not None})
    if page_dir is None:
        page_dir = os.path.dirname(os.path.abspath(out_pdf)) or "."
    os.makedirs(page_dir, exist_ok=True)

    def say(msg):
        if progress:
            progress(msg)

    rng = random.Random(p["seed"])
    nprng = np.random.default_rng(p["seed"])

    text = open(text_path, encoding="utf-8").read()
    text, swapped, missing = _prepare_text(text, font_path)
    say(f"字体相容性檢查：替換 {len(swapped)} 字、缺字 {len(missing)}")

    W, H = a4_size(p["dpi"])
    template = Template(
        background=Image.new("L", (W, H), 255),
        font=ImageFont.truetype(font_path, int(p["font_size"])),
        line_spacing=int(p["line_spacing"]),
        fill=0,
        left_margin=int(p["left_margin"]), top_margin=int(p["top_margin"]),
        right_margin=int(p["right_margin"]), bottom_margin=int(p["bottom_margin"]),
        word_spacing=int(p["word_spacing"]),
        line_spacing_sigma=float(p["line_spacing_sigma"]),
        font_size_sigma=float(p["font_size_sigma"]),
        word_spacing_sigma=float(p["word_spacing_sigma"]),
        perturb_x_sigma=float(p["perturb_x_sigma"]),
        perturb_y_sigma=float(p["perturb_y_sigma"]),
        perturb_theta_sigma=float(p["perturb_theta_sigma"]),
    )
    say("產生手寫頁面中…")
    try:
        raw_pages = list(handwrite(text, template, seed=p["seed"]))
    except TypeError:
        raw_pages = list(handwrite(text, template))

    ink = INK_COLORS.get(str(p["ink"]).lower(), INK_COLORS["black"])
    final, pngs, total_strikes = [], [], 0
    for i, pg in enumerate(raw_pages, 1):
        say(f"後製第 {i}/{len(raw_pages)} 頁（墨汁深度 / 涂改 / 上色）")
        gray = _vary_ink(pg, W, H, float(p["ink_depth_sigma"]), nprng)
        gray, ns = _add_strikes(gray, p, rng)
        total_strikes += ns
        # composite coloured ink over chosen paper
        bg = np.asarray(_paper_bg(p["paper"], W, H, p), dtype=np.float32)
        amt = ((255.0 - gray) / 255.0)[:, :, None]
        out = (bg * (1 - amt) + np.array(ink, dtype=np.float32)[None, None, :] * amt)
        page = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")
        png = os.path.join(page_dir, f"handwritten_page_{i:02d}.png")
        page.save(png); pngs.append(png)
        final.append(page)

    say("合併 PDF…")
    final[0].save(out_pdf, save_all=True, append_images=final[1:], resolution=float(p["dpi"]))
    say(f"完成：{len(final)} 頁，涂改 {total_strikes} 處 → {out_pdf}")
    return dict(pages=len(final), strikes=total_strikes, swapped=swapped,
               missing=missing, pngs=pngs, pdf=out_pdf)


def _frozen_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    d = _frozen_dir()
    render(os.path.join(d, "OS_Cheat_Sheet_handwriting_source.txt"),
           os.path.join(d, "TekitouPoem.ttf"),
           os.path.join(d, "OS_Cheat_Sheet_Handwritten.pdf"),
           progress=print)
