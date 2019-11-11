# Audio and Output group
##Requirements
```
cd /Server
nmp install
```

##API

**Comment IP address**:

10.101.12.139:3003 (UniPisa net)

**Client-server websocket port (internal)**: 4000

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

**Sample JSON data**:
```
{
    "comment": "Maradona scores goal with the hand"
    "emphasis": "rage"
    "startTime": 10
    "endTime": 15
    "priority": 1 
}
```

##How to run the code

Server:
```
node Server/bin/www.js
```
Client web page:

```
Client/index.html
```