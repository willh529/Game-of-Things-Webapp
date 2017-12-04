import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import { Form, Button, Input } from 'semantic-ui-react'
import { Link } from 'react-router-dom'
import { withRouter } from 'react-router-dom'
import axios from 'axios'


import styles from './Question.scss'

class Question extends Component {
    constructor(props) {
        super(props);
        this.state = { question: "",  players: [], answer: "", playerIndex: 0};
        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(e) {
        e.preventDefault();
        this.setState({[e.target.name]: e.target.value})
    }

    handleSubmit(e) {
        var self = this;
        e.preventDefault();
        document.getElementById("answer").reset();
        axios.post("http://localhost:5000/question", {
            player: self.state.players[self.state.playerIndex],
            answer: self.state.answer
            })
            .then(function (response) {
                self.state.playerIndex++;
                if(self.state.playerIndex == self.state.players.length) {
                    self.props.history.push("/game");
                }
            })
            .catch(function (error) {
                console.log(error)
            });
    }

    componentDidMount() {
        var self = this;
        axios.get('http://localhost:5000/question')
            .then(function (response) {
                self.setState({question: response.data.question, players: response.data.players})
            })
            .catch(function (error) {
                console.log(error)
            });
    }

    render() {
        return(
            <div className="Question">
                <h3>{this.state.question}</h3>
                <h4>Enter your answer, {this.state.players[this.state.playerIndex]}.</h4>
                <Form id="answer" onSubmit={this.handleSubmit}>
                    <Form.Field>
                        <Input placeholder="Answer" name="answer" onChange={this.handleChange}/>
                    </Form.Field>
                    <Button type="submit" content="Submit" />
                </Form>
            </div>
        )
    }
}

export default withRouter(Question)
