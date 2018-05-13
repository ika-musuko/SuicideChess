import React, { Component } from 'react'


class knight extends Component {

    render() {
        const selectedStyle = {
            filter: 'opacity(60%)'
        }
        const src = (this.props.pieceKey === "black_knightA" || this.props.pieceKey === "black_knightB") ? require('../assets/black_knight.png') : require('../assets/white_knight.png')
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

export default knight