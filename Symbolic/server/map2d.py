import json
from flask_socketio import SocketIO, emit


class Map2d():

    def __init__(self,width,height,positions,socketio,debug=True):

        self.positions = positions
        self.init_position = positions 
        
        self.width = width
        self.height = height

        self.debug = debug
        self.client_connected = False

        self.socketio = socketio
        if not debug:
            self.socketio.on_event('notify',self._send_init_position)     
    
    def _get_map_json(self):
        return {
            'debug':self.debug,
            'width':self.width,
            'height': self.height,
            'positions':self.positions
        }
    
    def _get_init_position(self):
        return {
            'debug':self.debug,
            'width':self.width,
            'height': self.height,
            'positions':self.init_position
        }

    def _update_position(self,new_positions):
        self.positions = new_positions
        if self.client_connected:
            self.socketio.emit('update',data=self._get_map_json())
    
    def _send_init_position(self,msg=None):
        self.client_connected = True
        self.socketio.emit('new',data=self._get_init_position())

    def _clear_init_position(self,init_pos):
        self.init_position = init_pos
    


