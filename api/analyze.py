import json
import yt_dlp
import boto3
import os

def handler(event, context):
    print("🔵 Início da função analyze")

    try:
        print(f"📝 Evento recebido: {event}")

        if 'body' not in event:
            raise ValueError("❌ Nenhum body recebido na requisição!")

        body = json.loads(event['body'])
        print(f"📦 Body decodificado: {body}")

        if 'video_url' not in body:
            raise ValueError("❌ Campo 'video_url' não encontrado no body!")

        video_url = body['video_url']
        print(f"🎬 URL do vídeo: {video_url}")

        # Download do vídeo
        try:
            ydl_opts = {'outtmpl': '/tmp/video.mp4'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"⬇️ Baixando vídeo...")
                ydl.download([video_url])
            print(f"✅ Download concluído.")
        except Exception as download_error:
            print(f"❌ Erro ao baixar vídeo: {str(download_error)}")
            raise download_error

        # Upload para S3
        try:
            print(f"🛫 Iniciando upload para S3...")
            s3 = boto3.client('s3')
            bucket_name = os.environ.get('AWS_S3_BUCKET_NAME', 'gptvideosbaile')
            object_key = 'videos/video.mp4'

            s3.upload_file('/tmp/video.mp4', bucket_name, object_key)
            print(f"✅ Upload para S3 feito.")
        except Exception as s3_error:
            print(f"❌ Erro ao fazer upload para S3: {str(s3_error)}")
            raise s3_error

        # Gerar URL temporária
        try:
            print(f"🔗 Gerando URL temporária...")
            url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_key}, ExpiresIn=3600)
            print(f"✅ URL gerada: {url}")
        except Exception as url_error:
            print(f"❌ Erro ao gerar URL temporária: {str(url_error)}")
            raise url_error

        return {
            "statusCode": 200,
            "body": json.dumps({"url": url})
        }

    except Exception as e:
        print(f"🚨 Erro final detectado: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
