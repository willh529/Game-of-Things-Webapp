import React, { Component } from 'react'
import { Button } from 'semantic-ui-react'
import { Link } from 'react-router-dom'
import axios from 'axios'

import styles from './Home.scss'

class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {title: "", startup: ""};
    }

    componentDidMount() {
        var self = this;
        axios.get('http://localhost:5000/')
            .then(function (response) {
                self.setState({title: response.data.title,
                    startup: response.data.startup})
            })
            .catch(function (error) {
                console.log(error)
            });

    }

    render() {
        return(
            <div className="Home">
                <h1>{this.state.title}</h1>
                <h4>{this.state.startup}</h4>
                <Link to="/start"><Button content="Setup game"/></Link>
                <Link to="/add"><Button content="Add a question"/></Link>
            </div>
        )
    }
}

export default Home
