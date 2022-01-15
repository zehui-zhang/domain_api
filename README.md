# Data Crawler from Domain.com API | AWS S3 EC2 | Docker Deployment

This is a practice about data crawler, AWS S3 and EC2, and docker.

The purpose is to implement a python application that can retrieve the listing summary about Sydney real estate from Domain.com, and upload data to AWS S3. 

The python application is deployed to Docker and can be run in AWS EC2.


## Table of Contents

- [Background](#background)
- [Prerequisite](#prerequisite)
- [Instruction](#instruction)
- [Further_Steps](#further_steps)
- [Reference](#reference)


## Background

Domain API used in this case https://developer.domain.com.au/docs/latest/apis/pkg_properties_locations 

Endpoint https://developer.domain.com.au/docs/v1/apis/pkg_properties_locations/references/salesresults_listings 

## Prerequisite

- Create Domain Developer Account https://developer.domain.com.au/ 
- Install Docker Desktop
- Create AWS Account, get credential pem file.

## Instruction
### 1. Connect to EC2 
1.1. creat a ec2 instance, then connect to ec2 instance
```
    ssh -i <credentail pem file> ec2-user@<ec2 instance public ip>
```

### 2. Build Python Docker Image
2.1. Dockerfile  
```#deriving the lastest base image: python
FROM python:latest

#copy requirements.txt to docker image
COPY requirements.txt requirements.txt

#install packages in requirements.txt in docker one by one
RUN pip3 install -r requirements.txt

#copy all files in docker
COPY . .

# run command 'python3 app.py'
CMD ["python3","app.py"]
```

2.2. Build an image
```
# build a docker image, you can replace <python docker> with your own repository name.
docker build --tag python-docker .

#view local images
docker images

#tag images
docker tag python-docker:latest python-docker:v1
```

2.3. Run a Docker container
```
#run your docker container locally
# -d start a container in detached mode 
# -P random port number
# --name name the docker container
docker run -d - P --name ec2-docker <dockeraccount>/python-docker:v1

#check the running container
docker ps
```

2.4. Push Docker Image to Dockerhub
```
docker tag python-docker:v1 <dockeraccount>/python-docker:v1
```

### 3. Install Docker image on EC2
3.1. 
```
#update
sudo yum update -y

#install most recent package
sudo amazon-linux-extras install docker

#start the service docker
sudo service docker start

#add the ec2-docker user to the group
sudo usermod -a -G docker ec2-user

#you need to logout to take affect
logout

#login again
ssh -i <pem file> ec2-user@<public ip>

#check the docker version
docker --version
```

### 4. Run Docker container on EC2
```
#pull the image
docker pull <dockeraccount>/python-docker:v1

#list the images
docker images

#run the container
docker run -d -P --name ec2-docker <dockeraccount>/python-docker:v1

#exec into docker container 
docker exec -it python-docker:v1 /bin/sh
```


## Further_Steps
1. Upload data to AWS RDS
2. ETL
3. Docker Upgrade
4. CICD



## Reference
Docker run command https://www.runoob.com/docker/docker-run-command.html 

Running Docker Containers On AWS EC2 https://medium.com/bb-tutorials-and-thoughts/running-docker-containers-on-aws-ec2-9b17add53646 