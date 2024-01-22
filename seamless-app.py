
import scipy
from transformers import AutoProcessor, SeamlessM4Tv2Model

from fastapi import FastAPI
from pydantic import BaseModel


class Text2SpeechReq(BaseModel):
    text: str
    srcLang: str
    tgtLang: str


app = FastAPI()
processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
model = SeamlessM4Tv2Model.from_pretrained("/media/hdd/modelhub/seamless-m4t-v2-large").to('cuda')


@app.post("/api/text2speech")
async def create_item(req: Text2SpeechReq):
    sample_rate = model.config.sampling_rate
    text_inputs = processor(text=req.text, src_lang=req.srcLang, return_tensors="pt").to('cuda')
    audio_array_from_text = model.generate(**text_inputs, tgt_lang=req.tgtLang)[0].cpu().numpy().squeeze()
    # print(audio_array_from_text)
    scipy.io.wavfile.write("outputs-speech.wav", rate=sample_rate, data=audio_array_from_text)
    return {'code': 200, 'message': 'ok'}