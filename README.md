# GPT Video Processor - Node.js Version

Este projeto cria uma API serverless com Node.js para:
- Receber uma URL de vídeo do YouTube
- Fazer download usando yt-dlp
- Subir o vídeo para o S3
- Gerar URL temporária

## Endpoints

POST `/api/analyze`

Body:
```json
{
  "video_url": "https://www.youtube.com/watch?v=ID_DO_VIDEO"
}
```
