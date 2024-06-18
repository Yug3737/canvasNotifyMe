from fastapi import FastAPI, Query, Path, Body
from typing import Annotated
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default= None, title="The decsription of the item", max_length=300
    ) 
    price: float = Field(gt=0, description="The price must be greater than 0")
    tax: float | None = None

app = FastAPI()

class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id":item_id, "item": item}
    return results
