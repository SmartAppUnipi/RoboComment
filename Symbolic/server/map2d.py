import json
from flask_socketio import SocketIO, emit


class Map2d():

    def __init__(self,width,height,socketio):

        self.positions = {}
        self.init_position = {}
        
        self.width = width
        self.height = height

        self.client_connected = False

        self.socketio = socketio
    
        self.socketio.on_event('notify',self._new_connection)    

    def _get_current_positions(self):
        return {
            'width':self.width,
            'height': self.height,
            'positions':self.positions
        }
    
    def _get_init_position(self):
        return {
            'width':self.width,
            'height': self.height,
            'positions':self.init_position
        }

    def _update_position(self,new_positions):
        self.positions = new_positions
        if self.client_connected:
            self.socketio.emit('update',data=self._get_current_positions())
        else:
            self._clear_init_position(new_positions)
            self._send_init_position()
    
    def _send_init_position(self,msg=None):
        self.client_connected = True
        self.socketio.emit('new',data=self._get_init_position())

    def _clear_init_position(self,init_pos):
        self.init_position = init_pos
    
    def _new_connection(self,msg=None):
        if not self.positions == {}:
            self.socketio.emit('new',data=self._get_current_positions())
    


