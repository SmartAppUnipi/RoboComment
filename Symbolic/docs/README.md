# APIs

Our **PORT** is 3001

## Video Processing

**Data are exchanged according to those "classes"**
```json
{
    "schemas": {
        "UncertainValue": {
            "value": "something",
            "confidence": "float (1 = totally certain, 0 = totally uncertain)"
        },
        "Coordinate": {
            "x": "float in meters",
            "y": "float in meters",
            "confidence": "float (1 = totally certain, 0 = totally uncertain)"
        },
        "Coordinate3D": {
            "x": "float in meters",
            "y": "float in meters",
            "z": "float in meters"
        }
    }
}
```

**URL** : `/positions/{int:timeframe}`

**Method** : `POST`

**Success Response Code** : `200 OK`

**Expected input**

```json
{
    "camera": {
        "position": "instance of Coordinate3D, is the position of the camera in the field",
        "target": "instance of Coordinate, is the position of the target of the camera on the field",
        "zoom": "float range TBD"
    },
    "players": [
        {
            "position": "instance of Coordinate",
            "speed": "instance of Coordinate",
            "id": "instance of UncertainValue with value = int that identifies the person",
            "team": "instance of UncertainValue with value = int 0 or 1"
        }
    ],
    "ball": [
        {
            "position": "instance of Coordinate",
            "speed": "instance of Coordinate",
            "midair": "float between 0 and 1 (0 = ground, 1 = surely flying)",
            "owner": "instance of UncertainValue where value is the index of the player in the 'players' field",
            "owner team": "instance of UncertainValue where value is 0 or 1"
        }
    ],
    "referee": [
        {
            "position": "instance of Coordinate",
            "pose": "TBD"
        }
    ]
}

```

**Notes** :
- x and y positions are a float with the meters with respect to the top left corner of the field.

## Comment Generation

### List of cathegories

```json
{
	"elementary":["pass","shot","holderMove","move","possession","cross","foul","duel","clearance","possession_lost","interception"],
	"scenario":["penalty","corner","offside","throwin","kickoff","free_kick","half_time","end_of_game"],
	"strategy":["counter-attack","melina","catenaccio","defence","attack"]
}
```