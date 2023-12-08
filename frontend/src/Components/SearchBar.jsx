import  React, {useState, useRef} from 'react';
import {FaSearch, fasearch} from 'react-icons/fa';
import './SearchBar.css';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Links from './search_results'
var link_param = []
export const SearchBar = () => {
    //var res_tab = document.getElementById("results_tab");
    const [input, setInput] = useState("")
    const [Resultants, setState] = React.useState(link_param);
    //res_tab.innerHTML  = "Search Results: "
    const sendQuery = async() => {
        alert(input)
        let csrfToken = document.head.querySelector('meta[name="csrf-token"]');
        const response = await axios.post("http://127.0.0.1:8000/api/create/", {
            text_query : input
        })
        .then((response) => {
            let data = response.data;
            console.log(response.data)
            //res_tab.innerHTML  = "Search Results: "
            //let res_string = ""
            console.log("here")
            
            link_param = []
            for (let i = 0; i < data.length; i++){
               
               link_param.push(data[i])

            }
            setState(link_param);
            //console.log(link_param[1])
        })
        .catch(function (error) {
            console.log(error);
        });
       
        
    
    }
    return (
        <div>
            <div className='input-wrapper'>

                <FaSearch id= 'search-icon' />
                <input placeholder='What is the bird in question?' 
                style={{width: "800px"}} 
                value={input} 
                onChange={(e) => setInput(e.target.value)}/>
                <button onClick={sendQuery}>Search</button>
            </div>
            
            <ul>{Resultants.map((item) => (
                 <li key = {item}><a href={item}>{item}</a></li>
            ))}</ul>

        </div>
  

    )
}


