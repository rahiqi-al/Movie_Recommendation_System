Elasticsearch: http://localhost:9200
Kibana: http://localhost:5601
run_the_app: uvicorn app:app --host 0.0.0.0 --port 8000 --reload #but we need to got the folder that have our app to run fast api
flask_Home: http://localhost:8000/
dashbord:http://localhost:5601/app/dashboards#/view/74948170-0018-11f0-bb58-61bb92685bf3?_g=(refreshInterval:(pause:!t,value:60000),time:(from:now-15m,to:now))&_a=()
change_port: netstat -tuln | grep 8000  # do this to check if the port in use if this is true then change the port to free one