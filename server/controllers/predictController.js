// controllers/predictController.js
const { spawn } = require('child_process');

const predict = (req, res) => {
  const inputData = req.body;
  const pythonPath = process.env.PYTHON_PATH || 'python';

  const python = spawn(pythonPath, ['model/predict.py', JSON.stringify(inputData)]);

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
};

module.exports = { predict };
