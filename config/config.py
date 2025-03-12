import yaml
from dotenv import load_dotenv
import os

load_dotenv()

class config:

    with open('config/config.yml','r')as file:
        config_data=yaml.load(file,Loader=yaml.FullLoader)

        path=config_data['PATH']
        data_schema=config_data['DATA_SCHEMA']
        item_schema=config_data['ITEM_SCHEMA']
        user_schema=config_data['USER_SCHEMA']



        es_host=os.getenv('ES_HOST')







config=config()


#print(config.user_schema)