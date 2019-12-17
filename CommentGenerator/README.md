# Comment Generation

## How to run it
``` 
pip3 install -r requirements.txt 
# the app MUST be started in the RoboComment directory
python3.6 CommentGenerator/app.py 
```
## How to test it
```
pytest CommentGenerator/tests
```

## API
### Check if the server is alive
- **URL** /api
- **method** GET

### POST an  action/event from the symbolic level
- ## Beta 
    - **method** POST 
    - **URL** api/action
    - **Expected input** json with format:
    ```
    {
        "match_id" : <the int id of the match that is analyzed>,
        "match_url" : <the URI of the video clip>,
        "type" : < the type of the action, if this value is 'positions' the json content will be used to display the minimap>,
        "start_time" : <int seconds, start time of the action>,
        "end_time : <int seconds, end time of the action>,

        <the other values here are a bit dependent on the 'type' field
        you can see some examples under tests/mock_assets>
    }
    ```
    - **return status code**
        - 400 BAD REQUEST if there are no 'match_id' and 'clip_uri'
        - 200 if ok
    - **Produced Output**   json with format:
        ```
        {
            "comment" : <a string with the produced comment>,
            "language": < string value between 'it' and 'en'>,
            "voice" : < a string we get from KB user info, it is the user preference about the voice>
            "emphasis" : <1, 3, 5 meaning happy, neutral, angry>,
            "startTime" : <integer seconds, the start time we recive from the symbolic level >,
            "endTime" : <integer seconds, the end time we receive from the symbolic level>,
            "priority": <float from 0 to 10 stating the importance of the comment, 10 is extremely important, 0 is not important>,
            "id" : <int with the id of the user who has to receive this comment>
        } 
        ```
    
### Start a comment session
- **URL** /api/session/<<int:userid>>
- **expected json**
```
{   
    "match_id" : < the int id of the match >
    "start_time" : < the time in seconds from which the user starts watching the match>
    "match_url" : <the URI of the video clip the user is watching> 
}
```
- **method** POST
- **effect** the I/O module should call this method to inform us that a user with userid wants a commentary for the match matchid
- **return status codes** 
    - 200 if we already have the resource in cache, so the videogroup shouldn't be involved. The resource is in cache if we already processed the same matchid and clip_uri
    - 201 if it's the first time we manage that match, the video group should be informed to start processing the video


### End a comment session
- **URL** /api/session/<<int:userid>>
- **method** DELETE
- **effect** the I/O module should call this method to inform us that a user with userid is no longer wathing the match