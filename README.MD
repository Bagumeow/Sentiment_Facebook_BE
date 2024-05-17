# Manange Fanpage and Sentiment Analysis WebAPP - BACKEND
## Description
This is the backend of the project "Manage Fanpage and Sentiment Analysis WebAPP". This project is a web application that allows users to manage their fanpages and analyze the sentiment of the comments on their posts. The backend is built with FastAPI and the frontend is built with Node.js. The sentiment analysis is done with the help of the Hugging Face Transformers library. 

Database is host on Supabase, a cloud database service that provides a Postgres database. The database is used to store the information of the users and the fanpages. The user information is used to authenticate the users and the fanpage information is used to get the posts and comments of the fanpages.

If you want to see the frontend of the project, you can go to the following link:
[Manage Fanpage and Sentiment Analysis WebAPP - FRONTEND](https://github.com/Bagumeow/Sentiment_Facebook_FE)

## Installation
 You can install the required packages by running the following command:
```bash
pip install -r requirements.txt
```

## Usage
To run the backend, you can use the following command:
```bash
uvicorn main:app --reload --host"your_host" --port "your_port"
```
You can access the API documentation by going to the following URL:
```
http://your_host:your_port/docs
```
