import React, {Component} from 'react';
import './Tile.css'

class tile extends Component {

    render () {
        return (
            this.props.requiredMove ? (
              <div
              className="required-tile"
              onClick={this.props.click}
              >
                  {this.props.children}
              </div>
            ) : this.props.color ? (
              <div
              className="white-tile"
              onClick={(this.props.click)}
              >
                  {this.props.children}
              </div>
            ) : (
              <div
              className="grey-tile"
              onClick={this.props.click}
              >
                  {this.props.children}
              </div>
            )
        )
    }

}

export default tile
