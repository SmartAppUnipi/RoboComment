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
- **URL**  /api/action
- **Expected Input** check  **assets/input_symbolic1.json** 
- **Produced Output**   json with format:
    ```
    {
        "comment" : <string comment>,
        "emphasis" : <integer value>,
        "startTime" : <integer seconds>,
        "endTime" : <integer seconds>,
        "priority": <integer level from 0 to 5>,
        "id" : <int with the user id>
    } 
    ```
- ## Beta 
    - **method** PUT 
    - **URL** api/action
    - **Expected input** need to tune with symbolic
    - **Produced Output**   json with format:
        ```
        {
            "comment" : <a string with the produced comment>,
            "emphasis" : <?? we need to think about that>,
            "startTime" : <integer seconds, the start time we recive from the symbolic level >,
            "endTime" : <integer seconds, the end time we receive from the symbolic level>,
            "priority": <float from 0 to 10 stating the importance of the comment, 10 is extremely important, 0 is not important>,
            "user_id" : <int with the id of the user who has to receive this comment>
        } 
        ```
### Start a comment session
- **URL** /api/session/<<int:matchid>>/<<int:userid>>
- **method** POST
- **effect** the I/O module should call this method to inform us that a user with userid wants a commentary for the match matchid


### End a comment session
- **URL** /api/session/<<int:matchid>>/<<int:userid>>
- **method** DELETE
- **effect** the I/O module should call this method to inform us that a user with userid is no longer wathing the match matchid