import React, { Component } from 'react'
import { Form, Button, Input } from 'semantic-ui-react'
import { Link } from 'react-router-dom'
import { withRouter } from 'react-router'
import axios from 'axios'


import styles from './Add.scss'

class Add extends Component {
    constructor(props) {
        super(props);
        this.state = { question: "" };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(e) {
        e.preventDefault();
        this.setState({[e.target.name]: e.target.value});
    }

    handleSubmit(e) {
        var self = this;
        e.preventDefault();
        axios.post("http://localhost:5000/add", {
            question: self.state.question
        })
            .then(function (response) {
                self.props.history.push("/");
            })
            .catch(function (error) {
                console.log(error)
            });
    }

    render() {
        return(
            <div className="Add">
                <h4>Enter a question.</h4>
                <Form onSubmit={this.handleSubmit}>
                    <Form.Field>
                        <Input placeholder="Enter your question" name="question" onChange={this.handleChange}/>
                    </Form.Field>
                    <Button type="submit" content="Submit" />
                </Form>
            </div>
        )
    }
}

export default withRouter(Add)
