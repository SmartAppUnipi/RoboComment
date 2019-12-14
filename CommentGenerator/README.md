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

### POST an  action
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
