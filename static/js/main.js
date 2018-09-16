/*
    Coordinatus
 */

console.log("Hello from Coordinatus");

class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

class Coordinates {
    constructor() {
        this.points = [];
        this.pointsR = 5.0;
        this.pointsColor = this.chooseColor();

        this.joinLineWidth = 2.0;
        this.joinLineColor = '#ECEFF1';

        this.pointsSubscribers = [];

        this.canvas = document.getElementById("canvas");
        this.updateWH();
        this.ctx = canvas.getContext('2d');

        let me = this;
        this.canvas.addEventListener('click', event => {
            me.addPoint(event.offsetX, event.offsetY);
        });

        this.drawPoints();
    }

    // just for fun function
    chooseColor() {
        const beautifulColors = [
            '#81C784',
            '#F48FB1',
            '#FFE082',
            '#90CAF9'
        ];
        let randomIdx = Math.floor(Math.random() * beautifulColors.length);
        return beautifulColors[randomIdx];
    }


    onPointsChange() {
        this.pointsSubscribers.forEach((fn, i, arr) => fn(this.points))
    }
    subscribeOnPointsChange(fn) {
        this.pointsSubscribers.push(fn);
        fn(this.points);
    }

    updateWH() {
        this.canvas.width = this.canvas.getBoundingClientRect().width;
        this.canvas.height = this.canvas.getBoundingClientRect().height;
    }

    clear() {
        this.ctx.clearRect(0,0, this.canvas.width, this.canvas.height);
    }
    drawPoints(clear = true) {
        if (clear) this.clear();
        this.ctx.fillStyle = this.pointsColor;

        this.points.forEach((p, i, arr) => {
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, this.pointsR, 0, 2*Math.PI);
            this.ctx.fill();
            this.ctx.closePath();
        })
    }
    joinPoints(points) {
        // check if points arrays is empty
        if (points.length <= 0) return;
        this.clear();
        this.ctx.strokeStyle = this.joinLineColor;
        this.ctx.lineWidth = this.joinLineWidth;

        this.ctx.beginPath();
        this.ctx.moveTo(points[0].x, points[0].y);
        for (let i = 1; i < points.length; i++) {
            this.ctx.lineTo(points[i].x, points[i].y);
        }
        this.ctx.lineTo(points[0].x, points[0].y);
        this.ctx.stroke();
        this.drawPoints(false);
    }
    addPoint(x, y) {
        for (let i = 0; i < this.points.length; ++i) {
            if (Math.abs(this.points[i].x - x) <= this.pointsR &&
                Math.abs(this.points[i].y - y) <= this.pointsR) {
                this.points.splice(i, 1);
                this.drawPoints();
                this.onPointsChange();
                return false;
            }
        }

        this.points.push(new Point(x, y));
        this.drawPoints();
        this.onPointsChange();
        return true;
    }
    addRandomPoints(quantity = 10) {
        let maxX = this.canvas.getBoundingClientRect().width - this.pointsR * 2;
        let maxY = this.canvas.getBoundingClientRect().height - this.pointsR * 2;
        for (let i = 0; i < quantity; ++i) {
            let x, y;
            do {
                x = Math.floor(Math.random() * maxX) + this.pointsR;
                y = Math.floor(Math.random() * maxY) + this.pointsR;
            } while(!this.addPoint(x, y));
        }
        this.drawPoints();
    }
    removePoints() {
        this.points.length = 0;
        this.clear();
        this.onPointsChange();
    }

    getJson() {
        return JSON.stringify(this.points);
    }
}

function request(url, data) {
    return new Promise(function (resolve, reject) {
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState === 4) {
                if (this.status === 200) {
                    resolve(this.response);
                } else {
                    reject(this.status)
                }
            }
        };
        xhttp.ontimeout = function() {
            reject('timeout');
        };
        xhttp.open('post', url, true);
        xhttp.setRequestHeader('Content-Type', 'application/json; charset=utf-8');
        xhttp.send(data);
    })
}

function buildJoin(coordinates) {
    const BUILD_JOIN = '/api/build_join';
    let sendPoints = request(BUILD_JOIN, coordinates.getJson());
    sendPoints
        .then(function getAnswer(answer) {
            let points = JSON.parse(answer);
            coordinates.joinPoints(points);
        })
        .catch(function onError(err) {
            console.error('Error during buildJoin()', err);
        });
}

let c = new Coordinates();

let pointsCounter = document.getElementById('points_counter');
c.subscribeOnPointsChange(function(points) {
    pointsCounter.innerText = points.length;
});

let clearBtn = document.getElementById('clear_btn');
clearBtn.onclick = () => c.removePoints();

let buildJoinBtn = document.getElementById('build_join_btn');
buildJoinBtn.onclick = () => buildJoin(c);

let addRandomBtn = document.getElementById('add_random_btn');
addRandomBtn.onclick = () => c.addRandomPoints();