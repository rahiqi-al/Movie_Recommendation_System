from flask import Flask, request, jsonify
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename="logs/app.log")
logger = logging.getLogger(__name__)

app = Flask(__name__)


# endpoint they will be here where i will have two enpoints one for recommendation & query something (just a normal search)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)