import React, { Component } from 'react'
import { Form, Button, Input } from 'semantic-ui-react'
import { Link } from 'react-router-dom'
import { withRouter } from 'react-router'
import axios from 'axios'


import styles from './Setup.scss'

class Setup extends Component {
    constructor(props) {
        super(props);
        this.state = { points: 0, players: "", playersText: "", pointsText: "", success: ""};
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    componentDidMount() {
        var self = this;
        axios.get("http://localhost:5000/")
            .then(function (response) {
                self.setState({playersText: response.data.players,
                    pointsText: response.data.points});
            })
            .catch(function (error) {
                console.log(error);
            });

    }

    handleChange(e) {
        e.preventDefault();
        this.setState({[e.target.name]: e.target.value})
    }

    handleSubmit(e) {
        var self = this;
        e.preventDefault();
        axios.post("http://localhost:5000/start", {
            points: parseInt(self.state.points),
            players: self.state.players.split(", ")
            })
            .then(function (response) {
                self.props.history.push("/question");
            })
            .catch(function (error) {
                console.log(error)
            });
    }

    render() {
        return(
            <div className="Setup">
                <h5>{this.state.pointsText}</h5>
                <h5>{this.state.playersText}</h5>
                <Form onSubmit={this.handleSubmit}>
                    <Form.Field>
                        <Input placeholder="Point Limit" name="points" onChange={this.handleChange}/>
                    </Form.Field>
                    <Form.Field>
                        <Input placeholder="Player Names" name="players" onChange={this.handleChange}/>
                    </Form.Field>
                    <Button type="submit" content="Submit" />
                </Form>
            </div>
        )
    }
}

export default withRouter(Setup)
