# Rules Symbolic Level
## Send plain positions
Sends all the plainpositions of the actors involved in the action to the next level [audio_output_request] 
### Actions
- push to stdout
```javascript
{...}
```
## Penalty
Fires when detecting a penalty
### Actions
- push to stdout
```javascript
{'type': 'penalty',
 'time': <time>,
 'team': <team>,
 'start_time': <time>,
 'end_time': <time>}
```
## Player pressed
Describes whether the ball owner is under pressure
### Actions
- push to stdout
```javascript
{'type':'player_pressed',
 'time': <time>,
 'player': {'id': <id>,
 'team': <team> },
 'position': <position>,
 'until': <time>}
```
## Player not pressed
Fires when the ball owner is under pressure
### Actions
- push to stdout
```javascript
{'type':'player_not_pressed',
 'time': <time>,
 'player': {'id': <id>,
 'team': <team> },
 'position': <position>,
 'until': <time>}
```
## Possession
Fires when detecting a possession
### Actions
- push to elementary
- consume
## Pass
Fires when detecting a pass
### Actions
- push to elementary
- fpass
- int_stdout
```javascript
{'type': 'pass',
 'start_time': <time>,
 'end_time': <time>,
 'player_active': <player>,
 'player_passive': <player>,
 'time': <time>}
```
