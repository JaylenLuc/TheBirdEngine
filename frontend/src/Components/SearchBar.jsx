import  React, {useState, useRef} from 'react';
import {FaSearch, fasearch} from 'react-icons/fa';
import './SearchBar.css';
import axios from 'axios';
//import { Link } from 'react-router-dom';


export const SearchBar = () => {
    const res_tab = document.getElementById("results_tab");
    const [input, setInput] = useState("")

    const sendQuery = async() => {
        alert(input)
        let csrfToken = document.head.querySelector('meta[name="csrf-token"]');
        const response = await axios.post("http://127.0.0.1:8000/api/create/", {
            text_query : input
        })
        .then((response) => {
            let data = response.data;
            console.log(response.data)
            res_tab.innerHTML  = ""
            let res_string = ""
            for (let i = 0; i < data.length; i++){
               res_string = res_string +  data[i] + "<br></br>";

            }
            res_tab.innerHTML = res_string


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
            
            <div id='results_tab'></div>
        </div>
            

    )
}


