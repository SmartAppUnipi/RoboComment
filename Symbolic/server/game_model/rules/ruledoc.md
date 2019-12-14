# Rules Symbolic Level
## Pressed
Describes whether the ball owner is under pressure
### Actions
- push
```javascript
{'type': 'player_pressed'}
```
## Not_pressed
Blah
### Actions
- push
```javascript
{'type':'possession',
 'time': <time>,
 'player': {'id': <id>,
 'team': <team> },
 'position': <position>,
 'until': <time>}
```
## Possession
Represents the possession
### Actions
- push
- consume
```javascript
{'type':'possession',
 'time': <time>,
 'player': {'id': <id>,
 'team': <team> },
 'position': <position>,
 'until': <time>}
```
