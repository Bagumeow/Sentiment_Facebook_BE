from tools.tools import *
from fastapi import FastAPI, __version__
from fastapi.responses import HTMLResponse
import os
from router import sentiment,user,fanpage_param
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI(title="Sentiment Analysis API", description="API for sentiment analysis", version="1.0.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def route():
    return {"message": "Welcome to Sentiment Analysis API"}

app.include_router(user.router)
app.include_router(sentiment.router)
app.include_router(fanpage_param.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=4040)
