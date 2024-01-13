import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App'

const root = ReactDOM.createRoot(document.getElementById('root'));

export const API_URL = "http://127.0.0.1:8000/api/"
export const SONG_LIST_URL = API_URL + "songs/"
export const PREDICT_URL = API_URL + "predict/"

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
