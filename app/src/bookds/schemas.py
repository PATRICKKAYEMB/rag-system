from pydantic import BaseModel
from datetime import datetime,date 
import uuid
class Book(BaseModel):
    id:uuid.UUID
    title:str
    pushisher:date
    page_count:int
    panguage:str
    create_at:datetime
    update_at:datetime

class BookCreateModel(BaseModel):
        pushisher:str
        title:str
        pushisher:str
        page_count:int
        panguage:str


class BookUpdaeModel(BaseModel):
    title:str
    pushisher:str
    page_count:int
    panguage:str
