import React, {Component} from 'react';
import './Tile.css'

class tile extends Component {
    constructor(props) {
        super(props)
        this.state = {
            x: props.x,
            y: props.y,
            selected: false,
            color: props.color,
        }
    }

    toggleSelected = () => {
        this.setState({
            selected: !this.state.selected,
        })
    }

    tileClick = () => {
        this.setState({
            selected: !this.state.selected,
        })
    }

    render () {
        return (
            this.state.color? (
                <button className="white-tile" onClick={this.tileClick}></button>
            ) : (
                <button className="grey-tile" onClick={this.tileClick}></button>
            )
        )
    }

}

export default tile