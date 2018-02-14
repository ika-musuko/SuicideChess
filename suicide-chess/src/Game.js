import { canMoveKnight, canMoveBishop, canMoveQueen, canMoveRook, canMoveKing, canMoveBlackPawn } from './GameMoves'

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
}

let observer = null

let firstTimeObserve = true
let firstTimePieceObserve = true

function emitChange() {
    observer(pieces)
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
    let canMove = true
    for(var property in pieces) {
        if(pieces.hasOwnProperty(property)) {
            if(pieces[property].x === move.x && pieces[property].y === move.y) {
                canMove = false
                emitPieceChange(null)
            }
        }
    }
    if(canMove){
        if(move.piece === "black_knightA") {
            if(canMoveKnight(move.x, move.y, pieces.black_knightA)){
                pieces.black_knightA = {x: move.x, y: move.y}
            }
        } else if (move.piece === "black_knightB") {
            if(canMoveKnight(move.x, move.y, pieces.black_knightB)){
                pieces.black_knightB = {x: move.x, y: move.y}
            }
        } else if (move.piece === "black_queen") {
            if (canMoveQueen(move.x, move.y, pieces.black_queen, pieces)) {
                pieces.black_queen = {x: move.x, y: move.y}
            }
        } else if (move.piece === "black_king") {
            if(canMoveKing(move.x, move.y, pieces.black_king, pieces)) {
                pieces.black_king = {x: move.x, y: move.y}
            }
        } else if (move.piece === "black_bishopA") {
            if(canMoveBishop(move.x, move.y, pieces.black_bishopA, pieces)) {
                pieces.black_bishopA = {x: move.x, y: move.y}
            }
        } else if (move.piece === "black_bishopB") {
            if(canMoveBishop(move.x, move.y, pieces.black_bishopB, pieces)) {
                pieces.black_bishopB = {x: move.x, y: move.y}
            }
        } else if (move.piece === "black_rookA") {
            if(canMoveRook(move.x, move.y, pieces.black_rookA, pieces)) {
                pieces.black_rookA = {x: move.x, y: move.y}
            }
        } else if (move.piece === "black_rookB") {
            if(canMoveRook(move.x, move.y, pieces.black_rookB, pieces)) {
                pieces.black_rookB = {x: move.x, y: move.y}
            }
        } else if (move.piece.substring(0,10) === "black_pawn") {
            if(canMoveBlackPawn(move.x, move.y, pieces[move.piece], pieces, pieces[move.piece].firstMove)) {
                pieces[move.piece] = {x: move.x, y: move.y, firstMove: false}
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
