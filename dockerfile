#deriving the lastest base image: python
FROM python:latest

#copy requirements.txt to docker image
COPY requirements.txt requirements.txt

#install packages in requirements.txt in docker one by one
RUN pip3 install -r requirements.txt

#copy all files in docker
COPY . .

# run command 'python3 app.py'
CMD ["python3","app.py"]