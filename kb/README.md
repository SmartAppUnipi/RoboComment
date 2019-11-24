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
npm run dev
```

### How to run the test suite
```
npm run test
```

### Rest API

__URL__: ```/persona/:id```

__Method__: ```GET```

__Response Codes__: ``` 200 | 404 ```

__Successful Response__: 
```javascript 
{
	"id": 11156,
	"name": "M. Trotta",
	"club": "FC Crotone",
	"height": "188",
	"date_of_birth": "1992-09-29"
}
```

__URL__: ```/club/:id```

__Method__: ```GET```

__Response Codes__: ``` 200 | 404 ```

__Successful Response__: 
```javascript 
{
	"id": 3161,
	"country": "Italy",
	"city": "Milano",
	"name": "FC Internazionale Milano"
}
```

__URL__: ```/match/:id```

__Method__: ```GET```

__Response Codes__: ``` 200 | 404 ```

__Successful Response__: 
```javascript 
{
	"home": {
		"id": 3162,
		"name": "SS Lazio"
	},
	"away": {
		"id": 3161,
		"name": "FC Internazionale Milano"
	},
	"result": ["2", "3"],
	"home_team": [{
		"id": "130",
		"name": "S. de Vrij",
		"club": 3162,
		"role": "Defender"
	}, {
		"id": "20550",
		"name": "",
		"club": 3162,
		"role": "Defender"
	}, {
		"id": "376362",
		"name": "Luiz Felipe",
		"club": 3162,
		"role": "Defender"
	}, {
		"id": "21384",
		"name": "C. Immobile",
		"club": 3162,
		"role": "Forward"
	}, {
		"id": "166534",
		"name": "T. Strakosha",
		"club": 3162,
		"role": "Goalkeeper"
	}, {
		"id": "20561",
		"name": "S. Luli",
		"club": 3162,
		"role": "Midfielder"
	}, {
		"id": "228928",
		"name": "A. Maru",
		"club": 3162,
		"role": "Midfielder"
	}, {
		"id": "265865",
		"name": "S. Milinkovi",
		"club": 3162,
		"role": "Midfielder"
	}, {
		"id": "7965",
		"name": "Lucas Leiva",
		"club": 3162,
		"role": "Midfielder"
	}, {
		"id": "346908",
		"name": "A. Murgia",
		"club": 3162,
		"role": "Midfielder"
	}, {
		"id": "40806",
		"name": "Felipe Anderson",
		"club": 3162,
		"role": "Midfielder"
	}],
	"away_team": [{
		"id": "21094",
		"name": "D. D'Ambrosio",
		"club": 3161,
		"role": "Defender"
	}, {
		"id": "135903",
		"name": "Jo",
		"club": 3161,
		"role": "Defender"
	}, {
		"id": "138408",
		"name": "M. ",
		"club": 3161,
		"role": "Defender"
	}, {
		"id": "3431",
		"name": "Jo",
		"club": 3161,
		"role": "Defender"
	}, {
		"id": "206314",
		"name": "M. Icardi",
		"club": 3161,
		"role": "Forward"
	}, {
		"id": "20571",
		"name": "S. Handanovi",
		"club": 3161,
		"role": "Goalkeeper"
	}, {
		"id": "116349",
		"name": "M. Vecino",
		"club": 3161,
		"role": "Midfielder"
	}, {
		"id": "14812",
		"name": "I. Peri",
		"club": 3161,
		"role": "Midfielder"
	}, {
		"id": "20556",
		"name": "A. Candreva",
		"club": 3161,
		"role": "Midfielder"
	}, {
		"id": "69968",
		"name": "M. Brozovi",
		"club": 3161,
		"role": "Midfielder"
	}, {
		"id": "3344",
		"name": "Rafinha",
		"club": 3161,
		"role": "Midfielder"
	}]
}
```


__URL__: ```/users/login```

__Method__: ```POST```

__Response Codes__: ``` 200 | 400 ```

__Body__: 
```javascript 
{
    "login": {
        "email": "",
        "password": ""
    }
}
```
__Successful Response__: 
```javascript 
{
    "id": 1
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
        "password": "xxxx",
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
