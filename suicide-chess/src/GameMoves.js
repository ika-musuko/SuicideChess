export function canMoveKnight(toX, toY, currentPos) {
    let dx = toX - currentPos.x
    let dy = toY - currentPos.y

    return (
        (Math.abs(dx) === 2 && Math.abs(dy) === 1) || (Math.abs(dx) === 1 && Math.abs(dy) === 2)
    )
}