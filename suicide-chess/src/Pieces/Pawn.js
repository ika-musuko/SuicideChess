import React, { Component } from 'react'


class pawn extends Component {

    render() {
        const selectedStyle = {
            filter: 'opacity(60%)'
        }

        const src = (
        this.props.pieceKey === "black_pawnA" ||
        this.props.pieceKey === "black_pawnB" ||
        this.props.pieceKey === "black_pawnC" ||
        this.props.pieceKey === "black_pawnD" ||
        this.props.pieceKey === "black_pawnE" ||
        this.props.pieceKey === "black_pawnF" ||
        this.props.pieceKey === "black_pawnG" ||
        this.props.pieceKey === "black_pawnH") ? 
        require('../assets/black_pawn.png') : require('../assets/white_pawn.png')

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

export default pawn