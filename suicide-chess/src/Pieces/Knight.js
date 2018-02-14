import React, { Component } from 'react'


class knight extends Component {

    render() {
        const selectedStyle = {
            filter: 'opacity(60%)'
        }
        return (
            <img 
            className="piece"
            onClick={this.props.click} 
            src={require('../assets/black_knight.png')} 
            alt={this.key} 
            style={this.props.selected ? selectedStyle : null }/>
        )
    }
}

export default knight