import React, { Component } from 'react'
import { Grid, Form, Button, Input, Dropdown } from 'semantic-ui-react'
import { Link } from 'react-router-dom'
import { withRouter } from 'react-router-dom'
import axios from 'axios'


import styles from './Game.scss'

class Game extends Component {
    constructor(props) {
        super(props);
        this.state = { answers: [], player_names: [], players: [], playerIndex: 0, answer: "", guessee: "", successful: "", error: "", scores: [] };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    componentDidMount() {
        var self = this;
        axios.all([
            axios.get("http://localhost:5000/guess"),
            axios.get("http://localhost:5000/score")
        ])
            .then(axios.spread(function (response, score) {
                self.setState({answers: response.data.answers,
                    players: response.data.players,
                    player_names: response.data.player_names,
                    error: response.data.error,
                    scores: score.data.scores});
            }))
            .catch(function (error) {
                console.log(error)
            });
    }

    handleChange(e, data) {
        e.preventDefault();
        this.setState({[data.name]: data.value});
    }

    handleSubmit(e) {
        e.preventDefault();
        var self = this;
        axios.post("http://localhost:5000/guess", {
            guesser: self.state.player_names[self.state.playerIndex],
            guessee: self.state.guessee,
            answer: self.state.answer
            })
            .then(function (response) {
                var oldName = self.state.player_names[self.state.playerIndex];
                self.setState({successful: response.data.status,
                    error: response.data.error,
                    player_names: response.data.player_names,
                    players: response.data.players,
                    answers: response.data.answers,
                    scores: response.data.scores});
                if(self.state.error == "Need to choose." || self.state.error == "Cannot guess yourself.") {
                    self.state.playerIndex = self.state.playerIndex;
                }
                else if(self.state.successful == "Score limit reached.") {
                    self.props.history.push("/score")
                }
                else if(self.state.successful == "Time for a new question." || self.state.player_names.length == 1) {
                    self.props.history.push("/question");
                }
                else if(self.state.successful == "Correct guess!") {
                    if(oldName == self.state.player_names[self.state.playerIndex - 1]) {
                        self.state.playerIndex--;
                    }
                }
                else if(self.state.playerIndex == self.state.player_names.length) {
                    self.state.playerIndex = 0;
                }
                else {
                    self.state.playerIndex++;
                }
            })
            .catch(function (error) {
                console.log(error)
            });
        document.getElementById("guess").reset();
        self.forceUpdate();
    }

    render() {
        return(
            <div className="Game">
                <h3>{this.state.player_names[this.state.playerIndex]}'s turn.</h3>
                <h3>Scores: {this.state.scores.join(", ")}</h3>
                <h4>Choose a player and answer to guess.</h4>
                <Form id="guess" onSubmit={this.handleSubmit}>
                    <Form.Field>
                        <Dropdown placeholder="Players" name="guessee" options={this.state.players} onChange={this.handleChange}/>
                    </Form.Field>
                    <Form.Field>
                        <Dropdown placeholder="Answers" name="answer" options={this.state.answers} onChange={this.handleChange}/>
                    </Form.Field>
                    <Button type="submit" content="Submit" />
                    <Link to="/score"><Button content="End game"/></Link>
                </Form>
                <h4>{this.state.successful}</h4>
                <h4>{this.state.error}</h4>
            </div>
        )
    }
}

export default withRouter(Game)
