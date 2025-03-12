import sys ,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import config
from elasticsearch import Elasticsearch
import logging
logger=logging.getLogger(__name__)


def  load_data_elasticsearch(df,index_name):


    try:
        logger.info('connecting to Elasticsearch ')
        es = Elasticsearch(config.es_host)

        if not es.ping():
            raise ConnectionError("failed to connect to Elasticsearch")
        
        logger.info('connection successful')
        

        if df.rdd.isEmpty():
            raise  ValueError("spark dataFrame is empty")
        
        documents=[row.asDict() for row in df.collect()]

        for document in documents:

            try:
                es.index(index=index_name ,document=document)
            
            except Exception as e :
                logger.exception(f'failed to index the document {document}')
        
        logger.info(f'documents are saved to index ({index_name}) ')

    except ConnectionError as ce:
        logger.exception(f"Connection error: {ce}")
        raise
    except ValueError as ve:
        logger.exception(f"Input error: {ve}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise

  

