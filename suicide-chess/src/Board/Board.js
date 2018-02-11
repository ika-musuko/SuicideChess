import React, { Component } from 'react'
import './Board.css'
import Tile from '../Tile/Tile'

class board extends Component {
    render () {
        let squares = []
        for(let i = 0; i < 8; i++ ) {
            for (let j = 0; j < 8; j++) {
                let color = false;
                if((i + j) % 2 === 0) {
                    color = true;
                }
                squares.push(<Tile x={j} y={i} key={i+10*j} color={color}/>)
            }
        }
        return (
            <div className="Board">
                {squares}
            </div>
        );
    }
}

export default board;