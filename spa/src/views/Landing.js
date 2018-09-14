import React from 'react';
import Axios from 'axios';
import ReactWordCloud from 'react-wordcloud';


class LandingPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: '',
            tokens: [],
            feedback: {
                value: ''
            },
        }
        this.handleOnChange = this.handleOnChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.waitForAnalysis = this.waitForAnalysis.bind(this);
        this.requestAnalysis = this.requestAnalysis.bind(this);
    }

    async handleSubmit(event) {
      console.log("submitting")
        event.preventDefault();
        let taskId;
        try {
          taskId = await this.requestAnalysis();
        } catch(err) {
          console.error(err);
          return
        }
        this.waitForAnalysis(taskId);
    }

    async requestAnalysis() {
      console.log("Requesting analysis")
      const url = 'http://localhost:3000/task/';
      const payload = {url: this.state.value};
      let resp;
      resp = await Axios.post(url, payload)
      return resp.data.id;
    }

    async waitForAnalysis(analysisId) {
      console.log('waiting for analysis')
      const url = `http://localhost:3000/task/${analysisId}`;
      let resp;
      try {
        resp = await Axios.get(url);
      } catch(err) {
        console.error(err);
        return
      }
      if(resp.status == 200) {
        this.setState({tokens: resp.data})
        return
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
                <div>
                    <form onSubmit={this.handleSubmit}>
                        <input
                          type="text"
                          value={this.state.value}
                          onChange={(ev) => this.handleOnChange(ev)}
                          placeholder="Submit a website's URL to get its content analyzed"
                        />
                        <button type="submit">Analyze!</button>
                    </form>
                </div>
                <TokensCloud
                  tokens={this.state.tokens}
                />
            </div>
        )
    }
}

class TokensCloud extends React.Component {
  constructor(props) {
    super(props);
    // this.state = {
    //   tokens: this.props.tokens,
    // }
  }
  render(){
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