import React, { Component } from 'react'
import { Form, Button, Input } from 'semantic-ui-react'
import { Link } from 'react-router-dom'
import { withRouter } from 'react-router-dom'
import axios from 'axios'


import styles from './Game.scss'

class Game extends Component {
    constructor(props) {
        super(props);
        this.state = { answers: [], players: [], playerIndex: 0, currAnswer: "", currGuessee: "", successful: "" };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    componentDidMount() {
        var self = this;
        axios.get('http://localhost:5000/guess')
            .then(function (response) {
                self.setState({answers: response.data.answers,
                    players: response.data.players });
            })
            .catch(function (error) {
                console.log(error)
            });

    }

    handleChange(e) {
        e.preventDefault();
        this.setState({[e.target.name]: e.target.value})
    }

    handleSubmit(e) {
        e.preventDefault();
        var self = this;
        e.preventDefault();
        document.getElementById("guess").reset();
        axios.post("http://localhost:5000/guess", {
            guesser: self.state.players[self.state.playerIndex],
            guessee: self.state.guessee,
            answer: self.state.answer
        })
            .then(function (response) {
                self.state.successful = response.data.status;
                console.log(response.data.status);
                self.state.players = response.data.players;
                self.state.answers = response.data.answers;
                self.state.playerIndex++;
                if(self.state.successful == "Time for a new question") {
                    self.props.history.push("/question");
                }
                if(self.state.playerIndex == self.state.players.length) {
                    self.state.playerIndex = 0;
                }
            })
            .catch(function (error) {
                console.log(error)
            });
    }

    render() {
        return(
            <div className="Game">
                <h4>Players: {this.state.players.join(", ")}</h4>
                <h4>Answers: {this.state.answers.join(", ")}</h4>
                <h4>{this.state.players[this.state.playerIndex]}'s turn.</h4>
                <Form id="guess" onSubmit={this.handleSubmit}>
                    <Form.Field>
                        <Input placeholder="Who do you guess?" name="guessee" onChange={this.handleChange}/>
                    </Form.Field>
                    <Form.Field>
                        <Input placeholder="Answer" name="answer" onChange={this.handleChange}/>
                    </Form.Field>
                    <Button type="submit" content="Submit" />
                    <Link to="/score"><Button content="End game"/></Link>
                </Form>
                <h4>{this.state.successful}</h4>
            </div>
        )
    }
}

export default withRouter(Game)
