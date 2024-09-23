
def run():
    from mnist.db import select, dml
    sql= "SELECT num FROM image_processing where prediction_result IS NULL"
    result = select(query=sql,size=1)

    import random
    rnum= random.randint(0,9)
    sql= "UPDATE image_processing SET prediction_result=%s WHERE num = %s"
    insert_row=dml(sql,rnum,result[0]['num'])

    sql= "UPDATE image_processing SET prediction_model= %s,prediction_time=%s WHERE num = %s"
    insert_row=dml(sql,f"model{rnum}.pkl",jigeum.seoul.now(),result[0]['num'])

    import requests
    api_url = "https://notify-api.line.me/api/notify"
    token = os.getenv('LINE_API_KEY','false')

    headers = {'Authorization':'Bearer '+token}

    message = {
       "message" : f"{jigeum.seoul.now()}:task done successful"
    }

    requests.post(api_url, headers= headers , data = message)

    print(f"작업 요청 시간:{jigeum.seoul.now()}")
    return {"hello", "world"}
