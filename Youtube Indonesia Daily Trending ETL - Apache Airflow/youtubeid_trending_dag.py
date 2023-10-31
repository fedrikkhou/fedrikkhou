import time
import json
from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from ytid.youtube_etl import YouTube_ETL

default_args ={
    'owner':'Fedrik',
    'retries':5,
    'retry_delay':timedelta(minutes=2)
}

@dag(dag_id='youtubeid_trending_ETL_v3',
    default_args = default_args,
    start_date=datetime(2023, 10, 28),
    schedule_interval='@daily')
def run_etl():

    #extract tasks
    @task(depends_on_past=False)
    def get_youtubeid_trending():
        API_KEY='AIzaSyD9WdysfVOaA5pLhb19s-xPTSoT-44x7lA'
        URL='https://youtube.googleapis.com/youtube/v3/videos'

        yt_etl = YouTube_ETL(api_key = API_KEY, url = URL)
        
        print("Get Youtube ID Trending Vidoes")
        videos = yt_etl.get_trendings()
        print(f"DATETIME NOW = {datetime.now()}" )

        df_videos = pd.DataFrame([
            video.to_dict(trending_time=datetime.now())
            for video in videos
        ])
        
        # Convert the DataFrame to JSON
        json_youtubeid_trending = df_videos.to_json(orient='records')
        return json_youtubeid_trending
    
    @task
    def save_youtubeid_trending(json_youtubeid_trending):
        # Parse the JSON data into a Python data structure
        data_trending = json.loads(json_youtubeid_trending)

        # Create a DataFrame from the Python data structure
        df_trending = pd.DataFrame(data_trending)
        df_trending['tags'] = df_trending['tags'].apply(json.dumps)
        df_trending['allowed_region'] = df_trending['allowed_region'].apply(json.dumps)

        postgres_hook = PostgresHook(postgres_conn_id="postgres_youtube")
        
        print("Executing INSERT Data to DB")
        df_trending.to_sql('youtubeidtrending', postgres_hook.get_sqlalchemy_engine(), if_exists='append', chunksize=1000, index=False)


    task_get_youtubeid_trending = get_youtubeid_trending()
    task_save_youtubeid_trending = save_youtubeid_trending(task_get_youtubeid_trending)
    task_get_youtubeid_trending >> task_save_youtubeid_trending

greet_dag = run_etl()