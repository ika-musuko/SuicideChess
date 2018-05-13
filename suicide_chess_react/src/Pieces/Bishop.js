import React, { Component } from 'react'


class bishop extends Component {

    render() {
        const selectedStyle = {
            filter: 'opacity(60%)'
        }
        const src = (this.props.pieceKey === "black_bishopA" || this.props.pieceKey === "black_bishopB") ? 
        require('../assets/black_bishop.png') : require('../assets/white_bishop.png')
        return (
            <img 
            className="piece"
            onClick={this.props.click} 
            src={src} 
            alt={this.props.pieceKey} 
            style={this.props.selected ? selectedStyle : null }/>
        )
    }
}

export default bishop