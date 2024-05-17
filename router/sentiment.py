from tools.tools import *
from fastapi import  FastAPI, HTTPException, status, Depends, APIRouter
import torch
from transformers import RobertaForSequenceClassification, AutoTokenizer
from underthesea import word_tokenize,text_normalize

model = RobertaForSequenceClassification.from_pretrained("wonrax/phobert-base-vietnamese-sentiment")
tokenizer = AutoTokenizer.from_pretrained("wonrax/phobert-base-vietnamese-sentiment", use_fast=False)

def word_segment(text):
    return word_tokenize(text_normalize(text), format="text")

class InputSentiment(BaseModel):
    input_text: str

def sentiment_analysis_text(text):
    input_ids = torch.tensor([tokenizer.encode(word_segment(text))])
    with torch.no_grad():
        out = model(input_ids)
        output = out.logits.softmax(dim=-1)
        if output.argmax().item() == 0:
            label = "Negative"
        elif output.argmax().item() == 1:
            label = "Positive"
        else:
            label = "Neutral"
        return label, output

router = APIRouter()

@router.post('/sentiment', status_code=status.HTTP_200_OK)
async def sentiment_analysis(inputs : InputSentiment ,access_token: str = Depends(oauth2_scheme)):
    label,logits = sentiment_analysis_text(inputs.input_text)
    return {
        "sentiment": label,
        "logits":logits.tolist()
    }