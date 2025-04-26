const express = require('express');
const bodyParser = require('body-parser');
const analyzeRoute = require('./analyze');

const app = express();
app.use(bodyParser.json());
app.use('/api', analyzeRoute);

app.get('/', (req, res) => {
  res.send('GPT Video Processor v2 - Node Version');
});

module.exports = app;