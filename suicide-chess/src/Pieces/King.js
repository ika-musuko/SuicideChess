import React, { Component } from 'react'


class king extends Component {

    render() {
        const selectedStyle = {
            filter: 'opacity(60%)'
        }

        const src = this.props.pieceKey === "Black_King" ? require('../assets/black_king.png') : require('../assets/white_king.png')

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

export default king