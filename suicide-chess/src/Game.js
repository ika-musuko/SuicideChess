import { canMoveKnight, canMoveBishop, canMoveQueen, canMoveRook, canMoveKing, canMoveBlackPawn, canMoveWhitePawn } from './Utilities/GameMoves'

let pieces = {
    black_knightA: { x: 1, y: 0 },
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
}

let observer = null

let firstTimeObserve = true
let firstTimePieceObserve = true

let whiteTurn = true

let changesMade = false

function emitChange() {
    whiteTurn = !whiteTurn
    observer(pieces, changesMade)
}

export function observe(o) {
    if(observer) {
        throw new Error('Multiple observers not implemented')
    }
    observer = o
    if(firstTimeObserve) {
        firstTimeObserve = false
        return
    } else {
        emitChange()
    }

    return () => {
        observer = null
    }
}

export function movePiece(move) {
    changesMade = false
    let canMove = true
    for(var property in pieces) {
        if(pieces.hasOwnProperty(property)) {
            if(pieces[property].x === move.x && pieces[property].y === move.y && property.substring(0,5) === move.piece.substring(0,5)) {
                canMove = false
                emitPieceChange(null)
            }
        }
    }
    if(canMove){
        if(move.piece === "black_knightA") {
            if(canMoveKnight(move.x, move.y, pieces.black_knightA)){
                pieces.black_knightA = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                        pieces[property].y = -1
                        pieces[property].x = -1
                    }
                }
            }
        } else if (move.piece === "black_knightB") {
            if(canMoveKnight(move.x, move.y, pieces.black_knightB)){
                pieces.black_knightB = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                        pieces[property].y = -1
                        pieces[property].x = -1
                    }
                }
            }
        } else if (move.piece === "black_queen") {
            if (canMoveQueen(move.x, move.y, pieces.black_queen, pieces)) {
                pieces.black_queen = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                        pieces[property].y = -1
                        pieces[property].x = -1
                    }
                }
            }
        } else if (move.piece === "black_king") {
            if(canMoveKing(move.x, move.y, pieces.black_king, pieces)) {
                pieces.black_king = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                        pieces[property].y = -1
                        pieces[property].x = -1
                    }
                }
            }
        } else if (move.piece === "black_bishopA") {
            if(canMoveBishop(move.x, move.y, pieces.black_bishopA, pieces)) {
                pieces.black_bishopA = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                        pieces[property].y = -1
                        pieces[property].x = -1
                    }
                }
            }
        } else if (move.piece === "black_bishopB") {
            if(canMoveBishop(move.x, move.y, pieces.black_bishopB, pieces)) {
                pieces.black_bishopB = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                        pieces[property].y = -1
                        pieces[property].x = -1
                    }
                }
            }
        } else if (move.piece === "black_rookA") {
            if(canMoveRook(move.x, move.y, pieces.black_rookA, pieces)) {
                pieces.black_rookA = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                        pieces[property].y = -1
                        pieces[property].x = -1
                    }
                }
            }
        } else if (move.piece === "black_rookB") {
            if(canMoveRook(move.x, move.y, pieces.black_rookB, pieces)) {
                pieces.black_rookB = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                        pieces[property].y = -1
                        pieces[property].x = -1
                    }
                }
            }
        } else if (move.piece.substring(0,10) === "black_pawn") {
            if(canMoveBlackPawn(move.x, move.y, pieces[move.piece], pieces, pieces[move.piece].firstMove)) {
                pieces[move.piece] = {x: move.x, y: move.y, firstMove: false}
                changesMade = true;
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                            pieces[property].x = -1
                            pieces[property].y = -1
                        }
                    }
                }
            }
        } else if (move.piece.substring(0,10) === "white_pawn") {
            if(canMoveWhitePawn(move.x, move.y, pieces[move.piece], pieces, pieces[move.piece].firstMove)) {
                pieces[move.piece] = {x: move.x, y: move.y, firstMove: false}
                changesMade = true;
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                            pieces[property].x = -1
                            pieces[property].y = -1
                        }
                    }
                }
            }
        } else if(move.piece === "white_knightA") {
            if(canMoveKnight(move.x, move.y, pieces.white_knightA)){
                pieces.white_knightA = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                            pieces[property].x = -1
                            pieces[property].y = -1
                        }
                    }
                }
            }
        } else if (move.piece === "white_knightB") {
            if(canMoveKnight(move.x, move.y, pieces.white_knightB)){
                pieces.white_knightB = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                            pieces[property].x = -1
                            pieces[property].y = -1
                        }
                    }
                }
            }
        } else if (move.piece === "white_queen") {
            if (canMoveQueen(move.x, move.y, pieces.white_queen, pieces)) {
                pieces.white_queen = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                            pieces[property].x = -1
                            pieces[property].y = -1
                        }
                    }
                }
            }
        } else if (move.piece === "white_king") {
            if(canMoveKing(move.x, move.y, pieces.white_king, pieces)) {
                pieces.white_king = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                            pieces[property].x = -1
                            pieces[property].y = -1
                        }
                    }
                }
            }
        } else if (move.piece === "white_bishopA") {
            if(canMoveBishop(move.x, move.y, pieces.white_bishopA, pieces)) {
                pieces.white_bishopA = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                            pieces[property].x = -1
                            pieces[property].y = -1
                        }
                    }
                }
            }
        } else if (move.piece === "white_bishopB") {
            if(canMoveBishop(move.x, move.y, pieces.white_bishopB, pieces)) {
                pieces.white_bishopB = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                            pieces[property].x = -1
                            pieces[property].y = -1
                        }
                    }
                }
            }
        } else if (move.piece === "white_rookA") {
            if(canMoveRook(move.x, move.y, pieces.white_rookA, pieces)) {
                pieces.white_rookA = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                            pieces[property].x = -1
                            pieces[property].y = -1
                        }
                    }
                }
            }
        } else if (move.piece === "white_rookB") {
            if(canMoveRook(move.x, move.y, pieces.white_rookB, pieces)) {
                pieces.white_rookB = {x: move.x, y: move.y}
                changesMade = true;
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[move.piece].x === pieces[property].x && pieces[move.piece].y === pieces[property].y && property.substring(0,5) !== move.piece.substring(0,5)) {
                            pieces[property].x = -1
                            pieces[property].y = -1
                        }
                    }
                }
            }
        }
        emitChange()
    }
}

let pieceObserver = null
function emitPieceChange(piece) {
    pieceObserver(piece)
}

export function pieceObserve(p) {
    pieceObserver = p
    if(firstTimePieceObserve) {
        firstTimePieceObserve = false
        return
    } else {
        emitPieceChange()
    }
}

export function selectPiece(piece) {
    emitPieceChange(piece)
}
