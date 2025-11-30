---
id: fastapi-basics
title: FastAPI Routing & Pydantic Cheatsheet
world: world-python
tags: [fastapi, python, backend]
---

# FastAPI Basics

## Request Body
To declare a request body, use Pydantic models:

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
```

## Path Parameters

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```
