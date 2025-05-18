// index.js
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const predictRoute = require('./routes/predict');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());

// Rutas
app.use('/predict', predictRoute);

app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://localhost:${PORT}`);
});
