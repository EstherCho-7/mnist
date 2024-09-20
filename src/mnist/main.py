from typing import Annotated
import os
import jigeum.seoul
from fastapi import FastAPI, File, UploadFile
import pymysql.cursors


app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    
    # 파일 저장
    img = await file.read()
    file_name = file.filename
    file_ext = file.content_type.split('/')[1]  # "image/jpeg"

    # 디렉토리가 없으면 오류, 코드에서 확인 및 만들기 추가
    upload_dir = "/home/esthercho/code/mnist/image"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    import uuid
    file_full_path = os.path.join(upload_dir, f'{uuid.uuid4()}.{file_ext}')

    with open(file_full_path, "wb") as f:
        f.write(img)

    sql="insert into image_processing(file_name, file_path, request_time, request_user) values(%s, %s, %s, %s)"
    conn=pymysql.connect(host='127.0.0.1', port=53306, user='mnist', password='1234', database='mnistdb', cursorclass=pymysql.cursors.DictCursor)

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, ('file_name', 'file_full_path', jigeum.seoul.now(), 'n15'))

        conn.commit()

    return {
            "filename": file.filename,
            "content_type": file_ext,
            "file_full_path": file_full_path,
           }


@app.get('/many/{size}')
def many(size: int):
    sql="select * from image_processing where prediction_time IS NULL order by num"
    conn=pymysql.connect(host='127.0.0.1', port=53306, user='mnist', password='1234', database='mnistdb', cursorclass=pymysql.cursors.DictCursor)

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result=cursor.fetchmany(size)

    return result

@app.get('/one')
def one():
    sql="select * from image_processing where prediction_time IS NULL order by num"
    conn=pymysql.connect(host='127.0.0.1', port=53306, user='mnist', password='1234', database='mnistdb', cursorclass=pymysql.cursors.DictCursor)

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result=cursor.fetchone()

    return result

@app.get('/all')
def all():
    sql="select * from image_processing where prediction_time IS NULL order by num"
    conn=pymysql.connect(host='127.0.0.1', port=53306, user='mnist', password='1234', database='mnistdb', cursorclass=pymysql.cursors.DictCursor)

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result=cursor.fetchall()

    return result
