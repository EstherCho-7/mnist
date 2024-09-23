import jigeum.seoul
import os
import random

def get_job_img_task():
    from mnist.db import select
    sql="select num, file_name, file_path from image_processing where prediction_result IS NULL order by num limit 1"
    r=select(sql, 1)
    return r[0]

def prediction(file_path, num):
    from mnist.db import dml
    sql="update image_processing set prediction_result=%s, prediction_model='n15', prediction_time=%s where num=%s"
    presult=random.randint(0, 9)
    dml(sql, presult, jigeum.seoul.now(), num)
    return presult

def run():
    job=get_job_img_task()
    num=job['num']
    file_name=job['file_name']
    file_path=job['file_path']

    presult= prediction(file_path, num)
