import React, { Component } from 'react'


class knight extends Component {

    render() {
        const selectedStyle = {
            filter: 'opacity(60%)'
        }
        return (
            <img 
            onClick={this.props.click} 
            src={require('../assets/black_knight.png')} 
            alt="black_knight" 
            style={this.props.selected ? selectedStyle : null }/>
        )
    }
}

export default knight