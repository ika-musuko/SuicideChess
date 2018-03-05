import { canMoveWhitePawn, canMoveBlackPawn, canMoveKnight, canMoveRook, canMoveQueen, canMoveKing, canMoveBishop } from '../Utilities/GameMoves'

export function getValidMoves(state,piece) {
    let validTiles = []
    if(piece !== null) {
        if(state.whiteTurn) {
            if(piece.substring(0,7) === "white_p"){
                for(var x = 0; x < 8; x++) {
                    for(var y = 0; y < 8; y++) {
                      if(canMoveWhitePawn(x,y,state[piece], state, state[piece].firstMove)) {
                        validTiles.push({ x: x, y: y})
                      }
                    }
                  }
                return validTiles
            } else if (piece === "white_knightA" || piece === "white_knightB"){
                for(x = 0; x < 8; x++) {
                    for(y = 0; y < 8; y++) {
                        if(canMoveKnight(piece,x,y,state[piece], state)) {
                            validTiles.push({ x: x, y: y})
                        }
                    }
                }
                return validTiles
            } else if (piece === "white_rookA" || piece === "white_rookB") {
                for(x = 0; x < 8; x++) {
                    for(y = 0; y < 8; y++) {
                        if(canMoveRook(x,y,state[piece], state, piece)) {
                            validTiles.push({x: x, y: y})
                        }
                    }
                }
                return validTiles
            } else if (piece === "white_queen"){
                for(x = 0; x < 8; x++) {
                    for(y = 0; y < 8; y++) {
                        if(canMoveQueen(x,y,state[piece], state, piece)) {
                            validTiles.push({x: x, y: y})
                        }
                    }
                }
                return validTiles
            } else if (piece === "white_king"){
                for(x = 0; x < 8; x++) {
                    for(y = 0; y < 8; y++) {
                        if(canMoveKing(x,y,state[piece], state, piece)) {
                            validTiles.push({x:x,y:y})
                        }
                    }
                }
                return validTiles
            } else if(piece === "white_bishopA" || piece === "white_bishopB"){
                for(x = 0; x < 8; x++) {
                    for(y = 0; y < 8; y++) {
                        if(canMoveBishop(x,y,state[piece], state, piece)) {
                            validTiles.push({x:x,y:y})
                        }
                    }
                }
                return validTiles
            } else {
                return []
            }
        } else {
            if(piece.substring(0,7) === "black_p") {
                for(x = 0; x < 8; x++) {
                    for(y = 0; y < 8; y++) {
                      if(canMoveBlackPawn(x,y,state[piece], state, state[piece].firstMove)) {
                        validTiles.push({x: x, y: y})
                      }
                    }
                  }
                return validTiles
            } else if (piece === "black_knightA" || piece === "black_knightB"){
                for(x = 0; x < 8; x++) {
                    for(y = 0; y < 8; y++) {
                        if(canMoveKnight(piece,x,y,state[piece], state)) {
                            validTiles.push({ x: x, y: y})
                        }
                    }
                }
                return validTiles
            } else if (piece === "black_rookA" || piece === "black_rookB") {
                for(x = 0; x < 8; x++) {
                    for(y = 0; y < 8; y++) {
                        if(canMoveRook(x,y,state[piece], state, piece)) {
                            validTiles.push({x: x, y: y})
                        }
                    }
                }
                return validTiles
            } else if (piece === "black_queen"){
                for(x = 0; x < 8; x++) {
                    for(y = 0; y < 8; y++) {
                        if(canMoveQueen(x,y,state[piece], state, piece)) {
                            validTiles.push({x: x, y: y})
                        }
                    }
                }
                return validTiles
            } else if (piece === "black_king"){
                for(x = 0; x < 8; x++) {
                    for(y = 0; y < 8; y++) {
                        if(canMoveKing(x,y,state[piece], state, piece)) {
                            validTiles.push({x:x,y:y})
                        }
                    }
                }
                return validTiles
            } else if(piece === "black_bishopA" || piece === "black_bishopB"){
                for(x = 0; x < 8; x++) {
                    for(y = 0; y < 8; y++) {
                        if(canMoveBishop(x,y,state[piece], state, piece)) {
                            validTiles.push({x:x,y:y})
                        }
                    }
                }
                return validTiles
            } else {
                return []
            }
        }
    } else {
        return []
    }
}