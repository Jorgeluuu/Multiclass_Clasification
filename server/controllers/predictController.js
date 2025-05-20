// controllers/predictController.js
const { spawn } = require('child_process');
const supabase = require('../database/connection_db_supabase');
// -----------------------------------------------------------------------------------------
const predict = (req, res) => {
  const inputData = req.body;
  const pythonPath = process.env.PYTHON_PATH || 'python';

  const python = spawn(pythonPath, ['model/predict.py', JSON.stringify(inputData)]);

  let result = '';

  python.stdout.on('data', (data) => { // ESTE NOMBRE SALE DE LA FAKE DATA EN MODELS.PY
    result += data.toString();
  });

  python.stderr.on('data', (data) => { // ESTE NOMBRE SALE DE LA FAKE DATA EN MODELS.PY
    console.error(`Error en Python: ${data}`);
  });

  python.on('close', async () => {
    const prediction = result.trim();

    try {
      // Guardamos en Supabase
      const { error } = await supabase
        .from('students')
        .insert([
          {
            age: inputData.age,
            education_years: inputData.education_years,
            credits_failed: inputData.credits_failed,
            target: prediction,
          },
        ]);

      if (error) throw error;

      res.json({ prediction, message: 'Guardado en Supabase ✅' });
    } catch (err) {
      console.error('⚠️ Error guardando en Supabase:', err);
      res.status(500).json({ error: '⚠️ Error guardando en Supabase' });
    }
  });
};


module.exports = { predict };
