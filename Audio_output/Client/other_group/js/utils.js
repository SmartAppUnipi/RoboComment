function init_pitch()
{
    //Disegno la mappa
    pitch = new Pitch(w, h)
    pitch.draw()

    svg = createSVG(w + 2 * border, h + 2 * border)
    return svg
}


function create_situation(svg,data)
{   
    if(!document.getElementById(_CONSTANTS.situation_id))
    {
   
       createGroup(svg,_CONSTANTS.situation_id)
    }     
    
    group = document.getElementById(_CONSTANTS.situation_id)
    data_dict = parse(data)
    
    new_list = data_dict['new_list']
    update_list = data_dict['update_list']
    remove_list = data_dict['remove_list']

    if(remove_list.length > 0)
        for(e in remove_list)
        {   
            console.log('REMOVE LIST ',remove_list)
            console.log('REMOVING ',remove_list[e])
            document.getElementById(remove_list[e]).remove()
        }
    if(new_list.length > 0)
        drawPlayers(group,new_list)

    if(update_list.length > 0)
        translate_players(update_list)
}

function translate_players(players)
{
    for(p in players)
    {   
        curr_player = _CURRENT_STATE[players[p]]
        dx = from_meters_to_pixels_x(curr_player['current_info'].position.x - curr_player['initial_pos'].x)
        dy = from_meters_to_pixels_y(curr_player['current_info'].position.y - curr_player['initial_pos'].y)
        document.getElementById(players[p]).setAttribute('transform','translate('+dx+" "+dy+')')
    }
}


