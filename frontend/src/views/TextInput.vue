<template>
    <div id='text_file_select' class="ti">
        <label for="textArea" class="ti-label">{{ $t('message.text') }}</label>
        <textarea id="textArea" class="glass-field ti-textarea" v-model="text"
            :placeholder="$t('message.enterText')"></textarea>

        <label for="textFileInput" class="ti-label">{{ $t('message.orUploadDocument') }}</label>
        <div class="file_select_container">
            <button @click="triggerTextFileInput" class="btn-glass btn-upload">{{ $t('message.chooseFile') }}</button>
            <span class="file-name" v-if="selectedTextFileName">{{ selectedTextFileName }}</span>
            <input type="file" ref="textFileInput" @change="uploadFile" id="textFileInput"
                accept=".doc,.docx,.pdf,.txt,.rtf" hidden />
        </div>

        <div v-if="isLoading" class="inline-loader"><span class="spin"></span>{{ $t('message.loading') }}…</div>
    </div>
</template>


<script>
export default {
    name: 'TextInput',

    data() {
        return {
            text: '',
            isLoading: false,
            selectedTextFileName: '',
        }
    },
    //當輸入框的值發生變化時，通知HomeView更新text_handwriting 7.4
    watch: {
        text: function (val) {
            this.$emit('childEvent', val);
        }
    },
    created() {
        const localStorageItems = ['selectedTextFileName','text']
        localStorageItems.forEach(item => {
            const value = localStorage.getItem(item);
            if (value !== null && value !== "undefined") {
                this[item] = JSON.parse(value);
            } else {
                console.log('localstorage缺失item:' + item)
            }
        });
    },
    methods: {
        uploadFile(e) {
            let file = e.target.files[0];
            // 當用戶選擇了一個新的文本檔案時，更新 selectedTextFileName
            this.selectedTextFileName = e.target.files[0].name;
            // localStorage.setItem('textFile', JSON.stringify(this.textFile));
            localStorage.setItem('selectedTextFileName', JSON.stringify(this.selectedTextFileName));

            let formData = new FormData();

            formData.append('file', file);  // 'file' 是你在伺服器端獲取檔案資料時的 key
            this.isLoading = true;
            this.$http.post(
                '/api/textfileprocess',
                formData, {

                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
                .then(response => {
                    this.text = response.data.text;
                    //通知HomeView更新text 7.3, 但是如果直接輸入文字，這裡不會通知父元件7.4
                    this.$emit('childEvent', this.text);
                    // 使用與 HomeView 一致的鍵名儲存
                    localStorage.setItem('text', JSON.stringify(this.text));
                    this.isLoading = false;
                })
                .catch(error => {
                    console.error(error);
                    this.isLoading = false;
                });
        },
        triggerTextFileInput() {
            this.$refs.textFileInput.click();
        },
    },

}
</script>

<style scoped>
.ti {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.ti-label {
    font-size: 0.86rem;
    font-weight: 600;
    color: var(--ink-soft);
    margin: 0;
}

.ti-textarea {
    width: 100%;
    min-height: 160px;
    resize: vertical;
    line-height: 1.6;
    font-size: 0.98rem;
}

.file_select_container {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.btn-upload {
    font-size: 0.88rem;
    padding: 0.55em 1em;
}

.file-name {
    font-size: 0.82rem;
    color: var(--ink-faint);
    word-break: break-all;
}
</style>
