var canvas,
    context,    // canvas context
    is_drawing = false,
    dragLastLocation,   // last drawn coords
    empty_result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  // clear prediction's table
    api_path = "127.0.0.1/api/predict";


// get coords from canvas
function getCanvasCoordinates(event) {

    let x = event.clientX - canvas.getBoundingClientRect().left,
        y = event.clientY - canvas.getBoundingClientRect().top;

    return {x: x, y: y};
}

function drawLine(position) {

    context.beginPath();
    context.moveTo(dragLastLocation.x, dragLastLocation.y);
    context.lineTo(position.x, position.y);
    context.stroke();
}

// start drawing
function dragStart(event) {

    is_drawing = true;
    dragLastLocation = getCanvasCoordinates(event);
}

// draw
function drag(event) {

    if (is_drawing === true) {

        let position = getCanvasCoordinates(event);
        drawLine(position);
        dragLastLocation = position;

    }
}

// stop drawing
function dragStop(event) {

    if (is_drawing === true) {
        is_drawing = false;
        let position = getCanvasCoordinates(event);
        drawLine(position);
        predict(); // change prediction's table

    }
}

// mouse left canvas
function dragLeave(event) {

    is_drawing = false
}

// restart drawing
function clear_canvas() {

    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);
    update_value(empty_result) // clear prediction's table
}

// update prediction's table
function update_value(prediction_array) {

    for (let i = 0; i < 10; i++) {

        document.getElementById("td_" + i).textContent = prediction_array[i].toFixed(5);
    }
}

//prediction
function predict() {

    let img = canvas.toDataURL('image/png');

    $.ajax({
        type: "GET",
        url: api_path,
        data: {
            image: img
        },
        success: function (data) {
            update_value(data["prediction"])
        },
        error: function(){
            update_value(empty_result)
        }
    });

}

function init() {

    document.getElementById("clear_button").onclick = clear_canvas;
    document.getElementById("predict_button").onclick = predict

    canvas = document.getElementById("canvas");
    canvas.height = 280;
    canvas.width = 280;
    context = canvas.getContext('2d');
    context.strokeStyle = 'black';
    context.lineWidth = 10;
    context.lineCap = 'round';

    clear_canvas();
    canvas.addEventListener('mousedown', dragStart, false);
    canvas.addEventListener('mousemove', drag, false);
    canvas.addEventListener('mouseup', dragStop, false);
    canvas.addEventListener('mouseleave', dragLeave, false)

}


window.addEventListener('load', init, false);