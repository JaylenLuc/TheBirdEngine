import  React, {useState, useRef} from 'react';
import {FaSearch, fasearch} from 'react-icons/fa';
import './SearchBar.css';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { render } from '@testing-library/react';

export default function Links({all_links}) {
    console.log(all_links[1]);
	return (
		<div>
            {all_links.map((link) => <li><a href={link}>{link}</a></li>)}
		</div>
	)
};

