import axios from 'axios';
import  React  from "react";
import "./App.css";
import { SearchBar } from './Components/SearchBar';

class App extends React.Component {

  state = {details : [], }

  componentDidMount() {
    let data;
    axios.get('http://127.0.0.1:8000/api/')
    .then(res => {
      data = res.data;
      this.setState({
        details: data
      })
      console.log(res.data);
    })
    .catch(err => { ' oopies ' })
  }

  render() {
    return (
      <div className='App'> 
        <header>The Bird Engine</header>
        <div className='search-bar-container'>
          <SearchBar />
          <div>Search Results</div>
        </div>

      </div>
    )
  }

}


export default App;
