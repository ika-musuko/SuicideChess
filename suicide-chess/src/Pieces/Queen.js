import React, { Component } from 'react'


class queen extends Component {

    render() {
        const selectedStyle = {
            filter: 'opacity(60%)'
        }

        const src = this.props.pieceKey === "Black_Queen" ? require('../assets/black_queen.png') : require('../assets/white_queen.png')

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

export default queen