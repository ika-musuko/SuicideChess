import React, { Component } from 'react'


class queen extends Component {

    render() {
        const selectedStyle = {
            filter: 'opacity(60%)'
        }
        return (
            <img 
            onClick={this.props.click} 
            src={require('../assets/black_queen.png')} 
            alt={this.key}
            style={this.props.selected ? selectedStyle : null }/>
        )
    }
}

export default queen