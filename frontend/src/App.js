import axios from 'axios';
import React from 'react';

class App extends React.Component {

  state = {details : [], }

  componentDidMount() {
    let data;
    axios.get('http://localhost:8000')
    .then(res => {
      data = res.data;
      this.setState({
        details: data
      });
    })
    .catch(err => { ' oopies ' })
  }

  render() {
    return (
      <div>
        <header>The Bird Engine</header>
        <hr></hr>
        {this.state.details.map((output, id) => (
          <div key = {id}>
            <div>
              <h2>Employee: {output.employee}</h2>
              <h3>Department: {output.department}</h3>
            </div>
          </div>
        ))}
      </div>
    )
  }

}


export default App;
