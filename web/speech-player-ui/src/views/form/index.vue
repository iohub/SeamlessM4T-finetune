<template>
  <div class="app-container">
    <el-row>
      <el-col :span="12">
        <el-input v-model="inputText" type="textarea" />
        <el-input
              v-model="outputText"
              :disabled="true">
          </el-input>
      </el-col>
    </el-row>
        
    <el-row  class="custom-margin">
      <el-col :span="12">
          <el-button type="primary" @click="onSubmit">翻译</el-button>

      </el-col>
    </el-row>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  data() {
    return {
      inputText: '',
      outputText: ''
    }
  },
  methods: {
    onSubmit() {
      const text = this.inputText
      var self = this
      axios.post('http://127.0.0.1:8000/api/v1/text2speech', 
        {text: text, srcLang: 'eng', tgtLang: 'cmn'})
        .then(resp => { 
          console.log('success', resp)
          self.outputText = resp.data.text
          let audio = new Audio('http://localhost:8000/static/output-speech.wav')
          audio.play()
        })
        .catch(err => console.error(err));
      }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}

.custom-margin {
  margin-top: 4px; /* change this to your desired value */
}
</style>

