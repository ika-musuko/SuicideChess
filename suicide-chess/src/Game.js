import { canMoveKnight, canMoveBishop, canMoveQueen, canMoveRook } from './GameMoves'

let pieces = {
    black_knightA: { x: 1, y: 0 },
    black_knightB: { x: 6, y: 0 },
    black_bishopA: { x: 2, y: 0 },
    black_bishopB: { x: 5, y: 0 },
    black_rookA: { x: 0, y: 0 },
    black_rookB: { x: 7, y: 0 },
    black_queen: { x: 3, y: 0 },
    black_king: { x: 4, y: 0 },
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
        } else if (move.piece === "Black_BishopA") {
            if(canMoveBishop(move.x, move.y, pieces.black_bishopA, pieces)) {
                pieces.black_bishopA = {x: move.x, y: move.y}
            }
        } else if (move.piece === "Black_BishopB") {
            if(canMoveBishop(move.x, move.y, pieces.black_bishopB, pieces)) {
                pieces.black_bishopB = {x: move.x, y: move.y}
            }
        } else if (move.piece === "Black_RookA") {
            if(canMoveRook(move.x, move.y, pieces.black_rookA, pieces)) {
                pieces.black_rookA = {x: move.x, y: move.y}
            }
        } else if (move.piece === "Black_RookB") {
            if(canMoveRook(move.x, move.y, pieces.black_rookB, pieces)) {
                pieces.black_rookB = {x: move.x, y: move.y}
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
