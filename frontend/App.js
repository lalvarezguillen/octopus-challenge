/* Entrypoint for the Single Page Application */
import React, { Component } from 'react';
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink as NavLinkBS,
} from 'reactstrap';
import Alert from 'react-s-alert';
import './App.css';
import LandingPage from './views/Landing'
import AdminPage from './views/Admin'

class App extends Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.state = {
      isOpen: false
    };
  }
  toggle() {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }
  render() {
    return (
      <HashRouter>
        <div>
          <Alert />
          <header
            id="js-header"
            className="u-header u-header--sticky-top u-header--toggle-section u-header--change-appearance"
            data-header-fix-moment="300"
          >
            <div
              className="u-header__section u-header__section--dark g-bg-black g-transition-0_3 g-py-10"
              data-header-fix-moment-exclude="g-py-10"
              data-header-fix-moment-classes="g-py-0"
            >
              <nav className="navbar navbar-expand-lg">
                <div className="container">
                  <button
                    className="navbar-toggler navbar-toggler-right btn g-line-height-1 g-brd-none g-pa-0 g-pos-abs g-top-3 g-right-0"
                    type="button"
                    aria-label="Toggle navigation"
                    aria-expanded="false"
                    aria-controls="navBar"
                    data-toggle="collapse"
                    data-target="#navBar"
                  >
                    <span className="hamburger hamburger--slider">
                      <span className="hamburger-box">
                        <span className="hamburger-inner"></span>
                      </span>
                    </span>
                  </button>

                  <NavLink className="navbar-brand" to="/">Octopus Challenge</NavLink>

                  <div
                    className="collapse navbar-collapse align-items-center flex-sm-row g-pt-10 g-pt-5--lg"
                    id="navBar"
                  >
                    <ul className="navbar-nav text-uppercase g-font-weight-600 ml-auto">
                      <li className="nav-item g-mx-20--lg">
                        <NavLink className="nav-link px-0" to="/">Home</NavLink>
                      </li>
                      <li className="nav-item g-mx-20--lg">
                        <NavLink className="nav-link px-0" to="/admin">Admin</NavLink>
                      </li>
                    </ul>
                  </div>
                </div>
              </nav>
            </div>
          </header>
          <section className="container g-mt-150">
            <Route exact path="/" component={LandingPage} />
            <Route path="/admin" component={AdminPage} />
          </section>
        </div>
      </HashRouter>
    );
  }
}

export default App;
