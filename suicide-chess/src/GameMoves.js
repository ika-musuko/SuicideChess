export function canMoveKnight(toX, toY, currentPos) {
    let dx = toX - currentPos.x
    let dy = toY - currentPos.y

    return (
        (Math.abs(dx) === 2 && Math.abs(dy) === 1) || (Math.abs(dx) === 1 && Math.abs(dy) === 2)
    )
}

export function canMoveQueen(toX, toY, currentPos, pieces) {
    let dx = toX - currentPos.x
    let dy = toY - currentPos.y
    let canMove = true
    if(dy === 0) {
        if(dx < 0) {
            for(var property in pieces) {
                if(pieces.hasOwnProperty(property)) {
                    if (pieces[property].x > toX && pieces[property].x < currentPos.x && pieces[property].y === currentPos.y) {
                        canMove = false
                    }
                }
            }
        } else if (dx > 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property)) {
                    if (pieces[property].x < toX && pieces[property].x > currentPos.x && pieces[property].y === currentPos.y) {
                        canMove = false
                    }
                }
            }
        }
    } else if (dx === 0) {
        if(dy < 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property)) {
                    if(pieces[property].y > toY && pieces[property].y < currentPos.y && pieces[property].x === currentPos.x) {
                        canMove = false
                    }
                }
            }
        } else if (dy > 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property)) {
                    if(pieces[property].y < toY && pieces[property].y > currentPos.y && pieces[property].x === currentPos.x) {
                        canMove = false
                    }
                }
            }
        }
    } else if (Math.abs(dx) === Math.abs(dy)) {
        canMove = true
    } else {
        canMove = false
    }
    return canMove
}