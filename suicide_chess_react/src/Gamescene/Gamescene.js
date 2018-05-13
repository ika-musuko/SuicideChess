import React, { Component } from 'react'
import Board from '../Board/Board'
import './Gamescene.css'
import { observe } from '../Game'
import { pieceObserve } from '../Game'
import { getValidMoves } from '../Utilities/GetValidMoves'
import { movePiece } from '../Game'
import firebase from '../firebase'
import { getRequiredMoves } from '../Utilities/GetRequiredMoves'
import { setRequiredMoves, setPieces } from '../Game'

class gamescene extends Component {
  constructor(props) {
    super(props)
    this.state = {
      black_knightA: { x: -1, y: 0 },
      black_knightB: { x: -1, y: 0 },
      black_bishopA: { x: -1, y: 0 },
      black_bishopB: { x: -1, y: 0 },
      black_rookA: { x: -1, y: 0 },
      black_rookB: { x: -1, y: 0 },
      black_queen: { x: -1, y: 0 },
      black_king: { x: -1, y: 0 },
      black_pawnA: { x: -1, y: 1, firstMove: true },
      black_pawnB: { x: -1, y: 1, firstMove: true },
      black_pawnC: { x: -1, y: 1, firstMove: true },
      black_pawnD: { x: -1, y: 1, firstMove: true },
      black_pawnE: { x: -1, y: 1, firstMove: true },
      black_pawnF: { x: -1, y: 1, firstMove: true },
      black_pawnG: { x: -1, y: 1, firstMove: true },
      black_pawnH: { x: -1, y: 1, firstMove: true },

      white_knightA: { x: -1, y: 7 },
      white_knightB: { x: -1, y: 7 },
      white_bishopA: { x: -1, y: 7 },
      white_bishopB: { x: -1, y: 7 },
      white_rookA: { x: -1, y: 7 },
      white_rookB: { x: -1, y: 7 },
      white_queen: { x: -1, y: 7 },
      white_king: { x: -1, y: 7 },
      white_pawnA: { x: -1, y: 6, firstMove: true },
      white_pawnB: { x: -1, y: 6, firstMove: true },
      white_pawnC: { x: -1, y: 6, firstMove: true },
      white_pawnD: { x: -1, y: 6, firstMove: true },
      white_pawnE: { x: -1, y: 6, firstMove: true },
      white_pawnF: { x: -1, y: 6, firstMove: true },
      white_pawnG: { x: -1, y: 6, firstMove: true },
      white_pawnH: { x: -1, y: 6, firstMove: true },
      validTiles: [],
      requiredMoves: [],

      moveList:[],

      whiteTurn: true,

      whiteWin: false,

      blackWin: false,

      databaseRef: firebase.database().ref('/SuicideChess/' + this.props.roomID),

      rematchRoute: '/rematch/' + this.props.roomID,
      exitGameRoute: '/exit_game/' + this.propsroomID,

      submitted: false,

      isWhite: false,
      username: this.props.user,
      otherUser: '',
      roomID: this.props.roomID,

      selectedPiece: null
    }
    observe(this.handlePieceMove.bind(this))
    pieceObserve(this.handlePieceSelect.bind(this))

    this.handleFormChange = this.handleFormChange.bind(this);
    this.handleSelectButton = this.handleSelectButton.bind(this);
  };

  componentDidMount() {
    /*this.setState({
      white_knightA: { x: -1, y: 7 },
      white_knightB: { x: -1, y: 7 },
      white_bishopA: { x: -1, y: 7 },
      white_bishopB: { x: -1, y: 7 },
      white_rookA: { x: -1, y: 7 },
      white_rookB: { x: -1, y: 7 },
      white_queen: { x: -1, y: 7 },
      white_king: { x: -1, y: 7 },
      white_pawnA: { x: -1, y: 6, firstMove: true },
      white_pawnB: { x: -1, y: 6, firstMove: true },
      white_pawnC: { x: -1, y: 6, firstMove: true },
      white_pawnD: { x: -1, y: 6, firstMove: true },
      white_pawnE: { x: -1, y: 6, firstMove: true },
      white_pawnF: { x: -1, y: 6, firstMove: true },
      white_pawnG: { x: -1, y: 6, firstMove: true },
    })*/
    let a = this;
    this.state.databaseRef.once('value').then(function(snapshot) {
      var room = snapshot.val();
      if(room['players'][0] === a.state.username) {

        var gameData = room['gameData']

        var winner = room['winner']
        
        if(winner === a.state.username) {
          a.setState({
            ...gameData,
            whiteTurn: gameData['whiteTurn'],
            username: a.state.username,
            otherUser: room['players'][1],
            moveList: room['moveList'],
            submitted: true,
            isWhite: true,
            whiteWin: true,
          });
        } else if (winner === room['players'][1]) {
          a.setState({
            ...gameData,
            whiteTurn: gameData['whiteTurn'],
            username: a.state.username,
            otherUser: room['players'][1],
            moveList: room['moveList'],
            submitted: true,
            isWhite: true,
            blackWin: true,
          });
        }

        a.setState({
          ...gameData,
          whiteTurn: gameData['whiteTurn'],
          username: a.state.username,
          otherUser: room['players'][1],
          moveList: room['moveList'],
          submitted: true,
          isWhite: true,
        });
        a.updateStateAfterDatabaseSync()
      } else if (room['players'][1] === a.state.username) {

        var gameData = room['gameData']
        var winner = room['winner']
        if(winner === a.state.username) {
          a.setState({
            ...gameData,
            whiteTurn: gameData['whiteTurn'],
            username: a.state.username,
            otherUser: room['players'][0],
            moveList: room['moveList'],
            submitted: true,
            isWhite: false,
            blackWin: true,
          })
        } else if (winner === room['players'][0]) {
          a.setState({
            ...gameData,
            whiteTurn: gameData['whiteTurn'],
            username: a.state.username,
            otherUser: room['players'][0],
            moveList: room['moveList'],
            submitted: true,
            isWhite: false,
            whiteWin: true,
          })
        }

        a.setState({
          ...gameData,
          whiteTurn: gameData['whiteTurn'],
          username: a.state.username,
          otherUser: room['players'][0],
          moveList: room['moveList'],
          submitted: true,
          isWhite: false
        })
        a.updateStateAfterDatabaseSync()
      }
    })
  }

  updateStateAfterDatabaseSync = () => {
    var newGameData = new Object();

    for(var piece in this.state) {
      if(this.state.hasOwnProperty(piece) && (piece.substring(0,6) === "black_" || piece.substring(0,6) === "white_")){
        newGameData[piece] = this.state[piece]
      }
    }
    newGameData['whiteTurn'] = this.state.whiteTurn
    setPieces(newGameData, newGameData['whiteTurn']);

    let requiredMoves = [];
    if(newGameData['whiteTurn']) {
      requiredMoves = getRequiredMoves(newGameData, true);
    } else {
      requiredMoves = getRequiredMoves(newGameData, false);
    }

    var gameListener = firebase.database().ref('/SuicideChess/' + this.state.roomID + '/gameData/');
    gameListener.on('child_changed', function(snapshot) {
      if(snapshot.key.substring(0,6) === 'white_' || snapshot.key.substring(0,6) === 'black_'){
        var data = snapshot.val();
        data['piece'] = snapshot.key;
        movePiece(data);
      }
    });
    this.setState({
      requiredMoves: requiredMoves
    })
  }


  componentDidUpdate() {
  }

  handlePieceMove (pieces, changesMade, move) {
    if(this.state.submitted) {
      if(this.state && changesMade) {
        let requiredMoves = [];
        if(this.state.whiteTurn) {
          requiredMoves = getRequiredMoves(pieces, false);
        } else {
          requiredMoves = getRequiredMoves(pieces, true);
        }

        setRequiredMoves(requiredMoves);

        var newMoves = this.state.moveList;
        newMoves.push(move)
        var gameData = pieces;
        gameData['whiteTurn'] = changesMade ? !this.state.whiteTurn : this.state.whiteTurn;
        var updates = {};
        updates['/SuicideChess/' + this.state.roomID + '/gameData/'] = gameData;
        updates['/SuicideChess/' + this.state.roomID + '/moveList'] = newMoves;

        let blackWin = true
        let whiteWin = true
        for(var piece in pieces) {
          if(pieces.hasOwnProperty(piece)) {
            if(pieces[piece].x !== -1) {
              if(piece.substring(0,6) === "black_") {
                blackWin = false;
              } else if (piece.substring(0,6) === "white_") {
                whiteWin = false;
              }
            }
          }
        }
        if(whiteWin) {
          updates['/SuicideChess/' + this.state.roomID + '/status'] = "finished"
          if(this.state.isWhite) {
            updates['/SuicideChess/' + this.state.roomID + '/winner'] = this.state.username
          } else {
            updates['/SuicideChess/' + this.state.roomID + '/winner'] = this.state.otherUser
          }
        } else if (blackWin) {
          updates['/SuicideChess/' + this.state.roomID + '/status'] = "finished"
          if(this.state.isWhite) {
            updates['/SuicideChess/' + this.state.roomID + '/winner'] = this.state.otherUser
          } else {
            updates['/SuicideChess/' + this.state.roomID + '/winner'] = this.state.username
          }
        }

        firebase.database().ref().update(updates);

        this.setState({
          validTiles: [],
          ...pieces,
          blackWin: blackWin,
          whiteWin: whiteWin,
          selectedPiece: null,
          moveList: newMoves,
          requiredMoves: requiredMoves,
          whiteTurn: changesMade ? !this.state.whiteTurn : this.state.whiteTurn,
        });
      } else {
        this.setState({
          selectedPiece: null,
          validTiles: []
        });
      }
    }
  };

  handlePieceSelect (piece) {
    if(this.state.submitted && !(this.state.whiteWin || this.state.blackWin)) {
      if((this.state.isWhite && this.state.whiteTurn) || (!this.state.isWhite && !this.state.whiteTurn)) {
        let validTiles = getValidMoves(this.state, piece)
        if(Object.keys(this.state.requiredMoves).length > 0) {
          validTiles = [];
          if(Object.keys(this.state.requiredMoves).includes(piece)) {
            for(var move in this.state.requiredMoves[piece]) {
              validTiles.push(this.state.requiredMoves[piece][move]);
            }
          } else {
            validTiles = [];
          }
        }
        if(piece !== null && this.state.isWhite && this.state.whiteTurn && piece.substring(0,5) === "white") {
          this.setState({
            validTiles: validTiles,
            selectedPiece: piece
          });
        } else if (piece !== null && !this.state.isWhite && !this.state.whiteTurn && piece.substring(0,5) === "black") {
          this.setState({
            validTiles: validTiles,
            selectedPiece: piece
          });
        }
      }
    }
  };

  handleFormChange (event) {
    this.setState({username: event.target.value});
  };

  handleSelectButton (event) {
    /*let a = this;
    var gameData = {};
    for(var property in a.state) {
      if(a.state.hasOwnProperty(property) && (property.substring(0,1) === 'w' || property.substring(0,1) === 'b')){
        gameData[property] = a.state[property];
      }
    }
    this.state.databaseRef.once('value').then(function(snapshot) {
      var games = snapshot.val();
      if(games === null) {
        var info = {
          user1: a.state.username,
          user2: '',
          gameData: gameData,
        };
        var roomID = a.state.databaseRef.push(info).key
        a.setState({
          username: a.state.username,
          isWhite: true,
          roomID: roomID,
          submitted: true,
        });
        var user2Joins = firebase.database().ref('/games/' + roomID);
        user2Joins.on('child_changed', function(snapshot) {
          user2Joins.off('child_changed');
          var gameListener = firebase.database().ref('/games/' + roomID + '/gameData/');
          gameListener.on('child_changed', function(snapshot) {
            if(snapshot.key.substring(0,6) === 'white_' || snapshot.key.substring(0,6) === 'black_'){
              var data = snapshot.val();
              data['piece'] = snapshot.key;
              movePiece(data);
            }
          });
          a.setState({
            otherUser: snapshot.val()
          });
        });
      } else {
        if(games[a.state.roomID]['user1'] === a.state.username) {
          var gameListener = firebase.database().ref('/games/' + property + '/gameData/');
          gameListener.on('child_changed', function(snapshot) {
            if(snapshot.key.substring(0,6) === 'white_' || snapshot.key.substring(0,6) === 'black_'){
              var data = snapshot.val();
              data['piece'] = snapshot.key;
              movePiece(data);
            }
          });
          gameData = games[a.state.roomID]['gameData']
          setPieces(gameData)
          a.setState({
            ...gameData,
            isWhite: true,
            username: a.state.username,
            otherUser: games[a.state.roomID]['user2'],
            submitted: true,
          });
        } else if (games[a.state.roomID]['user2'] === a.state.username) {
          gameListener = firebase.database().ref('/games/' + property + '/gameData/');
          gameListener.on('child_changed', function(snapshot) {
            if(snapshot.key.substring(0,6) === 'white_' || snapshot.key.substring(0,6) === 'black_'){
              var data = snapshot.val();
              data['piece'] = snapshot.key;
              movePiece(data);
            }
          });
          gameData = games[a.state.roomID]['gameData']
          setPieces(gameData);
          a.setState({
            ...gameData,
            isWhite: false,
            username: a.state.username,
            otherUser: games[a.state.roomID]['user1'],
            submitted: true,
          })
        }
        /*for(var property in games) {
          if(games.hasOwnProperty(property)) {
            if(games[property]['user2'] === '') {
              var postData ={
                user1: games[property]['user1'],
                user2: a.state.username,
                gameData: games[property]['gameData']
              }
              var updates = {};
              updates['/games/' + property] = postData;
              firebase.database().ref().update(updates);
              var gameListener = firebase.database().ref('/games/' + property + '/gameData/');
              gameListener.on('child_changed', function(snapshot) {
                if(snapshot.key.substring(0,6) === 'white_' || snapshot.key.substring(0,6) === 'black_'){
                  var data = snapshot.val();
                  data['piece'] = snapshot.key;
                  movePiece(data);
                }
              });
              a.setState({
                username: a.state.username,
                otherUser: games[property]['user1'],
                submitted: true,
                roomID: property,
              });
            }
          }
        }
      }
    })*/
  };

  getHeader = () => {
    if(this.state.submitted) {
      if(this.state.whiteWin) {
        if(this.state.isWhite) {
          return "You won!"
        } else {
          return "You lost!"
        }
      } else if (this.state.blackWin) {
        if(this.state.isWhite) {
          return "You lost!"
        } else {
          return "You won!"
        }
      } else if (this.state.isWhite) {
        if(this.state.whiteTurn) {
          return "Your turn"
        } else {
          return "Opponent's turn"
        }
      } else {
        if(this.state.whiteTurn){
          return "Opponent's turn"
        } else {
          return "Your Turn"
        }
      }
    }
  }

  render() {
    var header = this.getHeader()
    return (
      <div className="Gamescene">
        <h2>{header}</h2>
          <p> Username: {this.state.username}  Opponent: {this.state.otherUser}</p>
        <Board state={this.state} selectedPiece={this.state.selectedPiece} validTiles={this.state.validTiles} requiredMoves={this.state.requiredMoves}/>
      </div>
    );
  };
}

/* starting game data:
black_knightA: { x: 2, y: 0 },
black_knightB: { x: 6, y: 0 },
black_bishopA: { x: 2, y: 0 },
black_bishopB: { x: 5, y: 0 },
black_rookA: { x: 0, y: 0 },
black_rookB: { x: 7, y: 0 },
black_queen: { x: 3, y: 0 },
black_king: { x: 4, y: 0 },
black_pawnA: { x: 0, y: 1, firstMove: true },
black_pawnB: { x: 1, y: 1, firstMove: true },
black_pawnC: { x: 2, y: 1, firstMove: true },
black_pawnD: { x: 3, y: 1, firstMove: true },
black_pawnE: { x: 4, y: 1, firstMove: true },
black_pawnF: { x: 5, y: 1, firstMove: true },
black_pawnG: { x: 6, y: 1, firstMove: true },
black_pawnH: { x: 7, y: 1, firstMove: true },

white_knightA: { x: 1, y: 7 },
white_knightB: { x: 6, y: 7 },
white_bishopA: { x: 2, y: 7 },
white_bishopB: { x: 5, y: 7 },
white_rookA: { x: 0, y: 7 },
white_rookB: { x: 7, y: 7 },
white_queen: { x: 3, y: 7 },
white_king: { x: 4, y: 7 },
white_pawnA: { x: 0, y: 6, firstMove: true },
white_pawnB: { x: 1, y: 6, firstMove: true },
white_pawnC: { x: 2, y: 6, firstMove: true },
white_pawnD: { x: 3, y: 6, firstMove: true },
white_pawnE: { x: 4, y: 6, firstMove: true },
white_pawnF: { x: 5, y: 6, firstMove: true },
white_pawnG: { x: 6, y: 6, firstMove: true },
white_pawnH: { x: 7, y: 6, firstMove: true },
*/

export default gamescene;
