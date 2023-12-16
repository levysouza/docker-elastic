from fastapi import FastAPI
import requests
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers


app = FastAPI()

es_client = Elasticsearch([{'host': 'host.docker.internal', 'port':9200, 'scheme':'http'}],request_timeout=30)
data = pd.read_csv('data.csv')

@app.get("/")
def main():
    return {"Hello World":"TJ-MATCHING API"}


def index_payload():

    for i, row in data.iterrows():
        
        process_id = str(row['processo'])
        process_file = str(row['arquivo'])
        cod_subject = str(row['codigos_assunto'])
        cod_classs = (row['classe_processual'])
        decision_file = str(row['decisao'])
        text_petition = str(row['raw_peticao'])
        clean_text_petition = str(row['peticao_clean_text'])
        cod_judge = row['magistrado']

        yield {
            "_index": "index-tj-matching",
            "_source": {
                "process_id": process_id,
                "process_file": process_file,
                "cod_subject": cod_subject,
                "cod_classs": cod_classs,
                "decision_file": decision_file,
                "text_petition": text_petition,
                "clean_text_petition":clean_text_petition,
                "cod_judge": cod_judge
            }
        }     


@app.post("/index_deploy/")
def index_deploy():

    # drop the index if it exists
    if es_client.indices.exists(index='index-tj-matching'):

        es_client.indices.delete(index='index-tj-matching')
    
    #creating the index
    resp = helpers.bulk(es_client, index_payload())

    return {"resp":resp}


@app.get("/search/{query}")
def index_search(query:str):

    resp = es_client.search(
        index="index-tj-matching", 
        body = {
            "_source": ["process_id","process_file"],
            "from" : 0,
            "size" : 10,
            "query": {
                "multi_match":{
                "type": "most_fields",
                "query":  query, 
                "fields": ["clean_text_petition"] 
                }
            }
        }
    )
    return resp
    


