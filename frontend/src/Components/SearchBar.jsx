import  React, {useState} from 'react';
import {FaSearch, fasearch} from 'react-icons/fa';
import './SearchBar.css';
import axios from 'axios';



export const SearchBar = () => {
    const [input, setInput] = useState("")

    const sendQuery = async() => {
        alert(input)
        let csrfToken = document.head.querySelector('meta[name="csrf-token"]');
        const response = await axios.post("http://127.0.0.1:8000/api/create/", {
            text_query : input
        })
        .then((response) => {
            console.log(response)
        })
        .catch(function (error) {
            console.log(error);
        });
       
        
    
    }
    return (
        <div className='input-wrapper'>

            <FaSearch id= 'search-icon' />
            <input placeholder='What is the bird in question?' 
            style={{width: "700px"}} 
            value={input} 
            onChange={(e) => setInput(e.target.value)}/>
            <button onClick={sendQuery}>Search</button>
        </div>
        

    )
}


