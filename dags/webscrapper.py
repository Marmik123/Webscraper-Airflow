from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Function to scrape articles
def scrape_articles(**kwargs):
    keyword = kwargs.get('keyword')  # Replace with a default or passed keyword
    url = f"https://backend.finshots.in/backend/search/?q={keyword}" 
    print(url) # Adjust to the actual site
    response = requests.get(url)
    data=response.json()
        
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {url} with status {response.status_code}")

    print('#########RESPONSE######')
    print(data)
    print('#######################')
    
    #CONVERTING STR INTO DATE AND SORTING BASED ON PUBLISHED DATE
    post_sorted=sorted(
    data['matches'],
    key=lambda x: datetime.strptime(x["published_date"].split('+')[0][:19] + "+" + x["published_date"].split('+')[1], "%Y-%m-%dT%H:%M:%S%z") ,
    reverse=True)
    latest_five=post_sorted[:5]
    for post in latest_five:
        print('$$$ LATEST FIVE POST $$')
        print(post)    
        print('##########')
    # soup = BeautifulSoup(response.text, 'html.parser')
    # print(url)
    # print(soup)
    
    # articles = []
    
    # for item in soup.find_all('article', limit=5):  # Adjust tag as needed
    #     title = item.find('h2').text.strip() if item.find('h2') else "No title"
    #     link = item.find('a')['href'] if item.find('a') else "No link"
    #     date = item.find('time')['datetime'] if item.find('time') else "No date"
    #     articles.append({"title": title, "link": link, "date": date})

    # # Log or save results (replace this with database storage if needed)
    # for article in articles:
    #     print(article)  # Replace with a database insert or file write

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define the DAG
with DAG(
    dag_id='web_scraper_pipeline',
    default_args=default_args,
    description='A pipeline to scrape articles',
    schedule_interval=None,  # Run on demand
    start_date=datetime(2024, 11, 1),
    catchup=False,
) as dag:

    scrape_task = PythonOperator(
        task_id='scrape_articles',
        python_callable=scrape_articles,
        op_kwargs={'keyword': 'HDFC'},  # Replace or pass dynamically
    )

    scrape_task
