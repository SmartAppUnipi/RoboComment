var _CURRENT_STATE = {};

function get_dom_id(player) {
    return 'P_' + player.id.value + '_T_' + player.team.value
}

function get_ball_dom_id(id) {
    return 'B_' + id
}


function parse(data) {

    console.log("STAMPO PARSE");
    console.log(data);
    //console.log('DATA', data)

    var balls = data.positions.ball

    var players = data.positions.players
    
    //console.log('Players', players)
    console.log('CURRENT STATE', _CURRENT_STATE)
    
    var remove_list =[]
    for(var key in _CURRENT_STATE)
        remove_list.push(key)
        console.log(key)
    
    var rem = remove_list.slice()
    console.log('INITIAL REMOVE',rem)
    var new_list = []
    var update_list = []

    for (p in players) {
        p_id = get_dom_id(players[p])
        if (!_CURRENT_STATE.hasOwnProperty(p_id)) {
            _CURRENT_STATE[p_id] = {'initial_pos':players[p].position,
                                    'current_info':players[p]} 
          
            new_list.push(p_id)
         
        } else {
            _CURRENT_STATE[p_id]['current_info'] = players[p]
            update_list.push(p_id)
            remove_list.splice(remove_list.indexOf(p_id), 1);
        }
    }

    for (b in balls)
    {
        b_id = get_ball_dom_id(b)
        if (!_CURRENT_STATE.hasOwnProperty(b_id)) {
            _CURRENT_STATE[b_id] = {'initial_pos':balls[b].position,
                                    'current_info':balls[b]} 
          
            new_list.push(b_id)
         
        } else {
            _CURRENT_STATE[b_id]['current_info'] = balls[b]
            update_list.push(b_id)
            remove_list.splice(remove_list.indexOf(b_id), 1);
        }
    }

    for (e in remove_list) {
        delete _CURRENT_STATE[remove_list[e]]
    }

    //console.log('NEW_LIST', new_list)
    //console.log('UPDATE_LIST', update_list)
    //console.log('REMOVE_LIST', remove_list)
    //console.log('CURRENT STATE', _CURRENT_STATE)
    return {
        'new_list': new_list,
        'update_list': update_list,
        'remove_list': remove_list
    }


}