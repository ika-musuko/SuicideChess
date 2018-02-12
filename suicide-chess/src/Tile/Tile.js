import React, {Component} from 'react';
import './Tile.css'

class tile extends Component {

    render () {
        return (
            this.props.color? (
                <button className="white-tile" onClick={this.props.click}>
                    {this.props.children}
                </button>
            ) : (
                <button className="grey-tile" onClick={this.props.click}>
                    {this.props.children}
                </button>
            )
        )
    }

}

export default tile