function between(x, min, max) { // Inclusive
    return x <= max && x >= min;
}

function circle(ctx, x, y, r, color, stroke = false, strokeInfo = { width: 1, color: '#000' }) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
    if (stroke) {
        ctx.lineWidth = strokeInfo.width;
        ctx.strokeStyle = strokeInfo.color;
        ctx.stroke();
    }
}

function map_range(current, in_min, in_max, out_min, out_max) {
    return ((current - in_min) * (out_max - out_min)) / (in_max - in_min) + out_min;
}

function Matchup(ctx, index, winner, team1, team2) {
    this.getLevel = () => {
        if (between(index, 0, 15)) return -5
        else if (between(index, 16, 31)) return 5
        else if (between(index, 32, 39)) return -4
        else if (between(index, 40, 47)) return 4
        else if (between(index, 48, 51)) return -3
        else if (between(index, 52, 55)) return 3
        else if (index === 56 || index === 57) return -2
        else if (index === 58 || index === 59) return 2
        else if (index === 60) return -1
        else if (index === 61) return 1
        else if (index === 62) return 0
    };

    this.getRow = (level) => {
        if (level >= -1 && level <= 1) {
            return 7;
        }
        let intercept = 0;
        if (Math.abs(level) === 3) {
            intercept = 1;
        } else if (Math.abs(level) === 2) {
            intercept = 3;
        }
        const step = Math.pow(2, 5 - Math.abs(level))
        const l = [0, 16, 32, 40, 48, 52, 56, 58];
        let val;
        for (let i = 0; i < l.length; i++) {
            if (l[i] <= index) {
                val = l[i];
            }
        }
        return intercept + step * (index - val);
    };

    this.level = this.getLevel();
    this.row = this.getRow(this.level);

    this.draw = (row, level) => {
        const x = map_range(level, -6, 6, 0, 600);
        const y = map_range(row, -2, 17, 0, 600);

        let r = 10;
        if (level == 0) {
            r = 25;
        }
        circle(ctx, x, y, r, '#ff0000')
    };
    this.draw(this.row, this.level);
}
