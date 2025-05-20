import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Prediction from '../pages/Prediction';
import Monitoring from '../pages/Monitoring';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Prediction />} />
      <Route path="/monitoring" element={<Monitoring />} />
      <Route path="*" element={<div>Not Found</div>} />
    </Routes>
  );
};

export default AppRoutes;
