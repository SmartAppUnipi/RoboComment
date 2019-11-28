# Audio and Output group
### Requirements
```
cd /Server
nmp install
```
## 
### API

**Comment address and port**:
"fabula" on the routes.json file. 

**Method**:
POST with JSON data

**Success response code**:
200 OK

**Expected JSON data**:
 - comment: The text of the comment to be said.
 - emphasis: The emotion associated to the comment.
 - startTime: Starting time of the comment (seconds from the beginning of the video).
 - endTime: Ending time of the comment (seconds from the beginning of the video).
 - priority
 - id: user id

**Sample JSON data**:
```
{
    "comment": "Maradona scores goal with the hand"
    "emphasis": "rage"
    "startTime": 10
    "endTime": 15
    "priority": 1
    "id": 1
    "
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


Client:
- [x] Auto reconnection with servers (comments and video url)
- [x] Google API for text to speech
- [x] Managed the possible API response delay, sync with subtitles
- [ ] Improve GUI
- [x] Implement user login
- [ ] Implement video catalog
