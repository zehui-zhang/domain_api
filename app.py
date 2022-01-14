'''
This app will retrieve the listing summaries corresponding to the sales result of Sydney from Domain.com API.
https://developer.domain.com.au/docs/v1/apis/pkg_properties_locations/references/salesresults_listings

The data will be upload to AWS S3 bucket called "domain-sydney"

The prerequisites are
1. create a Domain Developer Account in order to get credentials. in this case, I choose OAtuth 2.0 (you can replace with your credentail instead)
2. create AWS account, then create a S3 bucket called "domain-sydeny" (you can replace with your bucket name)

Functions:
1. main()
    This function will get api access token, and retrieve data about Sydney sales results from Domain.com API, 
    then get current time, and save data as a csv file locally, finally upload the file to S3 bucket.

2. get_api_token()
    This function will use credential to get the token that access API

3. get_sales_results(access_token)
    This function will use access token to retrieve data from Domain.com API

4. get_current_time()
    This function will generate the current time, so we can know when the data has been retrieved.

5. save_as_csv(result,timestamp)
    This function will convert data to csv file. 
    The file name will include timestamp(current time)

6. upload_to_s3(file_name)
    This functino will upload the local file to S3 bucket, in this case, the bucket is "domain-sydney".
'''

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