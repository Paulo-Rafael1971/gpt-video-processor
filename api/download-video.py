import json
import boto3
import yt_dlp
import os
import tempfile

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def handler(event, context):
    try:
        body = json.loads(event['body'])
        video_url = body.get('url')

        if not video_url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "URL não fornecida."}),
            }

        with tempfile.TemporaryDirectory() as tmpdirname:
            ydl_opts = {
                'outtmpl': os.path.join(tmpdirname, '%(id)s.%(ext)s'),
                'format': 'best'
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                file_path = ydl.prepare_filename(info_dict)

            s3_key = os.path.basename(file_path)
            s3.upload_file(file_path, BUCKET_NAME, s3_key)

        file_url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': s3_key}, ExpiresIn=3600)

        return {
            "statusCode": 200,
            "body": json.dumps({"file_url": file_url}),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }