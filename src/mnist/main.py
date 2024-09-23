from typing import Annotated
import os
import jigeum.seoul
from fastapi import FastAPI, File, UploadFile
import pymysql.cursors


app = FastAPI()


@app.post("/files/")
async def file_list():
    from mnist.db import get_conn
    conn=get_conn()
    with conn:
        with conn.cursor() as cursor:
            sql="select * from image_processing where prediction_time IS NULL order by num"
            cursor.execute(sql)
            result=cursor.fetchall()
    return result


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    
    # 파일 저장
    img = await file.read()
    file_name = file.filename
    file_ext = file.content_type.split('/')[1]  # "image/jpeg"

    # 디렉토리가 없으면 오류, 코드에서 확인 및 만들기 추가
    upload_dir = "/home/ubuntu/images/n15/"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    import uuid
    file_full_path = os.path.join(upload_dir, f'{uuid.uuid4()}.{file_ext}')

    with open(file_full_path, "wb") as f:
        f.write(img)

    sql="insert into image_processing(file_name, file_path, request_time, request_user) values(%s, %s, %s, %s)"
    
    import jigeum.seoul
    from mnist.db import dml
    insert_row=dml(sql, file_name, file_full_path, jigeum.seoul.now(), 'n15')
    return {
            "filename": file.filename,
            "content_type": file_ext,
            "file_full_path": file_full_path,
            "insert_row_count": insert_row
           }


@app.get('/many/{size}')
def many(size: int = -1):
    from mnist.db import get_conn
    sql="select * from image_processing where prediction_time IS NULL order by num"
    conn=get_conn()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result=cursor.fetchmany(size)

    return result

@app.get('/one')
def one():
    from mnist.db import select
    sql="select * from image_processing where prediction_time IS NULL order by num limit 1"
    result=select(query=sql, size=1)
    return result[0]

@app.get('/all')
def all():
    from mnist.db import select
    sql="select * from image_processing"
    result=select(query=sql, size=-1)
    return result
