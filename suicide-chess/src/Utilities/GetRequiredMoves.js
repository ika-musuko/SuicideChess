import { getValidMoves } from './GetValidMoves'

export function getRequiredMoves(pieces, whiteTurnNext) {
  let requiredMoves = {};
  if(whiteTurnNext) {
    for(var property in pieces) {
      if(pieces.hasOwnProperty(property) && property.substring(0,6) === 'white_') {
        pieces['whiteTurn'] = true;
        let moves = getValidMoves(pieces, property);
        let validPieceMoves = [];
        for(var moveKey in moves) {
          if(moves.hasOwnProperty(moveKey)) {
            let move = moves[moveKey];
            for(var pieceKey in pieces) {
              if(pieces.hasOwnProperty(pieceKey) && pieceKey.substring(0,6) === 'black_') {
                let piece = pieces[pieceKey];
                if(move.x === piece.x && move.y === piece.y) {
                  validPieceMoves.push(move);
                }
              }
            }
          }
        }
        if(validPieceMoves.length !== 0) {
            requiredMoves[property] = validPieceMoves;
        }
      }
    }
  } else {
    for(var property in pieces) {
      if(pieces.hasOwnProperty(property) && property.substring(0,6) === 'black_') {
        pieces['whiteTurn'] = false;
        let moves = getValidMoves(pieces, property);
        let validPieceMoves = [];
        for(var moveKey in moves) {
          if(moves.hasOwnProperty(moveKey)) {
            let move = moves[moveKey];
            for(var pieceKey in pieces) {
              if(pieces.hasOwnProperty(pieceKey) && pieceKey.substring(0,6) === 'white_') {
                let piece = pieces[pieceKey];
                if(move.x === piece.x && move.y === piece.y) {
                  validPieceMoves.push(move);
                }
              }
            }
          }
        }
        if(validPieceMoves.length !== 0) {
            requiredMoves[property] = validPieceMoves;
        }
      }
    }
  }
  console.log(requiredMoves);
}
