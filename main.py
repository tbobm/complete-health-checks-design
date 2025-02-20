from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def read_root():
    return {"message": "healthy"}


@app.get("/")
def read_root():
    return {"Hello": "World"}
