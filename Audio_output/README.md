# Audio and Output group
### Requirements
```
cd /Server
nmp install
```
## 
### API
#### Comments:

**Comment address and port**:
"fabula" on the routes.json file. 

**Method**:
POST with JSON data

**Success response code**:
200 OK

**Expected JSON data**:
 - comment: The text of the comment to be said.
 - emphasis: A value for the emotion associated with the comment.
 
    - 1: low excitement
    - 3: medium excitement
    - 5: high excitement
 - startTime: Starting time of the comment (seconds from the beginning of the video).
 - endTime: Ending time of the comment (seconds from the beginning of the video).
 - priority: A comment that overlap the previous is discarded unless it has higher priority.
 - language: The language of the comment.
 - voice: The name of the google API voice.
 - id: Id of the user that has to receive the comment.

**Sample JSON data**:
```
{
    "comment": "Maradona scores goal with the hand",
    "emphasis": 3,
    "startTime": 10,
    "endTime": 15,
    "priority": 1,
    "language": "en",
    "voice": "en-US-Wavenet-D",
    "id": 1
}
```

## 
### Video group message
**Sample JSON**
```
{
    "match_id": 10,
    "match_url": "https://someurl/video.mp4",
    "user_id": 1
}
```

## 
### How to run the code

Server:
```
node Server/bin/www.js
```
Client web page:

```
Client/login.html
```

##
### To Do list

Server:
- [x] Multi client support
- [x] Priority manager for comments
- [x] Messages forward to other services
- [x] Send comments based on user ID
- [x] User connection/disconnection warning to Commentary

Client:
- [x] Auto reconnection with server
- [x] Google API for text to speech
- [x] Managed the possible API response delay, sync with subtitles
- [ ] Improve GUI
- [x] Implement user login
- [x] Implement video catalog
- [x] Manage cookies
- [x] MultiLingual voice
- [x] Multi voice
- [ ] More Emphasis
- [ ] Green filed of position
- [ ] Cache play
