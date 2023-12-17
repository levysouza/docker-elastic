from elasticsearch import Elasticsearch
from elasticsearch import helpers
from apis import utils

class ES_connector:
    def __init__(self) -> None:
        self.es_instance = None
        self.connect()

    def connect(self):
        # we can put host and port in config or env
        host = 'host.docker.internal'
        port = "9200"
        scheme = 'http'
        es = Elasticsearch([{'host': 'host.docker.internal', 'port':9200, 'scheme':'http'}],request_timeout=30)
        self.es_instance = es

    def populate_db(self, data):
        # drop the index if it exists
        if self.es_instance.indices.exists(index='index-tj-matching'):

            self.es_instance.indices.delete(index='index-tj-matching')
    
        #creating the index
        resp = helpers.bulk(es_client.es_instance, utils.index_payload(data))
        
        return resp

    def elastic_retrievel(self,query):
        resp = self.es_instance.search(
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
    
es_client = ES_connector()