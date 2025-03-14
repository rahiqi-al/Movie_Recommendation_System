import sys ,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import config
import logging
from pyspark.sql import SparkSession
from load_data_elasticsearch import load_data_elasticsearch
import threading
from pyspark.sql.functions import from_unixtime, col,to_date, date_format
from pyspark.ml.recommendation import ALS 
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
import datetime

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

        logger.info('starting on training the model')

        df_data_tarin,df_data_test=df_data.randomSplit([0.8,0.2])
        als=ALS(userCol='userId',itemCol='movieId',ratingCol='rating')
        paramgrid=ParamGridBuilder().addGrid(als.regParam,[0.3,0.01,0.15]).addGrid(als.rank,range(2,8)).build()
        evaluator=RegressionEvaluator(metricName='rmse',predictionCol='prediction',labelCol='rating')
        crossval=CrossValidator(estimator=als,estimatorParamMaps=paramgrid,evaluator=evaluator,numFolds=5)
        crossmodel=crossval.fit(df_data_tarin)
        best_model=crossmodel.bestModel
        predictions=best_model.transform(df_data_test)
        rmse=evaluator.evaluate(predictions.filter(col('prediction')!='nan'))
        model_path = f'file:///home/ali/Desktop/Movie Recommendation System/model/als_model_{datetime.date.today().strftime("%Y-%m-%d")}_{rmse}'
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        best_model.save(model_path)

        logger.info('model trained and got saved')

        return spark
    
            
    except Exception as e :
        logger.exception('error in the function transformation_trainig')
        raise

    

