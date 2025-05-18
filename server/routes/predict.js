// routes/predict.js
const express = require('express');
const { spawn } = require('child_process');
const router = express.Router();

router.post('/', (req, res) => {
  const inputData = req.body;

  const python = spawn('python', ['model/predict.py', JSON.stringify(inputData)]);

  let result = '';
  python.stdout.on('data', (data) => {
    result += data.toString();
  });

  python.stderr.on('data', (data) => {
    console.error(`Error en Python: ${data}`);
  });

  python.on('close', () => {
    res.json({ prediction: result.trim() });
  });
});

module.exports = router;
