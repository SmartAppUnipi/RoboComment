/****
 * TODO:
 * - Definire per bene la struttura dati da utilizzare per la mappa => Struttura campi dizionario???
 * 
 * - Per l'aggiornamento: il server può informare il client con un evento che la struttura delle posizioni 
 *   è cambiata? => Evitare quindi il fetch da parte del client!
 * 
 * - Come gestire gli id???  Corrispondenza id => elemento + gestione id mancanti
 * 
 * - Gestire in modo proporzionale gli spostamenti/posizioni nel modello (1 metro == ? pixels??)
 * 
 * - Migliorare struttura codice 
 * 
 * - Migliorare struttura DOM
 * 
 * - Id su palle (grado di incertezza)
 * - Mettere arbitro (team = -1)
 * - Input: metri float
 * - Json video processing
 * - 
 */


SVG_NS = 'http://www.w3.org/2000/svg'
_RADIUS = 20
_TEAM_0_COL = 'blue'
_TEAM_1_COL = 'red'
_BALL_COL = 'white'
_N_PLAYERS = 11
_N_TEAMS = 2
_N_BALLS = 1

animating = false
interval = null
/***----------------FUNZIONI USATE SOLO PER DEBUG!!!!!-------*/

/*Genera numeri casuali in [min,max]*/
function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
}

/*Richiede al server le nuove posizioni ed aggiorna le posizioni degli elementi a schermo*/
async function debug_retrieve()
{
    var data = await fetch_position()
    var positions = data[0]
    for(var key in positions)
    {
        document.getElementById(key).setAttribute('cx',positions[key]['position']['x']+getRandomArbitrary(-30,30))
        document.getElementById(key).setAttribute('cy',positions[key]['position']['y']+getRandomArbitrary(-30,30))
    }
}

/*Avvia / stoppa l'animazione dell'aggiornamento casuale*/
function debug_animate()
{
    animating = !animating
    if(animating)
        interval = window.setInterval(debug_retrieve,1000)
    else
        window.clearInterval(interval)
}   

/*Aggiunge un bottone nel DOM. Se premuto, avvia/stoppa l'animazione dell'aggiornamento*/
function add_debug_btn()
{
    var btn = document.createElement('button')
    btn.style.width = '150px'
    btn.style.height = '75px'
    btn.innerHTML = 'Debug'
    btn.style.position = 'absolute'
    btn.style.top = '100px'
    btn.style.left = '1200px'
    document.getElementById('banner').appendChild(btn)

    btn.onclick = debug_animate
}

/*-------------------END DEBUG-------------------*/

/*Richiede al server le posizioni */
async function fetch_position() {

    var response = await  fetch("/debug/positions", { method: 'GET' })
    var data = await response.json()
    positions = data['positions']
    height = data['height']
    width = data['width']
    return [positions,width,height]    
}

/*Carica nel dom i cerchi che rappresentano giocatori + palla*/
function load_circles(positions) {
    circle = null
    for (i = 0; i < _N_TEAMS; i++) {
        for (j = 0; j < _N_PLAYERS; j++) {
            console.log('player_' + j + '_T_' + i)
            pos = (positions['player_' + j + '_T_' + i]['position'])
            console.log(pos)
            console.log(pos['x'])
            if (i == 0)
                circle = createCircle(document.getElementById('group'), pos['x'], pos['y'],
                    _RADIUS, _TEAM_0_COL, 'player_' + j + '_T_' + i)
            else
                circle = createCircle(document.getElementById('group'), pos['x'], pos['y'],
                    _RADIUS, _TEAM_1_COL, 'player_' + j + '_T_' + i)
        }
    }

    pos = positions['ball']['position']
    circle = createCircle(document.getElementById('group'), pos['x'], pos['y'],
        _RADIUS, _BALL_COL, 'ball')
}


/*Carica nel DOM la mappa del campo + giocatori*/
async function load_map() {

    var data = await fetch_position()
    var positions = data[0]
    var width = data[1]
    var height = data[2]
    console.log(positions)
    load_image(width, height)
    document.getElementById("map").onload = function () {
        svg = createSVG()
        document.getElementById("banner").appendChild(svg)
        createGroup(svg, 'group')
        load_circles(positions)
        add_debug_btn()
    }
}

/*Carica nel DOM l'elemento SVG*/
function createSVG() {
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg")
    var w = $('#map').width()
    var h = $('#map').height()
    console.log(w, h)
    svg.setAttribute('width', w)
    svg.setAttribute('height', h)
    svg.setAttribute('id', 'svg')
    console.log(svg)
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
function createCircle(svg, cx, cy, r, fill, id) {
    var g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute('cx', cx)
    circle.setAttribute('cy', cy)
    circle.setAttribute('r', r)
    circle.setAttribute('fill', fill)
    circle.setAttribute('id', id)

    svg.appendChild(g)
    g.appendChild(circle)
}


/*Carica l'immagine del campo nel DOM e ne setta le dimensioni*/
function load_image(width, height) {
    document.getElementById("map").data = "/static/img/field.png"
    document.getElementById("map").style.width = width
    document.getElementById('map').style.height = height
}



$(document).ready(function () {
    load_map()
    document.getElementById("map").onload = function () {
        svg = createSVG()
        document.getElementById("banner").appendChild(svg)

    }
})

