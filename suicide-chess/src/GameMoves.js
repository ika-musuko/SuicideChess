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

    //Movement in x direction

    if(dy === 0) {

        //Negative movement

        if(dx < 0) {
            for(var property in pieces) {
                if(pieces.hasOwnProperty(property)) {
                    if (pieces[property].x > toX && pieces[property].x < currentPos.x && pieces[property].y === currentPos.y) {
                        return false
                    }
                }
            }
        }
        
        //Positive movement
        
        else if (dx > 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property)) {
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
                if(pieces.hasOwnProperty(property)) {
                    if(pieces[property].y > toY && pieces[property].y < currentPos.y && pieces[property].x === currentPos.x) {
                        return false
                    }
                }
            }
        } 
        
        //Positive Movement

        else if (dy > 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property)) {
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
            do {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[property].x === currentPos.x + i && pieces[property].y === currentPos.y + i) {
                            return false;
                        }
                    }
                }
                i++;
            } while(i < Math.abs(dy) && i < Math.abs(dx))
        }

        //Movement in negative x and y

        else if (dx < 0 && dy < 0) {
            i = 1
            do {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[property].x === currentPos.x - i && pieces[property].y === currentPos.y - i) {
                            return false;
                        }
                    }
                }
                i++;
            } while(i < Math.abs(dy) && i < Math.abs(dx))
        }

        //Movement in negative x and positive y

        else if (dx < 0 && dy > 0) {
            i = 1
            do {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[property].x === currentPos.x - i && pieces[property].y === currentPos.y + i) {
                            return false;
                        }
                    }
                }
                i++;
            } while(i < Math.abs(dy) && i < Math.abs(dx))
        }

        //Movement in positive x and negative y

        else if (dx > 0 && dy < 0) {
            i = 1
            do {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[property].x === currentPos.x + i && pieces[property].y === currentPos.y - i) {
                            return false;
                        }
                    }
                }
                i++;
            } while(i < Math.abs(dy) && i < Math.abs(dx))
        }

    } else {
        return false
    }
    return true
}

export function canMoveBishop(toX, toY, currentPos, pieces) {

    let dx = toX - currentPos.x
    let dy = toY - currentPos.y

    if (Math.abs(dx) === Math.abs(dy)) {

        //Movement in positive x and y

        if(dx > 0 && dy > 0) {
            var i = 1
            do {
                for(var property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[property].x === currentPos.x + i && pieces[property].y === currentPos.y + i) {
                            return false;
                        }
                    }
                }
                i++;
            } while(i < Math.abs(dy) && i < Math.abs(dx))
        }

        //Movement in negative x and y

        else if (dx < 0 && dy < 0) {
            i = 1
            do {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[property].x === currentPos.x - i && pieces[property].y === currentPos.y - i) {
                            return false;
                        }
                    }
                }
                i++;
            } while(i < Math.abs(dy) && i < Math.abs(dx))
        }

        //Movement in negative x and positive y

        else if (dx < 0 && dy > 0) {
            i = 1
            do {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[property].x === currentPos.x - i && pieces[property].y === currentPos.y + i) {
                            return false;
                        }
                    }
                }
                i++;
            } while(i < Math.abs(dy) && i < Math.abs(dx))
        }

        //Movement in positive x and negative y

        else if (dx > 0 && dy < 0) {
            i = 1
            do {
                for(property in pieces) {
                    if(pieces.hasOwnProperty(property)) {
                        if(pieces[property].x === currentPos.x + i && pieces[property].y === currentPos.y - i) {
                            return false;
                        }
                    }
                }
                i++;
            } while(i < Math.abs(dy) && i < Math.abs(dx))
        }

    } else {
        return false
    }
    return true
}

export function canMoveRook(toX, toY, currentPos, pieces) {

    let dx = toX - currentPos.x
    let dy = toY - currentPos.y

    //Movement in x direction

    if(dy === 0) {

        //Negative movement

        if(dx < 0) {
            for(var property in pieces) {
                if(pieces.hasOwnProperty(property)) {
                    if (pieces[property].x > toX && pieces[property].x < currentPos.x && pieces[property].y === currentPos.y) {
                        return false
                    }
                }
            }
        }
        
        //Positive movement
        
        else if (dx > 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property)) {
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
                if(pieces.hasOwnProperty(property)) {
                    if(pieces[property].y > toY && pieces[property].y < currentPos.y && pieces[property].x === currentPos.x) {
                        return false
                    }
                }
            }
        } 
        
        //Positive Movement

        else if (dy > 0) {
            for(property in pieces) {
                if(pieces.hasOwnProperty(property)) {
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

export function canMoveKing(toX, toY, currentPos, pieces) {
    return true;
}