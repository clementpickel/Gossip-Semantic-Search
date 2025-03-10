from src.extract import Extract
from src.embedding import Embedding
from src.dto import ArticleDto, ParameterDto

import numpy as np
from fastapi import FastAPI, HTTPException

app = FastAPI()
extract = Extract()
embedding = Embedding()
data = extract.get_data_csv()
data = np.array(data)
title_vectors = extract.unpack(data)

@app.post("/api/update/",
          response_model=None,
          summary="Update data",
          description="Get new data from RSS flux and save them.")
def update_db():
    global data, title_vectors
    rss_flux = extract.get_data_rss()
    data = extract.save_data(rss_flux)
    data = np.array(data)
    title_vectors = extract.unpack(data)
    return None

@app.post("/api/article/",
          response_model=list[ArticleDto],
          summary="Get similar articles",
          description="Returns a list of similar articles based on the input text.")
def get_article(payload: ParameterDto):
    if payload.size < 0 or payload.size > 50:
        raise HTTPException(status_code=400, detail="Size must be between 0 and 50")
    if payload.text == "":
        raise HTTPException(status_code=400, detail="Empty string")

    text_embedding = embedding.embedding(payload.text)
    data_index = embedding.get_similar(text_embedding, title_vectors)
    res = []
    for i in range(payload.size):
        res.append(extract.line_to_json(data[data_index[i]]))
    return res
