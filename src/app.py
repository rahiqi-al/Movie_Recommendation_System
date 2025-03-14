import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import config
from elasticsearch import Elasticsearch
from pyspark.ml.recommendation import ALS , ALSModel
from flask import Flask, request, jsonify
import logging
from pyspark.sql.functions import col
from transformation import transformation_trainig
from load_data_elasticsearch import load_data_elasticsearch
 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename="logs/app.log")
logger = logging.getLogger(__name__)

app = Flask(__name__)

spark = transformation_trainig()

es = Elasticsearch(config.es_host)
model_folder = "/home/ali/Desktop/Movie Recommendation System/model"
try:
    # Get model with lowest RMSE(so basicly the min function whould get the least rmse wich will be x and this x from the list of models )
    best_model_name = min(
        [d for d in os.listdir(model_folder) if d.startswith("als_model")],
        key=lambda x: float(x.split('_')[-1])
    )
    best_model_path = f"file://{os.path.join(model_folder, best_model_name)}"
    
    
    best_model = ALSModel.load(best_model_path)
    logger.info(f"Loaded {best_model_name}")
except Exception as e:
    logger.info(f"Failed: {e}")


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to Movie Recommendation API"})

@app.route('/search/movie', methods=['GET'])
def search_movie():
    try:
        title = request.args.get('title', '')  
        if not title:
            return jsonify({"error": "Title parameter is required"}), 400
        
        query = {
            "query": {
                "match": {
                    "movieTitle": {
                        "query": title,
                        "fuzziness": "AUTO"  # Allow some typo tolerance
                    }
                }
            }
        }
        result = es.search(index="combined_tables", body=query)
        movies = [hit["_source"] for hit in result["hits"]["hits"]]
        
        logger.info(f"Found {len(movies)} movies matching '{title}'")
        return jsonify({"movies": movies})
    except Exception as e:
        logger.error(f"Error searching movie '{title}': {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/recommend/user/<int:user_id>', methods=['GET'])
def recommend_for_user(user_id):
    user_df = spark.createDataFrame([(user_id,)], ["userId"])
    rec_user=best_model.recommendForUserSubset(user_df,5)
    rec_user=rec_user.selectExpr('*',"explode(recommendations) as rec").drop('recommendations')
    rec_user = rec_user.withColumn("movieID", col('rec.movieId')).withColumn("rating", col('rec.rating')).drop('rec')
    load_data_elasticsearch(rec_user,'recomendations')
    rec_flask=[row.asDict() for row in rec_user.collect()]
    return jsonify(rec_flask)

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)