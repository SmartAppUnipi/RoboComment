## Knowledge Base

##### Members
- Bettels Dennis
- Numeroso Danilo
- Varagnolo Davide

### Dependency
- NodeJS

### How to run our module
```
cd kb ; npm install
npm run build && npm run start
```

### Rest API

__URL__: ```/persona/:id```

__Method__: ```GET```

__Response Codes__: ``` 200 | 400 ```

__Successful Response__: 
```json 
{
  "id": 5,
  "first_name": "Andrea",
  "last_name": "Pirlo",
  "date_of_birth": "1970-12-22T00:00:00.000+01:00",
  "career": [
    {
      "year": "2003-2004",
      "roles": [
        {
          "type": "player",
          "shirt_number": 21,
          "at": {
            "name": "ACM",
            "city": "Milan",
            "palmares": [
              {
                "name": "UCL",
                "year": "2003-2004"
              }
            ],
            "stadium": {
              "name": "San Siro",
              "capacity": 70000
            }
          }
        }
      ]
    }
  ]
}
```

__URL__: ```/club/:id```

__Method__: ```GET```

__Response Codes__: ``` 200 | 400 ```

__Successful Response__: 
```javascript 
{
    "name": "ACM",
    "city": "Milan",
    "palmares": [
        {
            "name": "UCL",
            "year": "2003-2004"
        }
    ],
    "stadium": {
        "name": "San Siro",
        "capacity": 70000
    }
}
```

__URL__: ```/cup/:id```

__Method__: ```GET```

__Response Codes__: ``` 200 | 400 ```

__Successful Response__: 
```javascript 
[
    {
        "name": "UCL",
        "year": "2003-2004"
    },
    {
        "name": "UCL",
        "year": "2004-2005"
    },
    ...
]
```
__URL__: ```/cup/:id/:season```

__Method__: ```GET```

__Response Codes__: ``` 200 | 400 ```

__Successful Response__: 
```javascript 
[
    {
        "name": "UCL",
        "year": "2003-2004"
    }
]
```

__URL__: ```/match/:home/:away/:date```

__Method__: ```GET```

__Response Codes__: ``` 200 | 400 ```

__Successful Response__: 
```javascript 
[
    {
        "home": {
            "name": "JUV",
            "city": "Turin",
            "palmares": [],
            "stadium": {
                "name": "Nameless",
                "capacity": 10000
            }
        },
        "away": {
            "name": "LEC",
            "city": "Lecce",
            "palmares": [],
            "stadium": {
                "name": "Nameless",
                "capacity": 30000
            }
        },
        "result": [
            0,
            0
        ],
        "date": "2004-05-08T00:00:00.000+02:00",
        "home_team": [{persona}, ...],
        "away_team": [{persona}, ...]
    }
]
```


__URL__: ```/users/:id```

__Method__: ```GET```

__Response Codes__: ``` 200 | 400 ```

__Successful Response__: 
```javascript 
{
    "id": 1,
    "first_name": "first",
    "last_name": "last",
    "date_of_birth": "11/11/11",
    "email": "example@example.com",
    "favourite_team": "Napoli"
}
```

__URL__: ```/users/```

__Method__: ```POST```

__Behaviour__: ```CREATE USER```

__Response Codes__: ``` 200 | 400 ```

__Body__: 
```javascript 
{
    "users": {
        "first_name": "first",
        "last_name": "last",
        "date_of_birth": "11/11/11",
        "email": "example@example.com",
        "favourite_team": "Napoli"
    }
}
```

__Successful Response__: 
```javascript 
{
    "id": <new_id>,
    "first_name": "first",
    "last_name": "last",
    "date_of_birth": "11/11/11",
    "email": "example@example.com",
    "favourite_team": "Napoli"
}
```

__URL__: ```/users/```

__Method__: ```PUT```

__Behaviour__: ```UPDATE USER```

__Response Codes__: ``` 200 | 400 ```

__Body__: 
```javascript 
{
    "users": {
        "id": 1,
        "first_name": "first1",
        "last_name": "last1",
        "date_of_birth": "11/11/11",
        "email": "example@example.com",
        "favourite_team": "Napoli"
    }
}
```

__Successful Response__: 
```javascript 
{
    "id": 1,
    "first_name": "first1",
    "last_name": "last1",
    "date_of_birth": "11/11/11",
    "email": "example@example.com",
    "favourite_team": "Napoli"
}
```


__URL__: ```/users/:id```

__Method__: ```DELETE```

__Response Codes__: ``` 200 ```
