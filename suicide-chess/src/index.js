import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';

var container = document.getElementById('gameRoot');
ReactDOM.render(<App roomID={container.getAttribute('roomID')}/>, container);
registerServiceWorker();
