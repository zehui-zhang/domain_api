#deriving the lastest base image
FROM python:latest
 
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3","data_crawler.py"]