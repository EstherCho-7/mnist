import jigeum.seoul
import os

def run():
    # 1. image_processing table -> prediction_result IS NULL 인 ROW 1개
    from mnist.db import select, dml
    sql= "select num from image_processing where prediction_result IS NULL"
    result = select(query=sql,size=1)

    # 2. 랜덤으로 0~9 중 하나 값을 prediction_result 컬럼에 업데이ㅡ
    import random
    rnum= random.randint(0,9)
    sql= "update image_processing set prediction_result=%s where num = %s"
    insert_row=dml(sql,rnum,result[0]['num'])

    # prediction_model, time도 업데이트
    sql= "update image_processing set prediction_model= %s,prediction_time=%s where num = %s"
    insert_row=dml(sql,f"model{rnum}.pkl",jigeum.seoul.now(),result[0]['num'])

    # 3. LINE으로 처리 결과 전송
    import requests
    api_url = "https://notify-api.line.me/api/notify"
    token = os.getenv('ACCESS_TOKEN','false')

    headers = {'Authorization':'Bearer '+token}

    message = {
       "message" : f"{jigeum.seoul.now()}:task done successful"
    }

    requests.post(api_url, headers= headers , data = message)

    print(f"작업 요청 시간:{jigeum.seoul.now()}")
    return {"hello":" world"}
