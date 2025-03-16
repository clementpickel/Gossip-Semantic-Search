# Get started

```
pip install requirement.txt
python -m uvicorn src.main:app --reload
```

## Documentation

You can see the Swagger after starting the project at http://localhost:8000/docs

## How it works ?

### Update

1. Get all the articles from the RSS flux
2. Get the embeding of the title from google's api
3. Save the embeding and the article in a vector database faiss

### Search

1. Get the embeding of teh query from google's api
2. Get the 3 closest vector from the database
3. Return there metadata

## Ressources

[FAISS github](https://github.com/facebookresearch/faiss)
[Obtenir des embedding de texte](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings?hl=fr)
[Vectoring Words (Word Embeddings)](https://www.youtube.com/watch?v=gQddtTdmG_8), Computerphile
[Camembert model](https://huggingface.co/almanach/camembert-base)
[Text embeddings & semantic search](https://www.youtube.com/watch?v=OATCgQtNX2o), HuggingFace

[Feedparser documentation](https://pypi.org/project/feedparser/)
[RSS made easy](https://www.youtube.com/watch?v=6HNUqDL-pI8), Growth origin
[Public flux rss](https://www.public.fr/flux-rss)
[VSD flux rss](https://vsd.fr/flux-rss/)

## Reference

```
@article{douze2024faiss,
title={The Faiss library},
author={Matthijs Douze and Alexandr Guzhva and Chengqi Deng and Jeff Johnson and Gergely Szilvasy and Pierre-Emmanuel Mazaré and Maria Lomeli and Lucas Hosseini and Hervé Jégou},
year={2024},
eprint={2401.08281},
archivePrefix={arXiv},
primaryClass={cs.LG}
}
```
