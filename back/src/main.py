from src.extract import Extract
from src.dto import ArticleDto, ParameterDto
from src.database import Database
import numpy as np
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

db_name = 'db'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["OPTIONS", "GET", "POST"],
    allow_headers=["*"],
    expose_headers=["*"]
)

database = Database()
extract = Extract(db=database)

if Path(f"{db_name}.index").exists() and Path(f"{db_name}.meta").exists():
    database.load(db_name)
else:
    extract.get_and_save()
    database.save(db_name)

database.print()

@app.post("/api/update",
          response_model=None,
          summary="Update data",
          description="Get new data from RSS flux and save them.")
def update_db():
    global extract
    extract.get_and_save()
    database.save()
    return None

@app.post("/api/article",
          response_model=list[ArticleDto],
          summary="Get similar articles",
          description="Returns a list of similar articles based on the input text.",
          )
def get_article(payload: ParameterDto):
    if payload.size < 0 or payload.size > 50:
        raise HTTPException(status_code=400, detail="Size must be between 0 and 50")
    if payload.text == "":
        raise HTTPException(status_code=400, detail="Empty string")

    text_embedding = database.get_emb(payload.text)
    result = database.get_similar(text_embedding, payload.size)
    return result
