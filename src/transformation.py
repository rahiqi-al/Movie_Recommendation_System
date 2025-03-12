import sys ,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import config
import logging
from pyspark.sql import SparkSession
from load_data_elasticsearch import load_data_elasticsearch
import threading
from pyspark.sql.functions import from_unixtime, col,to_date, date_format

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename="logs/app.log",filemode='a')
logger=logging.getLogger(__name__)



def transformation_trainig():
    try :
        logger.info('creating the session')

        spark = SparkSession.builder.appName('movie').getOrCreate()

        logger.info('session created successfully')

        df_data = spark.read.csv(config.path+"u.data",  sep="\t", schema=config.data_schema)
        

        df_item = spark.read.csv(config.path+"u.item",  sep="|",  schema=config.item_schema)



        df_user = spark.read.csv(config.path+"u.user", sep="|", schema=config.user_schema)
        
        df=df_data.join(df_user,'userId',how='inner').join(df_item,'movieId','inner').withColumn('datetime',from_unixtime(col("timestamp"))).drop('timestamp').withColumn('time',date_format(col("datetime"),"HH:mm:ss")).withColumn('date',to_date(col("datetime"))).drop('datetime')
        tasks = [
            threading.Thread(target=load_data_elasticsearch, args=(df_data, 'data')),
            threading.Thread(target=load_data_elasticsearch, args=(df_item, 'item_movies')),
            threading.Thread(target=load_data_elasticsearch, args=(df_user, 'user')),
            threading.Thread(target=load_data_elasticsearch, args=(df, 'combined_tables')) ]

        logger.info('starting loading the data')
        for task in tasks:
            task.start()

        for task in tasks:
            task.join()
        logger.info('all data loaded successfully')
    
    except Exception as e :
        logger.exception('error in the function transformation_trainig')
        raise

    

     
    

transformation_trainig()


