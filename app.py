# -*- coding: utf-8 -*-
"""
OS 手寫小抄產生器 — GUI
把文字檔用指定字體轉成「手寫」PDF。所有參數都可在視窗中調整。
依賴：pillow numpy handright fonttools   (build_exe.bat 會自動處理)
"""
import os, sys, threading, traceback
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import render_core as rc


def app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


# (key, 中文標籤) — 順序即顯示順序
FIELDS = [
    ("font_size",           "字體大小"),
    ("line_spacing",        "行間距"),
    ("top_margin",          "上邊距"),
    ("bottom_margin",       "下邊距"),
    ("left_margin",         "左邊距"),
    ("right_margin",        "右邊距"),
    ("line_spacing_sigma",  "行間距擾動"),
    ("font_size_sigma",     "字體大小擾動"),
    ("word_spacing_sigma",  "字間距擾動"),
    ("perturb_x_sigma",     "筆畫橫向偏移"),
    ("perturb_y_sigma",     "筆畫縱向偏移"),
    ("perturb_theta_sigma", "筆畫旋轉偏移"),
    ("word_spacing",        "字間距"),
    ("strike_len_sigma",    "塗改線長度標準差"),
    ("strike_angle_sigma",  "塗改線角度標準差"),
    ("strike_width_sigma",  "塗改線寬度標準差"),
    ("strike_prob",         "塗改出現的幾率"),
    ("strike_width",        "塗改線寬度"),
    ("ink_depth_sigma",     "墨汁深度標準差"),
    ("dpi",                 "解析度 DPI"),
    ("seed",                "亂數種子"),
]
INT_KEYS = {"font_size", "line_spacing", "top_margin", "bottom_margin", "left_margin",
            "right_margin", "word_spacing", "strike_width", "dpi", "seed"}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OS 手寫小抄產生器")
        self.geometry("560x760")
        self.minsize(540, 680)
        d = app_dir()
        self.var_font = tk.StringVar(value=os.path.join(d, "TekitouPoem.ttf"))
        self.var_text = tk.StringVar(value=os.path.join(d, "OS_Cheat_Sheet_handwriting_source.txt"))
        self.var_out  = tk.StringVar(value=os.path.join(d, "OS_Cheat_Sheet_Handwritten.pdf"))
        self.var_paper = tk.StringVar(value="blank")
        self.var_ink   = tk.StringVar(value="black")
        self.vars = {}
        self._build()

    def _build(self):
        pad = dict(padx=6, pady=3)
        top = ttk.Frame(self); top.pack(fill="x", **pad)
        ttk.Label(top, text="OS 手寫小抄產生器", font=("Microsoft JhengHei", 15, "bold")).pack(anchor="w")
        ttk.Label(top, text="選字體與文字檔 → 調參數 → 生成手寫 PDF", foreground="#555").pack(anchor="w")

        # file pickers
        fp = ttk.LabelFrame(self, text="檔案")
        fp.pack(fill="x", **pad)
        self._file_row(fp, "字體 (.ttf)", self.var_font, 0, [("字體", "*.ttf *.otf")])
        self._file_row(fp, "文字檔 (.txt)", self.var_text, 1, [("文字檔", "*.txt")])
        self._file_row(fp, "輸出 PDF", self.var_out, 2, None, save=True)

        # style row
        sr = ttk.LabelFrame(self, text="紙張 / 墨色")
        sr.pack(fill="x", **pad)
        ttk.Label(sr, text="紙張").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        ttk.Combobox(sr, textvariable=self.var_paper, width=10, state="readonly",
                     values=["blank", "lined", "grid"]).grid(row=0, column=1, padx=6)
        ttk.Label(sr, text="(blank=空白 / lined=橫線 / grid=方格)").grid(row=0, column=2, sticky="w")
        ttk.Label(sr, text="墨色").grid(row=1, column=0, sticky="w", padx=6, pady=4)
        ttk.Combobox(sr, textvariable=self.var_ink, width=10, state="readonly",
                     values=["black", "blue", "dark-gray"]).grid(row=1, column=1, padx=6)
        ttk.Label(sr, text="(black=黑 / blue=藍筆 / dark-gray=深灰)").grid(row=1, column=2, sticky="w")

        # parameter grid (scrollable)
        pf = ttk.LabelFrame(self, text="參數")
        pf.pack(fill="both", expand=True, **pad)
        canvas = tk.Canvas(pf, highlightthickness=0)
        sb = ttk.Scrollbar(pf, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        defaults = rc.default_params()
        for i, (key, label) in enumerate(FIELDS):
            r, c = divmod(i, 2)
            cell = ttk.Frame(inner); cell.grid(row=r, column=c, sticky="w", padx=6, pady=2)
            ttk.Label(cell, text=label, width=14, anchor="w").pack(side="left")
            v = tk.StringVar(value=str(defaults[key]))
            ttk.Entry(cell, textvariable=v, width=8).pack(side="left")
            self.vars[key] = v

        # action
        af = ttk.Frame(self); af.pack(fill="x", **pad)
        self.status = ttk.Label(af, text="就緒", foreground="#0a6")
        self.status.pack(side="left")
        self.btn = ttk.Button(af, text="生成 PDF", command=self._run)
        self.btn.pack(side="right")

    def _file_row(self, parent, label, var, row, types, save=False):
        ttk.Label(parent, text=label, width=12, anchor="w").grid(row=row, column=0, sticky="w", padx=6, pady=4)
        ttk.Entry(parent, textvariable=var, width=44).grid(row=row, column=1, padx=4)
        def browse():
            if save:
                f = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF", "*.pdf")], initialfile=os.path.basename(var.get()))
            else:
                f = filedialog.askopenfilename(filetypes=types or [("All", "*.*")])
            if f:
                var.set(f)
        ttk.Button(parent, text="瀏覽", command=browse).grid(row=row, column=2, padx=4)

    def _collect(self):
        p = {}
        for key, _ in FIELDS:
            s = self.vars[key].get().strip()
            p[key] = int(float(s)) if key in INT_KEYS else float(s)
        p["paper"] = self.var_paper.get()
        p["ink"] = self.var_ink.get()
        return p

    def _set_status(self, msg, color="#0a6"):
        self.status.config(text=msg, foreground=color)
        self.update_idletasks()

    def _run(self):
        try:
            params = self._collect()
        except ValueError:
            messagebox.showerror("參數錯誤", "請確認所有參數都是數字。")
            return
        font, text, out = self.var_font.get(), self.var_text.get(), self.var_out.get()
        for path, name in [(font, "字體檔"), (text, "文字檔")]:
            if not os.path.isfile(path):
                messagebox.showerror("找不到檔案", f"{name} 不存在：\n{path}")
                return
        self.btn.config(state="disabled")

        def work():
            try:
                res = rc.render(text, font, out, params=params,
                                progress=lambda m: self.after(0, self._set_status, m))
                msg = f"完成！{res['pages']} 頁，涂改 {res['strikes']} 處"
                self.after(0, self._set_status, msg)
                self.after(0, lambda: messagebox.showinfo("完成", msg + f"\n\n{out}"))
                try:
                    if sys.platform.startswith("win"):
                        os.startfile(os.path.dirname(out))
                except Exception:
                    pass
            except Exception as e:
                tb = traceback.format_exc()
                self.after(0, self._set_status, "發生錯誤", "#c00")
                self.after(0, lambda: messagebox.showerror("錯誤", f"{e}\n\n{tb}"))
            finally:
                self.after(0, lambda: self.btn.config(state="normal"))

        threading.Thread(target=work, daemon=True).start()


if __name__ == "__main__":
    App().mainloop()
