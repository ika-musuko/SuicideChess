import React, { Component } from 'react'


class rook extends Component {

    render() {
        const selectedStyle = {
            filter: 'opacity(60%)'
        }
        const src = (this.props.pieceKey === "Black_RookA" || this.props.pieceKey === "Black_RookB") ? 
        require('../assets/black_rook.png') : require('../assets/white_rook.png')
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

export default rook