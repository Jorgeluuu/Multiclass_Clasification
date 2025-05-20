// index.js
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config(); // Loading environment variables from .env file
const predictRoute = require('./routes/predict'); // Importing the prediction route

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());

// Informative message
app.get('/', (req, res) => {
  res.send('🧠 API de Predicción - Servidor funcionando. Usa POST en /predict para obtener predicciones.');
});

// Routes
app.use('/predict', predictRoute);

app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://localhost:${PORT}`);
});
