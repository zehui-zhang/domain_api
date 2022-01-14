# Data Crawler from Domain.com API | AWS S3 EC2 | Docker Deployment

This is a practice about data crawler, AWS S3 and EC2, and docker.

The purpose is to implement a python application that can retrieve the listing summary about Sydney real estate from Domain.com, and upload data to AWS S3. 

The python application is deployed to Docker and can be run in AWS EC2.


## Table of Contents

- [Background](#background)
- [Prerequisite](#prerequisite)
- [Instruction](#instruction)


## Background

Domain API used in this case https://developer.domain.com.au/docs/latest/apis/pkg_properties_locations 

Endpoint https://developer.domain.com.au/docs/v1/apis/pkg_properties_locations/references/salesresults_listings 

## Prerequisite

- Create Domain Developer Account https://developer.domain.com.au/ 
- Install Docker Desktop
- Create AWS Account, get credential pem file.

## Instruction
### 1. creat a ec2 instance, then connect to ec2 instance
```
    ssh -i <credentail pem file> ec2-user@<ec2 instance public ip>
```
