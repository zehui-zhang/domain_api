import requests
import pandas as pd
from datetime import datetime
import boto3

def main():
    access_token = get_api_token()
    result = get_sales_results(access_token)
    timestamp = get_current_time()
    file_name = save_as_csv(result,timestamp)
    upload_to_s3(file_name)

def get_api_token():
    client_id = 'client_20afd1ce29eeec057cafe70570f54ce7'
    client_secret= 'secret_9a3436a977c2896a96fe8e65738e42ea'
    scopes = ['api_salesresults_read']
    auth_url = 'https://auth.domain.com.au/v1/connect/token'

    response = requests.post(auth_url, data = {
                    'client_id':client_id,
                    'client_secret':client_secret,
                    'grant_type':'client_credentials',
                    'scope':scopes,
                    'Content-Type':'text/json'
    })

    json_res = response.json()
    access_token = json_res['access_token']
    print('Connecting to api...')
    return access_token

#get sydney sales results
def get_sales_results(access_token):
    url_endpoint = 'https://api.domain.com.au/v1/salesResults/'
    city = 'Sydney/listings'

    auth = {'Authorization':'Bearer ' + access_token}
    url = url_endpoint + city
    r = requests.get(url, headers=auth)
    result = r.json()
    print('Getting raw data...')
    return result

#get current timestamp
def get_current_time():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    print('The current time is: ' + timestamp)
    return timestamp


def save_as_csv(result,timestamp):
    file_name = 'sydney_sales_results'+ timestamp + '.csv'
    df = pd.DataFrame(result)
    df.to_csv(file_name,encoding='utf-8',index=False)
    print('The csv file has been generated locally...')
    return file_name

def upload_to_s3(file_name):
    s3 = boto3.resource('s3')
    bucket_name = 'domain-sydney'
    s3.meta.client.upload_file(file_name,bucket_name,file_name)
    print('The csv file has been uploaded to S3 successfully...')
    print('The file name is ' + file_name)

main()