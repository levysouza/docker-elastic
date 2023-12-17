from fastapi import APIRouter
from fastapi import File, UploadFile
from apis.es_connector import es_client
from typing import Any
from apis import utils
import pandas as pd


router = APIRouter()

@router.get("")
def main():
    return {"Hello World":"TJ-MATCHING API"}


@router.get("/index_deploy")
def index_deploy()->Any:
    
    data = pd.read_csv('data.csv')
    
    resp = es_client.populate_db(data)

    return {'total':resp[0]}


@router.post("/search_pdf")
async def search_file(file: UploadFile):
    
    raw_text_pdf = utils.extract_pdf(file)

    resp = es_client.elastic_retrievel(raw_text_pdf)

    return resp
    