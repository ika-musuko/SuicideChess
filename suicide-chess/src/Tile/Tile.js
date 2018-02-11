import React, {Component} from 'react';
import './Tile.css'

class tile extends Component {
    constructor(props) {
        super(props)
        this.state = {
            x: props.x,
            y: props.y,
        }
    }

    tileClick = () => {
        console.log(this.state.x + "," + this.state.y)
    }

    render () {

        return (
            <button onClick={this.tileClick}></button>
        )
    }

}

export default tile