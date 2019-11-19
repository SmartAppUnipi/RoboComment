import json
import random 

_N_PLAYERS = 11
_N_TEAMS = 2
_N_BALLS = 1

def build_fake_map(width,height):

    fake_data = {}

    for i in range(_N_TEAMS):
        for j in range(_N_PLAYERS):

            if i == 0:
                fake_data["player_{}_T_{}".format(j,i)] = {'position':
                            {
                                'x':random.randrange(10,width / 2),
                                'y':random.randrange(10,height),
                            }
                        }
            else:
                fake_data["player_{}_T_{}".format(j,i)] = {'position':
                            {
                                'x':random.randrange(width / 2,width),
                                'y':random.randrange(10,height),
                            }
                        }
    
    fake_data["ball"] = {'position':
                        {
                            'x':random.randrange(10,width),
                            'y':random.randrange(10,height),
                        }
                    }

    return fake_data

class Map2d():

    def __init__(self,width,height,positions):

        self.postions = {}
        self.width = width
        self.height = height

        for i in range(_N_TEAMS):
            for j in range(_N_PLAYERS):
               self.positions = positions

    def _get_map_json(self):
        return {
            'width':self.width,
            'height': self.height,
            'positions':self.positions
        }

if __name__ == "__main__":
   
    print(build_fake_map())
    map = Map2d(100,300,build_fake_map())
    print(json.dumps(map._get_map_json(), indent=4)) 

