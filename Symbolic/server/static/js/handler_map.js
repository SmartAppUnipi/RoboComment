//Contiene tutte e sole le informazioni iniziali degli elementi nella mappa
class InitialInfo {
    //misure in metri!!
    constructor(width, height, info) {
        this.width = width
        this.height = height
        this.info = info
        console.log('INIT_INFO: ', info)

    };

    get_player_by_id(id, team) {
        for (var p in this.info.players) {
            var player_id = this.info.players[p].id.value
            if (player_id == id && this.info.players[p].team.value == team)
                return this.info.players[p]

        }

        return null
    }

    get_ball() {
        return this.info.ball[0]
    }

    is_player_contained(id, team) {
        for (var p in this.info.players) {
            var player_id = this.info.players[p].id.value
            if (player_id == id && this.info.players[p].team.value == team)
                return true

        }

        return false
    }

    addPlayerInfo(player_info) {
        if (!this.is_player_contained(player_info.id.value, player_info.team.value)) {
            this.info.players.push(player_info)
        }
    }

}

//Converte da metri in pixels lungo l'asse x
function from_meters_to_pixels_x(init_info, pos, use_offset = true) {
    // 1200 : 120 = x : pos
    if (use_offset)
        return ((_CONSTANTS.pixels_width * pos) / init_info.width) + _CONSTANTS.pixels_border
    return (_CONSTANTS.pixels_width * (pos) / init_info.width)
}

//Converte da metri in pixels lungo l'asse y
function from_meters_to_pixels_y(init_info, pos, use_offset = true) {
    // 500 : 90 = x : pos
    if (use_offset)
        return ((_CONSTANTS.pixels_height * pos) / init_info.height) + _CONSTANTS.pixels_border
    return (_CONSTANTS.pixels_height * (pos) / init_info.height)

}

//Disegna i giocatori/arbitro aggiungendo i rispettivi elementi nel DOM (da chiamare solo al momento dell'aggiunta nel DOM)
function drawPlayers(init_info, info_players) {
    console.log(info_players)

    for (var p in info_players) {

        //Determina le informazioni da associare al giocatore/arbitro
        switch (info_players[p].team.value) {
            case 0:
                fill = 'blue';
                _text = (info_players[p].id.confidence >= 0.5) ? info_players[p].id.value : '?';
                _class = 'player';
                id = 'P_' + _text + '_T_0';
                break;
            case 1:
                fill = 'red';
                _text = (info_players[p].id.confidence >= 0.5) ? info_players[p].id.value : '?';
                _class = 'player';
                id = 'P_' + _text + '_T_1';
                break;
            case -1:
                fill = 'yellow';
                _text = "Ref";
                _class = 'referee';
                id = 'P_' + info_players[p].id.value + '_T_-1';
                break;
        }

        //Aggiunge al DOM l'elemento
        createCircle(document.getElementById('svg'),
            from_meters_to_pixels_x(init_info, info_players[p].position.x),
            from_meters_to_pixels_y(init_info, info_players[p].position.y),
            15, fill, _class, _text, id)
    }
}


//Disegna la palla e la aggiunge al DOM
function drawBall(init_info, ball) {
    for (var b in ball)
        createCircle(document.getElementById('svg'),
            from_meters_to_pixels_x(init_info, ball[b].position.x),
            from_meters_to_pixels_y(init_info, ball[b].position.y),
            15, 'white', 'ball', 'B_' + b, 'B_' + b)

}

//Inizializza la mappa, disegnando giocatori + arbitro
function init(w, h, info) {
    init_info = new InitialInfo(w, h, info)
    console.log('GET: ', w, h)
    console.log('INFO:', info)
    drawPlayers(init_info, info.players)
    drawBall(init_info, info.ball)
    return init_info
}

//Accede al DOM e restituisce, se esiste l'elemento con id P_id_T_team
function get_player_dom_element(id, team) {

    query = 'P_' + id + '_T_' + team
    //console.log(query)
    return document.getElementById(query)
}

function get_ball_dom_element() {
    return document.getElementById('B_0')
}

//Aggiorna la posizione della palla sul campo... (per il momento solo la prima...)
function updateBalls(init_info, positions) {
    balls = positions.ball

    for (var b in balls) {
        var ball = balls[b]
        init_x = init_info.get_ball().position.x
        init_y = init_info.get_ball().position.y

        new_x = ball.position.x
        new_y = ball.position.y

        ball_dom = get_ball_dom_element()

        dx = new_x - init_x
        dy = new_y - init_y

        move_x = from_meters_to_pixels_x(init_info, dx, false)
        move_y = from_meters_to_pixels_y(init_info, dy, false)
        ball_dom.setAttribute('transform', 'translate(' + move_x + ' ' + move_y + ')')
    }
}

//Aggiorna i giocatori sul campo
function updatePlayers(init_info, positions) {
    players = positions.players
    for (var p in players) {
        player = players[p]

        //Se non era già presente, aggiunge il nuovo giocatore sul campo
        if (!init_info.is_player_contained(player.id.value, player.team.value)) {
            drawPlayers(init_info, [player])
            init_info.addPlayerInfo(player)
            console.log('ADDED PLAYER: ', init_info)
        } else {

            //Se non sono sicuro dell'id (confidence <= 0.5) metto ? nel testo
            if (player.id.confidence <= 0.5) {
                target = get_player_dom_element(player.id.value, player.team.value)
                // console.log('INNER:', target.childNodes[1].innerHTML)
                target.childNodes[1].innerHTML = '?'

            } else {

                target = get_player_dom_element(player.id.value, player.team.value)
                //console.log('INNER GREAT:', target.childNodes[1].innerHTML)

                //Se sono l'arbitro con prob > 0.5, scrivo Ref nel testo
                if (player.team.value == -1 && player.team.confidence > 0.5)
                    target.childNodes[1].innerHTML = 'Ref'

                else //Altrimenti metto l'id del giocatore nel testo
                    target.childNodes[1].innerHTML = player.id.value
            }



            if (player.team.confidence <= 0.5) {
                //Non sono sicuro del team (prob <= 0.5) => Coloro il giocatore di marrone
                target = get_player_dom_element(player.id.value, player.team.value)
                target.childNodes[0].setAttribute('fill', 'brown')
            } else {

                switch (player.team.value) {
                    case 0: //Squadra 0 => blue
                        fill = 'blue';
                        break;
                    case 1: //Squadra 1 => rosso
                        fill = 'red';
                        break;
                    case -1: //Arbitro => Giallo
                        fill = 'yellow';
                        break;
                }

                target.childNodes[0].setAttribute('fill', fill)
            }

        }

        //Prendo le informazioni iniziali
        init_x = init_info.get_player_by_id(player.id.value, player.team.value).position.x
        init_y = init_info.get_player_by_id(player.id.value, player.team.value).position.y

        //Prendo le nuove posizioni
        new_x = player.position.x
        new_y = player.position.y

        player_dom = get_player_dom_element(player.id.value, player.team.value)

        dx = new_x - init_x
        dy = new_y - init_y

        //Aggiorno la mappa applicando una traslazione
        move_x = from_meters_to_pixels_x(init_info, dx, false)
        move_y = from_meters_to_pixels_y(init_info, dy, false)
        player_dom.setAttribute('transform', 'translate(' + move_x + ' ' + move_y + ')')

    }
}


$(document).ready(function () {


    w = _CONSTANTS.pixels_width
    h = _CONSTANTS.pixels_height
    border = _CONSTANTS.pixels_border

    //Disegno la mappa
    pitch = new Pitch(w, h)
    pitch.draw()

    svg = createSVG(w + 2 * border, h + 2 * border)
    init_info = null

    //Vari listeners....
    var socket = io()
    socket.on('connect', function () {
        console.log('Connected!')
        document.getElementById('svg').innerHTML = ''
        socket.emit('notify', {
            data: 'I\'m connected!'
        });
    });

    socket.on('new', function (data) {
        console.log('DATA_NEW:', data.width, data.height)
        init_info = init(data.width, data.height, data.positions)
        console.log(init_info.get_player_by_id(2, 1))

    });

    socket.on('update', function (data) {
        console.log('DATA_UPDATE:', data.positions)
        updatePlayers(init_info, data.positions)
        updateBalls(init_info, data.positions)

    });

});

