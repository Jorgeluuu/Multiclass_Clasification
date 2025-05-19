// routes/predict.js
const express = require('express');
const router = express.Router();
const { predict } = require('../controllers/predictController');

// Ruta POST para hacer predicciones
router.post('/', predict);

// (Opcional) Ruta GET por ID para pruebas o futura lógica
router.get('/:id', (req, res) => {
  const studentId = req.params.id;
  // Lógica de prueba por ahora
  res.json({ message: `Datos del estudiante con ID: ${studentId}` });
});

module.exports = router;
