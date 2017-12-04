import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import { Form, Button, Input } from 'semantic-ui-react'
import { Link } from 'react-router-dom'
import { withRouter } from 'react-router-dom'
import axios from 'axios'


import styles from './Score.scss'

class Score extends Component {
    constructor(props) {
        super(props);
        this.state = { scores: [], winner: "" };
    }

    componentDidMount() {
        var self = this;
        axios.get('http://localhost:5000/score')
            .then(function (response) {
                self.setState({scores: response.data.scores, winner: response.data.winner })
            })
            .catch(function (error) {
                console.log(error)
            });
    }

    render() {
        return(
            <div className="Score">
                <h2>{this.state.winner} wins!</h2>
                <h3>{this.state.scores.join(", ")}</h3>
                <Link to="/start"><Button content="New game"/></Link>
            </div>
        )
    }
}

export default withRouter(Score)
