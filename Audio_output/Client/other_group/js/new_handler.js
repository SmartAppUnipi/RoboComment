//Converte da metri in pixels lungo l'asse x
function from_meters_to_pixels_x(pos, use_offset = true) {
    // 1200 : 120 = x : pos
    if (use_offset)
        return ((_CONSTANTS.pixels_width * pos) / _CONSTANTS.meters_width) + _CONSTANTS.pixels_border
    return (_CONSTANTS.pixels_width * (pos) / _CONSTANTS.meters_width)
}

//Converte da metri in pixels lungo l'asse y
function from_meters_to_pixels_y(pos, use_offset = true) {
    // 500 : 90 = x : pos
    if (use_offset)
        return ((_CONSTANTS.pixels_height * pos) / _CONSTANTS.meters_height) + _CONSTANTS.pixels_border
    return (_CONSTANTS.pixels_height * (pos) / _CONSTANTS.meters_height)

}


$(document).ready(function () {

    w = _CONSTANTS.pixels_width
    h = _CONSTANTS.pixels_height
    border = _CONSTANTS.pixels_border
    svg = init_pitch()

  
    // //Vari listeners....
    // var socket = io()
    //  socket.on('connect', function () {
    //     console.log('Connected!')
    //     document.getElementById('svg').innerHTML = ''
    //     socket.emit('notify', {
    //         data: 'I\'m connected!'
    //     });
    // });
    //
    // socket.on('update', function (data) {
    //     console.log('DATA_UPDATE:', data.positions)
    //     create_situation(svg,data)
    //
    //
    // });
    //
    // socket.on('new', function (data) {
    //     //console.log('DATA_NEW:', data.positions)
    //     create_situation(svg,data)
    //
    //
    // });

});