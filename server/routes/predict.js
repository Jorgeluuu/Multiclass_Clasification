// routes/predict.js
const express = require('express');
const router = express.Router();
const { predict } = require('../controllers/predictController');

// Route POST to predict
router.post('/', predict);

// ROUTE to introduce new student
router.post('/new', (req, res) => {
  const newStudent = req.body;
  // THIS MUST BE REPLACE WITH CORRECT LOGIC !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  res.json({ message: 'Nuevo estudiante creado', student: newStudent });
});

// Route GET to predict
router.get('/', (req, res) => {
  res.json({ message: 'GET request to the predict endpoint' });
});

// Route GET per id
router.get('/:id', (req, res) => {
  const studentId = req.params.id;
  // THIS MUST BE REPLACE WITH CORRECT LOGIC !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  res.json({ message: `Datos del estudiante con ID: ${studentId}` });
});

module.exports = router;
