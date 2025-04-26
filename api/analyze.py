import json
import yt_dlp
import boto3
import os

def handler(request):
    try:
        body = request.get_json()
        video_url = body['video_url']
        print(f"Recebendo URL do vídeo: {video_url}")

        ydl_opts = {'outtmpl': '/tmp/video.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Iniciando o download do vídeo: {video_url}")
            ydl.download([video_url])

        s3 = boto3.client('s3')
        bucket_name = 'gptvideosbaile'
        object_key = 'videos/video.mp4'

        print(f"Enviando para o S3: {bucket_name}/{object_key}")
        s3.upload_file('/tmp/video.mp4', bucket_name, object_key)

        print(f"Gerando URL temporária")
        url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_key}, ExpiresIn=3600)

        return {
            "statusCode": 200,
            "body": json.dumps({"url": url})
        }

    except Exception as e:
        print(f"Erro: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
