from fastapi import FastAPI
import yt_dlp, boto3, os

app = FastAPI()

# Cliente S3 usando variáveis de ambiente
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
BUCKET = os.getenv("S3_BUCKET", "gptvideosbaile")

# Health-check em /
@app.get("/")
def health():
    return {"status":"alive"}

# Seu endpoint principal
@app.post("/analyze")
def analyze(payload: dict):
    video_url = payload.get("video_url")
    if not video_url:
        return {"error":"payload precisa de video_url"}

    # 1) Baixar vídeo para /tmp/video.mp4
    ydl_opts = {"outtmpl":"/tmp/video.mp4"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # 2) Enviar ao S3
    key = f"videos/{os.path.basename('/tmp/video.mp4')}"
    s3.upload_file("/tmp/video.mp4", BUCKET, key)

    # 3) Gerar link pré-assinado
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket":BUCKET,"Key":key},
        ExpiresIn=3600
    )
    return {"url":url}