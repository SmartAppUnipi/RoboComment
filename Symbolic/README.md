# Symbolic Level Group

## Members
- Lorenzo Bellomo
- Andrea Bruno
- Michele Fontana
- Lorenzo Spano

## How to run our module

    $ pip install -r requirements.txt
    $ python server/app.py

## APIs

### Symbolic Level API (offered methods)

To be determined

### From Video Processing

**URL** : `/positions/{int:timeframe}`

**Method** : `POST`

**Success Response Code** : `200 OK`

**Expected input**

```json
{
    "players": [
        {
            "x": "int in [0, 100)",
            "y": "int in [0, 100)",
            "id": "(optional) int",
            "team": "(optional) int 1 or 2"
        }
    ],
    "ball": [
        {
            "x": "int in [0, 100)",
            "y": "int in [0, 100)",
            "owner": "(optional) int" 
        }
    ],
    "referee": [
        {
            "x": "int in [0, 100)",
            "y": "int in [0, 100)",
            "pose": "(optional) string" 
        }
    ]
}
```

**Notes** : x and y positions are expressed in percentage with respect to the whole field, where the point (0, 0) corresponds to the top left corner of the field.