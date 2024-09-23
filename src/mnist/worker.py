import jigeum.seoul
import os
import random

def get_job_img_task():
    from mnist.db import select
    sql="select num, file_name, file_path from image_processing where prediction_result IS NULL order by num limit 1"
    r=select(sql, 1)

    if len(r)>0:
        return r[0]
    else:
        return None

def prediction(file_path, num):
    from mnist.db import dml
    sql="update image_processing set prediction_result=%s, prediction_model='n15', prediction_time=%s where num=%s"
    presult=random.randint(0, 9)
    dml(sql, presult, jigeum.seoul.now(), num)
    return presult

def run():
    job=get_job_img_task()
    if job is None:
        print(f"{jigeum.seoul.now()}- job is None")
        return

    num=job['num']
    file_name=job['file_name']
    file_path=job['file_path']
    
    presult= prediction(file_path, num)

    print(jigeum.seoul.now())

    # line
    import requests
    api_url = "https://notify-api.line.me/api/notify"
    token = os.getenv('ACCESS_TOKEN','false')

    headers={'Authorization':'Bearer '+token}

    message={
        "message": f"{jigeum.seoul.now()}: 작업에 성공, result={presult}"
            }

    requests.post(api_url, headers=headers, data=message)
