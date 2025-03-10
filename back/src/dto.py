from pydantic import BaseModel

class ParameterDto(BaseModel):
    text: str
    size: int

class ArticleDto(BaseModel):
    title: str
    link: str
    author: str
    content: str
    distance: float

class DBElem(BaseModel):
    title: str
    link: str
    author: str
    content: str
