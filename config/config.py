import yaml
from dotenv import load_dotenv
import os

load_dotenv()

class config:

    with open('config/config.yml','r')as file:
        config_data=yaml.load(file,Loader=yaml.FullLoader)





config=config()


#print(config.test1,config.test2)