# GPT Video Processor API

Essa API permite o processamento de vídeos de plataformas como o YouTube. O processo inclui o download do vídeo, upload para o S3 da AWS, e geração de um link de compartilhamento temporário para acesso.

## Endpoints

### POST /analyze
Esse endpoint permite que você envie a URL de um vídeo para ser processado.

#### Body Request
```json
{
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}