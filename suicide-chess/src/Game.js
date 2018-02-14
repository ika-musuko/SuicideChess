import { canMoveKnight } from './GameMoves'
import { canMoveQueen } from './GameMoves'

let pieces = {
    black_knightA: {x: 1, y:0},
    black_knightB: {x: 6, y:0},
    black_queen: {x: 3, y: 0}
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
        if(move.piece === "Black_KnightA") {
            if(canMoveKnight(move.x, move.y, pieces.black_knightA)){
                pieces.black_knightA = {x: move.x, y: move.y}
            }
        } else if (move.piece === "Black_KnightB") {
            if(canMoveKnight(move.x, move.y, pieces.black_knightB)){
                pieces.black_knightB = {x: move.x, y: move.y}
            }
        } else if (move.piece === "Black_Queen") {
            if (canMoveQueen(move.x, move.y, pieces.black_queen, pieces)) {
                pieces.black_queen = {x: move.x, y: move.y}
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
