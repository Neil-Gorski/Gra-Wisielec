import pydantic

from pydantic import BaseModel, Field

class CategoriesSchema(BaseModel):
    id : int = Field(default=None)
    name : str = Field(default=None)
    description : str = Field(default=None)
    class Config:
        the_schema = {
            "categories_demo" :{
                "name": "City",
                "description": "This category is about citys"
            } 
        }

class WordSchema(BaseModel):
    id : int = Field(default=None)
    category_id : int = Field(default=None)
    word : str = Field(default=None)
    class Config:
        the_schema = {
            "words_demo" :{
                "category_id": "1",
                "word": "Krakow"
            } 
        }

