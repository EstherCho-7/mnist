FROM python:3.11

WORKDIR /code

RUN apt update
RUN apt install -y cron
COPY ml-work-cronjob /etc/cron.d/ml-work-cronjob
RUN crontab /etc/cron.d/ml-work-cronjob

COPY src/mnist/main.py /code/
COPY pr.sh /code/pr.sh

RUN pip install --no-cache-dir --upgrade git+https://github.com/EstherCho-7/mnist.git@0.5.0

CMD ["sh", "run.sh"]
