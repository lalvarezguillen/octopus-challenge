import React from 'react';
import Axios from 'axios';
import ReactWordCloud from 'react-wordcloud';
import 'regenerator-runtime/runtime';
import { ClipLoader, PacmanLoader } from 'react-spinners';
import Alert from 'react-s-alert';


class LandingPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tokens: [],
      feedback: {
        url: ''
      },
      loading: false,
    }
    this.urlInput = React.createRef();
    this.handleOnChange = this.handleOnChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.waitForAnalysis = this.waitForAnalysis.bind(this);
    this.requestAnalysis = this.requestAnalysis.bind(this);
    this.alertError = this.alertError.bind(this);
  }

  async handleSubmit(event) {
    this.setState({ loading: true });
    event.preventDefault();
    let taskId;
    try {
      taskId = await this.requestAnalysis();
    } catch (err) {
      console.error(err);
      this.setState({ loading: false });
      if (err.response.status == 400) {
        let msg = "The URL you provided appears to be invalid. Please include the URL's protocol";
        return this.alertError(msg);
      }
      let msg = `There was an error while submitting your request (code ${err.response.status})`;
      return this.alertError(msg);
    }
    await this.waitForAnalysis(taskId);
  }

  async requestAnalysis() {
    console.log("Requesting analysis")
    const url = '/task/';
    const payload = { url: this.urlInput.current.value };
    let resp;
    resp = await Axios.post(url, payload)
    return resp.data.id;
  }

  alertError(msg) {
    Alert.error(msg, { position: 'bottom' })
  }

  async waitForAnalysis(analysisId) {
    console.log('waiting for analysis')
    const url = `/task/${analysisId}`;
    let resp;
    try {
      resp = await Axios.get(url);
    } catch (err) {
      console.error(err);
      this.setState({ loading: false });
      let msg = `There was a problem fetching your results (code ${err.response.status}`
      return this.alertError(msg)
    }
    if (resp.status == 200) {
      return this.setState({ tokens: resp.data, loading: false })
    }
    if (resp.status == 204) {
      setTimeout(() => this.waitForAnalysis(analysisId), 2000);
    }
  }

  handleOnChange(event) {
    this.setState({
      value: event.target.value,
      feedback: {},
    });
  }

  render() {
    return (
      <div>
        <div className='g-mb-70'>
          <form className="g-brd-around g-brd-gray-light-v4 g-pa-30 g-mb-30" onSubmit={this.handleSubmit}>
            <div className="row justify-content-center text-center">
              <div className="col-lg-5">
                <div className="input-group g-brd-primary--focus">
                  <input type="text"
                    className="form-control form-control-md rounded-0 "
                    ref={this.urlInput}
                    placeholder="Paste here a website's full URL to get its content analyzed"
                  />
                </div>
              </div>
              <button className="btn btn-md u-btn-black" type="submit" disabled={this.state.loading}>
                Analyze!
                      </button>
            </div>
          </form>
        </div>
        {this.state.loading ?
          <div className='d-flex justify-content-center'>
            <PacmanLoader
              loading={true}
              color="#000"
            />
          </div> :
          <TokensCloud
            tokens={this.state.tokens}
          />
        }
      </div>
    )
  }
}

class TokensCloud extends React.Component {
  constructor(props) {
    super(props);
  }


  render() {
    return (
      <div>
        <ReactWordCloud
          words={this.props.tokens}
          wordCountKey="frequency"
          wordKey="token"
        />
      </div>
    )
  }
}

export default LandingPage;