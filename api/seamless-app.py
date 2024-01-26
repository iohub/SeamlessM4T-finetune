
import scipy
from transformers import AutoProcessor, SeamlessM4Tv2Model
import torch
import torchaudio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from seamless_communication.inference import Translator


class Text2SpeechReq(BaseModel):
    text: str
    srcLang: str
    tgtLang: str


origins = [
    "http://localhost",
    "http://localhost:9528",
    "http://localhost:8000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_version = '1'

if model_version == 'v2':
    processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
    model = SeamlessM4Tv2Model.from_pretrained("/media/hdd/modelhub/seamless-m4t-v2-large").to('cuda')
else:
    finetune_checkpoint = '/home/do/ssd/data/m4t-traindata/checkpoint.pt'

    translator = Translator(model_name_or_card="seamlessM4T_large", 
                            vocoder_name_or_card='vocoder_36langs', 
                            device=torch.device("cuda:0"), dtype=torch.float16)
    translator.load_state_dict(torch.load(finetune_checkpoint), strict=False)

@app.post("/api/v2/text2speech")
async def create_item(req: Text2SpeechReq):
    sample_rate = model.config.sampling_rate
    text_inputs = processor(text=req.text, src_lang=req.srcLang, return_tensors="pt").to('cuda')
    audio_array_from_text = model.generate(**text_inputs, tgt_lang=req.tgtLang)[0].cpu().numpy().squeeze()
    # print(audio_array_from_text)
    scipy.io.wavfile.write("output-speech.wav", rate=sample_rate, data=audio_array_from_text)
    return {'code': 200, 'message': 'ok'}


@app.post("/api/v1/text2speech")
async def create_item(req: Text2SpeechReq):
    text, speech = translator.predict(input=req.text,
                                      task_str='T2ST',
                                      src_lang=req.srcLang,
                                      tgt_lang=req.tgtLang)
    wavdata = speech.audio_wavs[0].cpu().numpy()[0]
    torchaudio.save('output-speech.wav', torch.FloatTensor(wavdata), sample_rate=speech.sample_rate)

    return {'code': 200, 'message': 'ok', 'text': str(text)}