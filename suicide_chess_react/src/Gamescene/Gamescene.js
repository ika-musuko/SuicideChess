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
import { getPiece } from '../Utilities/GetPieceById'
import { checkStalemate } from '../Utilities/CheckStalemate'

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

      stalemate: false,

      blackWin: false,

      movesSinceCaptureOrPawnMove: 0,

      databaseRef: firebase.database().ref('/SuicideChess/' + this.props.roomID),

      rematchRoute: '/rematch/' + this.props.roomID,
      exitGameRoute: '/exit_game/' + this.propsroomID,

      submitted: false,

      isWhite: false,
      userId: this.props.user,
      userName: '',
      otherUserName: '',
      otherUserId: '',
      roomID: this.props.roomID,

      selectedPiece: null
    }
    observe(this.handlePieceMove.bind(this))
    pieceObserve(this.handlePieceSelect.bind(this))
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
      var otherUserId = '';
      if(room['players'][0] === a.state.userId) {

        var gameData = room['gameData']

        var winner = room['winner']

        if(winner === a.state.userId) {
          a.setState({
            ...gameData,
            whiteTurn: gameData['whiteTurn'],
            userId: a.state.userId,
            otherUserId: room['players'][1],
            moveList: room['moveList'],
            submitted: true,
            isWhite: true,
            whiteWin: true,
          });
          otherUserId = room['players'][1]
        } else if (winner === room['players'][1]) {
          a.setState({
            ...gameData,
            whiteTurn: gameData['whiteTurn'],
            userId: a.state.userId,
            otherUserId: room['players'][1],
            moveList: room['moveList'],
            submitted: true,
            isWhite: true,
            blackWin: true,
          });
          otherUserId = room['players'][1]
        }

        a.setState({
          ...gameData,
          whiteTurn: gameData['whiteTurn'],
          userId: a.state.userId,
          otherUserId: room['players'][1],
          stalemate: gameData['movesSinceCaptureOrPawnMove'] >= 20 ? true : false,
          moveList: room['moveList'],
          submitted: true,
          isWhite: true,
        });
        otherUserId = room['players'][1]
        a.updateStateAfterDatabaseSync()
      } else if (room['players'][1] === a.state.userId) {

        gameData = room['gameData']
        winner = room['winner']
        if(winner === a.state.userId) {
          a.setState({
            ...gameData,
            whiteTurn: gameData['whiteTurn'],
            userId: a.state.userId,
            otherUserId: room['players'][0],
            moveList: room['moveList'],
            submitted: true,
            isWhite: false,
            blackWin: true,
          })
          otherUserId = room['players'][0]
        } else if (winner === room['players'][0]) {
          a.setState({
            ...gameData,
            whiteTurn: gameData['whiteTurn'],
            userId: a.state.userId,
            otherUserId: room['players'][0],
            moveList: room['moveList'],
            submitted: true,
            isWhite: false,
            whiteWin: true,
          })
          otherUserId = room['players'][0]
        }

        a.setState({
          ...gameData,
          whiteTurn: gameData['whiteTurn'],
          userId: a.state.userId,
          otherUserId: room['players'][0],
          moveList: room['moveList'],
          stalemate: gameData['movesSinceCaptureOrPawnMove'] >= 20 ? true : false,
          submitted: true,
          isWhite: false
        })
        otherUserId = room['players'][0]
        a.updateStateAfterDatabaseSync()
      }
      if(a.otherUserId !== '') {
        var thisUserRef = firebase.database().ref('/users/' + a.state.userId)
        thisUserRef.once('value').then(function(snapshot) {
          a.setState({
            userName: snapshot.val().displayName
          })
        });
        var thatUserRef = firebase.database().ref('/users/' + otherUserId)
        thatUserRef.once('value').then(function(snapshot) {
          a.setState({
            otherUserName: snapshot.val().displayName
          })
        })
      } else {
        thisUserRef = firebase.database().ref('/users/' + a.state.userId)
        thisUserRef.once('value').then(function(snapshot) {
          a.setState({
            userName: snapshot.val().displayName
          })
        });
      }
    })
  }

  updateStateAfterDatabaseSync = () => {
    var newGameData = {};

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
    var a = this;
    gameListener.on('child_changed', function(snapshot) {
      if(snapshot.key.substring(0,6) === 'white_' || snapshot.key.substring(0,6) === 'black_'){
        var data = snapshot.val();
        data['piece'] = snapshot.key;
        movePiece(data);
      } else if (snapshot.key === 'movesSinceCaptureOrPawnMove'){
        var data = snapshot.val();
        a.setState({
          movesSinceCaptureOrPawnMove: data
        })
      }
    });
    this.setState({
      requiredMoves: requiredMoves
    })
  }

  componentDidUpdate() {

  }

  handlePieceMove (pieces, changesMade, move, pieceCaptured) {
    if(this.state.submitted) {
      if(this.state && changesMade) {
        if(this.state.movesSinceCaptureOrPawnMove + 1 >= 20) {
          stalemate = true;
        }
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
        updates['/SuicideChess/' + this.state.roomID + '/moveList'] = newMoves;


        let blackWin = true
        let whiteWin = true
        var stalemate = checkStalemate(pieces, !this.state.whiteTurn);

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


        let pawnMoved = false;
        for(var piece in pieces) {
          if(pieces.hasOwnProperty(piece)){
            if(this.state[piece].x !== pieces[piece].x || this.state[piece].y !== pieces[piece].y) {
              if(piece.substring(6,10) === 'pawn') {
                pawnMoved = true;
              }
            }
          }
        }

        let incremenetMovesSinceCaptureOrPawnMove = false;
        var resetMoveSinceCapturedOrPawnMove = pawnMoved || pieceCaptured ? true : false
        if(this.state.isWhite) {
          if(this.state.whiteTurn) {
            incremenetMovesSinceCaptureOrPawnMove = true;
          } else {

          }
        } else {
          if(this.state.whiteTurn) {

          } else {
            incremenetMovesSinceCaptureOrPawnMove = true;
          }
        }
        if(incremenetMovesSinceCaptureOrPawnMove) {
          if(this.state.isWhite && this.state.whiteTurn) {
            gameData['movesSinceCaptureOrPawnMove'] = this.state.movesSinceCaptureOrPawnMove + 1
          } else if (!this.state.isWhite && !this.state.whiteTurn) {
            gameData['movesSinceCaptureOrPawnMove'] = this.state.movesSinceCaptureOrPawnMove + 1
          }
          if(this.state.movesSinceCaptureOrPawnMove + 1 >= 20) {
            stalemate = true;
          }
        } else {
          gameData['movesSinceCaptureOrPawnMove'] = this.state.movesSinceCaptureOrPawnMove
        }

        if(resetMoveSinceCapturedOrPawnMove) {
          gameData['movesSinceCaptureOrPawnMove'] = 0;
        }

        if(stalemate) {
          let aliveBlackPieces = 0;
          let aliveWhitePieces = 0;
          for(piece in pieces) {
            if(pieces.hasOwnProperty(piece)) {
              if(piece.substring(0,6) === 'white_' && pieces[piece].x !== -1) {
                aliveWhitePieces++;
              } else if (piece.substring(0,6) === 'black_' && pieces[piece].x !== -1) {
                aliveBlackPieces++;
              }
            }
          }
          if(aliveBlackPieces > aliveWhitePieces) {
            stalemate = false
            whiteWin = true
          } else if (aliveBlackPieces < aliveWhitePieces) {
            stalemate = false
            blackWin = true
          }
        }

        if(whiteWin) {
          updates['/SuicideChess/' + this.state.roomID + '/status'] = "finished"
          if(this.state.isWhite) {
            updates['/SuicideChess/' + this.state.roomID + '/winner'] = this.state.userId
          } else {
            updates['/SuicideChess/' + this.state.roomID + '/winner'] = this.state.otherUserId
          }
        } else if (blackWin) {
          updates['/SuicideChess/' + this.state.roomID + '/status'] = "finished"
          if(this.state.isWhite) {
            updates['/SuicideChess/' + this.state.roomID + '/winner'] = this.state.otherUserId
          } else {
            updates['/SuicideChess/' + this.state.roomID + '/winner'] = this.state.userId
          }
        } else if (stalemate) {
          updates['/SuicideChess/' + this.state.roomID + '/status'] = "finished"
        }

        updates['/SuicideChess/' + this.state.roomID + '/gameData/'] = gameData;

        firebase.database().ref().update(updates);

        if(whiteWin || blackWin || stalemate) {
          window.location.reload();
        }

        this.setState({
          validTiles: [],
          ...pieces,
          blackWin: blackWin,
          whiteWin: whiteWin,
          stalemate: stalemate,
          selectedPiece: null,
          moveList: newMoves,
          movesSinceCaptureOrPawnMove: incremenetMovesSinceCaptureOrPawnMove ? (this.state.movesSinceCaptureOrPawnMove + 1) : (this.state.movesSinceCaptureOrPawnMove + 1),
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
    if(!(this.state.whiteWin || this.state.blackWin) && !this.state.stalemate) {
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

  getHeader = () => {
    if(this.state.submitted) {
      if(this.state.stalemate) {
        return "Stalemate!"
      }
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
    var yourCapturedPieces = [];
    var theirCapturedPieces = [];
    if(this.state.isWhite) {
      for(var property in this.state) {
        if(this.state.hasOwnProperty(property)) {
          if(property.substring(0,6) === 'white_') {
            if(this.state[property].x === -1 && this.state[property].y === -1) {
              theirCapturedPieces.push(property);
            }
          } else if (property.substring(0,6) === 'black_'){
            if(this.state[property].x === -1 && this.state[property].y === -1) {
              yourCapturedPieces.push(property);
            }
          }
        }
      }
    } else {
      for(property in this.state) {
        if(this.state.hasOwnProperty(property)) {
          if(property.substring(0,6) === 'white_') {
            if(this.state[property].x === -1 && this.state[property].y === -1) {
              yourCapturedPieces.push(property);
            }
          } else if(property.substring(0,6) === 'black_'){
            if(this.state[property].x === -1 && this.state[property].y === -1) {
              theirCapturedPieces.push(property);
            }
          }
        }
      }
    }
    return (
      <div className="Gamescene">
        <div className="left-column" style={{display: 'inline', float: 'left', width:'30%'}}>
          <h3>Your Captured Pieces</h3>
          <div className='captured-pieces'>
            {yourCapturedPieces.map(piece => getPiece(piece))}
          </div>
        </div>
        <div className='center-column' style={{display: 'inline', float:'left', width: '40%'}}>
          <h2>{this.getHeader()}</h2>
          <h3>{this.state.userName} vs. {this.state.otherUserName}</h3>
          <Board flip={!this.state.isWhite} state={this.state} selectedPiece={this.state.selectedPiece} validTiles={this.state.validTiles} requiredMoves={this.state.requiredMoves}/>
        </div>
        <div className='left-column' style={{display:'inline', width:'30%', float:'left'}}>
          <h3>Their Captured Pieces</h3>
          <div className='captured-pieces'>
            {theirCapturedPieces.map(piece => getPiece(piece))}
          </div>
        </div>
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
