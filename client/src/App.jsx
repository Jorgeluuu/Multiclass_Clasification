import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import Layout from './layout/layout';
import AppRoutes from './routes/Routes';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <AppRoutes />
      </Layout>
    </BrowserRouter>
  );
}

export default App;