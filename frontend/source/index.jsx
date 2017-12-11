import React from 'react';
import {render} from 'react-dom';
import {browserHistory, BrowserRouter as Router, Route, Link} from 'react-router-dom'
import 'semantic-ui-css/semantic.min.css';

// Include your new Components here
import Home from './components/Home/Home.jsx';
import Setup from './components/Setup/Setup.jsx';
import Question from './components/Question/Question.jsx';
import Game from './components/Game/Game.jsx';
import Score from './components/Score/Score.jsx';
import Add from './components/Add/Add.jsx';

// Include any new stylesheets here
// Note that components' stylesheets should NOT be included here.
// They should be 'require'd in their component class file.
require('./styles/main.scss');

render(
    (<Router>
        <div>
            <Route exact path="/" component = {Home}/>
            <Route exact path="/start" component = {Setup}/>
            <Route exact path="/question" component={Question}/>
            <Route exact path="/game" component={Game}/>
            <Route exact path="/score" component={Score}/>
            <Route exact path="/add" component={Add}/>
        </div>
    </Router>),
    // Define your router and replace <Home /> with it!
    document.getElementById('app')
);
