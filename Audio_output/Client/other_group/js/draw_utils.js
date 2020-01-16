/*Carica nel DOM l'elemento SVG*/
function createSVG(width, height) {
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg")
    svg.setAttribute('width', width + "px")
    svg.setAttribute('height', height + "px")
    svg.setAttribute('id', 'svg')
    svg.setAttribute("z-index", 2)
    console.log(svg)
    document.body.appendChild(svg)
    return svg
}



/*Carica nel DOM il tag g (gruppo di elementi di tipo svg e.g circle,rect...)*/
function createGroup(svg, id) {
    var g = document.createElementNS("http://www.w3.org/2000/svg", "g")
    g.setAttribute('id', id)
    g.setAttribute('transform', 'scale(1)')
    svg.appendChild(g)
}


/*Crea un elemento di tipo circle e lo carica nel DOM*/
function createCircle(svg, cx, cy, r, fill, _class, _text, id) {
    var g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    g.setAttribute('class', _class)
    g.setAttribute('id', id)
    g.setAttribute('transform', 'translate(0 0)')
    circle.setAttribute('cx', cx)
    circle.setAttribute('cy', cy)
    circle.setAttribute('r', r)
    circle.setAttribute('fill', fill)

    var text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.innerHTML = _text
    text.setAttribute('x', cx)
    text.setAttribute('y', cy)
    text.setAttribute('text-anchor', 'middle')
    text.setAttribute('dy', '.3em')

    svg.appendChild(g)
    g.appendChild(circle)
    g.appendChild(text)
}


function drawBall(group, ball) {
    for (var b in ball)
        createCircle(group,
            from_meters_to_pixels_x(ball[b].position.x),
            from_meters_to_pixels_y(ball[b].position.y),
            15, 'white', 'ball', 'B_' + b, 'B_' + b)
}

function drawPlayers(group, info_players) {
    console.log(info_players)

    for (var p in info_players) {

        curr_player = _CURRENT_STATE[info_players[p]]['current_info']

        if (!curr_player.hasOwnProperty('team')) {
            createCircle(group,
                from_meters_to_pixels_x(curr_player.position.x),
                from_meters_to_pixels_y(curr_player.position.y),
                15, 'white', 'ball', info_players[p], info_players[p])
        } else {
            //Determina le informazioni da associare al giocatore/arbitro
            switch (curr_player.team.value) {
                case 0:
                    fill = 'blue';
                    _text = (curr_player.id.confidence >= 0.5) ? curr_player.id.value : '?';
                    _class = 'player';
                    id = 'P_' + _text + '_T_0';
                    break;
                case 1:
                    fill = 'red';
                    _text = (curr_player.id.confidence >= 0.5) ? curr_player.id.value : '?';
                    _class = 'player';
                    id = 'P_' + _text + '_T_1';
                    break;
                case -1:
                    fill = 'yellow';
                    _text = "Re"+ curr_player.id.value;
                    _class = 'referee';
                    id = 'P_' + curr_player.id.value + '_T_-1';
                    break;
            }

            //Aggiunge al DOM l'elemento
            createCircle(group,
                from_meters_to_pixels_x(curr_player.position.x),
                from_meters_to_pixels_y(curr_player.position.y),
                15, fill, _class, _text, id)
        }
    }
}