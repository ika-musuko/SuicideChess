import React, { Component } from 'react'
import Gamescene from './Gamescene/Gamescene'
import './App.css'

class App extends Component {
  render() {
    return (
      <div className="App">
        <Gamescene roomID={this.props.roomID} user={this.props.user}/>
      </div>
    );
  }
}

export default App;
