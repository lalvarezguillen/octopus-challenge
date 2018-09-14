import React, { Component } from 'react';
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import './App.css';
import LandingPage from './views/Landing'

class App extends Component {
  render() {
    return (
      <HashRouter>
        <div>
        <h1>SendGrid</h1>
        <ul className="header">
          <li><NavLink to="/">Home</NavLink></li>
          <li><NavLink to="/admin">Admin</NavLink></li>
        </ul>
        <div className="content">
          <Route exact path="/" component={LandingPage}/>
        </div>
      </div>
      </HashRouter>
    );
  }
}

export default App;
