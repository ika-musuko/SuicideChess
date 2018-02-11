import React, { Component } from 'react'
import Board from '../Board/Board'
import './Gamescene.css'

class gamescene extends Component {
    render() {
      return (
        <div className="Gamescene"> 
          <Board />
        </div>
      );
    }
  }

export default gamescene;