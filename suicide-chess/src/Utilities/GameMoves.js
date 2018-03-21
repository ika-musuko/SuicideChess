export function canMoveKnight(piece, toX, toY, currentPos, pieces) {
    let dx = toX - currentPos.x
    let dy = toY - currentPos.y

    for(var property in pieces) {
        if(pieces.hasOwnProperty(property)) {
            if (piece.substring(0,5) === property.substring(0,5) && pieces[property].x === toX && pieces[property].y === toY) {
                return false
            }
        }
    }

    return (
        (Math.abs(dx) === 2 && Math.abs(dy) === 1) || (Math.abs(dx) === 1 && Math.abs(dy) === 2)
    )
}

export function canMoveQueen(toX, toY, currentPos, pieces, piece) {
    let dx = toX - currentPos.x
    let dy = toY - currentPos.y

    for(var property in pieces) {
        if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
            if (pieces[property].x === toX && pieces[property].y === toY && property.substring(0,5) === piece.substring(0,5)) {
                return false
            }
        }
    }

    //Movement in x direction

    if(dy === 0) {

        //Negative movement

        if(dx < 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                    if (pieces[property].x > toX && pieces[property].x < currentPos.x && pieces[property].y === currentPos.y) {
                        return false
                    }
                }
            }
        }
        
        //Positive movement
        
        else if (dx > 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                    if (pieces[property].x < toX && pieces[property].x > currentPos.x && pieces[property].y === currentPos.y) {
                        return false
                    }
                }
            }
        }
    } 
    
    //Movement in y direction    

    else if (dx === 0) {

        //Negative Movement

        if(dy < 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                    if(pieces[property].y > toY && pieces[property].y < currentPos.y && pieces[property].x === currentPos.x) {
                        return false
                    }
                }
            }
        } 
        
        //Positive Movement

        else if (dy > 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                    if(pieces[property].y < toY && pieces[property].y > currentPos.y && pieces[property].x === currentPos.x) {
                        return false
                    }
                }
            }
        }
    } 
    
    //Diagonal movement
    
    else if (Math.abs(dx) === Math.abs(dy)) {

        //Movement in positive x and y

        if(dx > 0 && dy > 0) {
            var i = 1
            while(i < Math.abs(dy) && i < Math.abs(dx)) {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                        if(pieces[property].x === currentPos.x + i && pieces[property].y === currentPos.y + i && property !== piece) {
                            return false;
                        }
                    }
                }
                i++;
            }
        }

        //Movement in negative x and y

        else if (dx < 0 && dy < 0) {
            i = 1
            while(i < Math.abs(dy) && i < Math.abs(dx)) {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                        if(pieces[property].x === currentPos.x - i && pieces[property].y === currentPos.y - i && property !== piece) {
                            return false;
                        }
                    }
                }
                i++;
            }
        }

        //Movement in negative x and positive y

        else if (dx < 0 && dy > 0) {
            i = 1
            while(i < Math.abs(dy) && i < Math.abs(dx)) {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                        if(pieces[property].x === currentPos.x - i && pieces[property].y === currentPos.y + i && property !== piece) {
                            return false;
                        }
                    }
                }
                i++;
            } 
        }

        //Movement in positive x and negative y

        else if (dx > 0 && dy < 0) {
            i = 1
            while(i < Math.abs(dy) && i < Math.abs(dx)) {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                        if(pieces[property].x === currentPos.x + i && pieces[property].y === currentPos.y - i && property !== piece) {
                            return false;
                        }
                    }
                }
                i++;
            } 
        }

    } else {
        return false
    }
    return true
}

export function canMoveBishop(toX, toY, currentPos, pieces, piece) {

    let dx = toX - currentPos.x
    let dy = toY - currentPos.y

    for(var property in pieces) {
        if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
            if (pieces[property].x === toX && pieces[property].y === toY && property.substring(0,5) === piece.substring(0,5)) {
                return false
            }
        }
    }

    if (Math.abs(dx) === Math.abs(dy)) {

        //Movement in positive x and y

        if(dx > 0 && dy > 0) {
            var i = 1
            while(i < Math.abs(dy) && i < Math.abs(dx)) {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                        if(pieces[property].x === currentPos.x + i && pieces[property].y === currentPos.y + i && property !== piece) {
                            return false;
                        }
                    }
                }
                i++;
            }
        }

        //Movement in negative x and y

        else if (dx < 0 && dy < 0) {
            i = 1
            while(i < Math.abs(dy) && i < Math.abs(dx)) {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                        if(pieces[property].x === currentPos.x - i && pieces[property].y === currentPos.y - i && property !== piece) {
                            return false;
                        }
                    }
                }
                i++;
            }
        }

        //Movement in negative x and positive y

        else if (dx < 0 && dy > 0) {
            i = 1
            while(i < Math.abs(dy) && i < Math.abs(dx)) {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                        if(pieces[property].x === currentPos.x - i && pieces[property].y === currentPos.y + i && property !== piece) {
                            return false;
                        }
                    }
                }
                i++;
            } 
        }

        //Movement in positive x and negative y

        else if (dx > 0 && dy < 0) {
            i = 1
            while(i < Math.abs(dy) && i < Math.abs(dx)) {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                        if(pieces[property].x === currentPos.x + i && pieces[property].y === currentPos.y - i && property !== piece) {
                            return false;
                        }
                    }
                }
                i++;
            } 
        }
    } else {
        return false
    }
    return true
}

export function canMoveRook(toX, toY, currentPos, pieces, piece) {

    let dx = toX - currentPos.x
    let dy = toY - currentPos.y

    //Movement in x direction

    for(var property in pieces) {
        if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
            if (pieces[property].x === toX && pieces[property].y === toY && property.substring(0,5) === piece.substring(0,5)) {
                return false
            }
        }
    }

    if(dy === 0) {

        //Negative movement

        if(dx < 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                    if (pieces[property].x > toX && pieces[property].x < currentPos.x && pieces[property].y === currentPos.y) {
                        return false
                    }
                }
            }
        }
        
        //Positive movement
        
        else if (dx > 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                    if (pieces[property].x < toX && pieces[property].x > currentPos.x && pieces[property].y === currentPos.y) {
                        return false
                    }
                }
            }
        }
    } 
    
    //Movement in y direction    

    else if (dx === 0) {

        //Negative Movement

        if(dy < 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                    if(pieces[property].y > toY && pieces[property].y < currentPos.y && pieces[property].x === currentPos.x) {
                        return false
                    }
                }
            }
        } 
        
        //Positive Movement

        else if (dy > 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                    if(pieces[property].y < toY && pieces[property].y > currentPos.y && pieces[property].x === currentPos.x) {
                        return false
                    }
                }
            }
        }
    } else {
        return false
    }
    return true
}

export function canMoveKing(toX, toY, currentPos, pieces, piece) {
    let dx = toX - currentPos.x
    let dy = toY - currentPos.y
    if(Math.abs(dx) > 1 || Math.abs(dy) > 1) {
        return false
    } else {
        for(var property in pieces) {
            if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                if(pieces[property].x === toX && pieces[property].y === toY && property.substring(0,5) === piece.substring(0,5)){
                    return false
                }
            }
        }
    }
    return true
}

export function canMoveBlackPawn(toX, toY, currentPos, pieces, firstMove) {
    let dx = toX - currentPos.x
    let dy = toY - currentPos.y
    
    if(dy < 0) {
        return false
    } else if (dy === 1 && dx === 0) {
        for(var property in pieces) {
            if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                if(pieces[property].x === toX && pieces[property].y === toY) {
                    return false
                }
            }
        }
        return true
    } else if (dy === 2 && dx === 0 && firstMove) {
        for(property in pieces) {
            if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                if(pieces[property].x === toX && (pieces[property].y === toY - 1 || pieces[property].y === toY)) {
                    return false
                }
            }
        }
        return true
    } else if (dy === 1 && Math.abs(dx) === 1){
        for(property in pieces) {
            if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                if(pieces[property].x === toX && pieces[property].y === toY && property.substring(0,5) === "white") {
                    return true
                }
            }
        }
        return false
    } else {
        return false
    }
}

export function canMoveWhitePawn(toX, toY, currentPos, pieces, firstMove) {

    let dx = toX - currentPos.x
    let dy = toY - currentPos.y


    if(dy > 0) {
        return false
    } else if (dy === -1 && dx === 0) {
        for(var property in pieces) {
            if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                if(pieces[property].x === toX && pieces[property].y === toY) {
                    return false
                }
            }
        }
        return true
    } else if (dy === -2 && dx === 0 && firstMove) {
        for(property in pieces) {
            if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                if(pieces[property].x === toX && (pieces[property].y === toY + 1 || pieces[property].y === toY)) {
                    return false
                }
            }
        }
        return true
    } else if (dy === -1 && Math.abs(dx) === 1) { 
        for(property in pieces) {
            if(pieces.hasOwnProperty(property) && (property.substring(0,5) === "black" || property.substring(0,5) === "white")) {
                if(pieces[property].x === toX && pieces[property].y === toY && property.substring(0,5) === "black") {
                    return true
                }
            }
        }
        return false
    } else {
        return false
    }
}