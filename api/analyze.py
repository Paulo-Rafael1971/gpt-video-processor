from fastapi import FastAPI
import yt_dlp
import boto3
import os

app = FastAPI()

# Configuração do S3
s3 = boto3.client('s3')
bucket_name = 'gptvideosbaile'  # Substitua pelo seu nome de bucket

@app.post("/analyze")
def analyze(payload: dict):
    video_url = payload['video_url']
    
    # Baixar o vídeo
    ydl_opts = {'outtmpl': '/tmp/video.mp4'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Upload para o S3
    file_name = '/tmp/video.mp4'
    object_key = f"videos/{os.path.basename(file_name)}"
    s3.upload_file(file_name, bucket_name, object_key)

    # Gerar URL pré-assinada
    url = s3.generate_presigned_url('get_object',
                                   Params={'Bucket': bucket_name, 'Key': object_key},
                                   ExpiresIn=3600)
    return {"url": url}
