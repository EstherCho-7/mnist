# mnist

# What is it?
- Tensorflow를 이용하여 사진 등의 파일의 데이터를 DB에 저장하고, 학습된 데이터들로 결과값을 도출하는 Classifier

## How it works?
1. 70,000개의 흑백반전된, 0부터 9까지의 숫자가 적힌 손글씨를 학습
2. keras로 학습 모델 저장
3. FastAPI로 파일을 Upload하고 예측하는 application 제작
4. 해당 app에 흰 배경에 검은 글씨인 손글씨 숫자 파일을 Upload 시 어떤 숫자인지 예측

## How to start?
```bash
# Docker
$ docker pull esthercho7/mnist:0.8.0
$ docker run -p <PORT> --name <CONTAINER_NAME> -e ACCESS_TOKEN=<YOUR_LINE_TOKEN> -v <UPLOAD_DIRECTORY> esthercho7/mnist:0.8.0
$ docker exec -it <CONTAINER_NAME> bash

# In Container
$ ml-worker

# Tracking log
$ tail -f /var/log/worker.log
```
- or, wait for notification of LINE (notify every 3 minutes)

## Result

