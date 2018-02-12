let pieces = {
    black_knightA: {x: 2, y:0},
    black_knightB: {x: 5, y:0}
}
let observer = null

function emitChange() {
    observer(pieces)
}

export function observe(o) {
    if(observer) {
        throw new Error('Multiple observers not implemented')
    }
    observer = o
    emitChange()

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
            pieces.black_knightA = {x: move.x, y: move.y}
        } else if (move.piece === "Black_KnightB") {
            pieces.black_knightB = {x: move.x, y: move.y}
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
    emitPieceChange()
}

export function selectPiece(piece) {
    emitPieceChange(piece)
}
