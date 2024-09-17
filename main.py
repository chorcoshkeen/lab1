# -*- coding: utf-8 -*-
import os
from model_utils import load_model, make_inference
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel


class Instance(BaseModel):
    hair: int 
    feathers: int 
    eggs: int 
    milk: int 
    airborne: int 
    aquatic: int 
    predator: int 
    toothed: int 
    backbone: int 
    breathes: int 
    venomous: int 
    fins: int 
    legs: int 
    tail: int 
    domestic: int 
    catsize: int 


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
model_path: str = "./models/pipeline.pkl"
if model_path is None:
    raise ValueError("The environment variable $MODEL_PATH is empty!")


async def is_token_correct(token: str) -> bool:
    dummy_correct_token = "00000"
    return token == dummy_correct_token


async def check_token(token: str = Depends(oauth2_scheme)) -> None:
    if not await is_token_correct(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/healthcheck")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predictions")
async def predictions(instance: Instance,
                      token: str = Depends(check_token)) -> dict[str, str]:
    return make_inference(load_model(model_path), instance.model_dump())