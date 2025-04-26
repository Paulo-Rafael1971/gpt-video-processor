const express = require('express');
const AWS = require('aws-sdk');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const router = express.Router();

AWS.config.update({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.AWS_REGION
});

const s3 = new AWS.S3();

router.post('/analyze', async (req, res) => {
  try {
    const { video_url } = req.body;
    if (!video_url) {
      return res.status(400).json({ error: 'URL do vídeo é obrigatória' });
    }

    const filePath = '/tmp/video.mp4';
    const command = `yt-dlp -o "${filePath}" "${video_url}"`;

    exec(command, async (error, stdout, stderr) => {
      if (error) {
        console.error('Erro ao baixar vídeo:', error);
        return res.status(500).json({ error: 'Falha ao baixar o vídeo' });
      }

      const fileContent = fs.readFileSync(filePath);

      const params = {
        Bucket: process.env.AWS_S3_BUCKET_NAME,
        Key: 'videos/video.mp4',
        Body: fileContent
      };

      try {
        await s3.upload(params).promise();
        const url = s3.getSignedUrl('getObject', {
          Bucket: process.env.AWS_S3_BUCKET_NAME,
          Key: 'videos/video.mp4',
          Expires: 3600
        });

        return res.status(200).json({ url });
      } catch (uploadError) {
        console.error('Erro no upload:', uploadError);
        return res.status(500).json({ error: 'Falha ao enviar para o S3' });
      }
    });
  } catch (err) {
    console.error('Erro geral:', err);
    return res.status(500).json({ error: 'Erro interno do servidor' });
  }
});

module.exports = router;