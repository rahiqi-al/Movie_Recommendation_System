import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import config
from elasticsearch import Elasticsearch
from pyspark.ml.recommendation import ALS
from flask import Flask, request, jsonify
import logging
from transformation import transformation_trainig

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename="logs/app.log")
logger = logging.getLogger(__name__)

app = Flask(__name__)

#spark = transformation_trainig()
es = Elasticsearch(config.es_host)
#model = ALS.load("path/to/als_model")

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
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)