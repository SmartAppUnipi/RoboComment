# Comment Generation

## How to run it
``` 
pip3 install -r requirements.txt 
python3.6 CommentGenerator/app.py [AUDIO IP]
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
- **Expected Input** check  **assets/input1.json** 
- **Produced Output**   json with format:
    ```
    {
        "comment" : <string comment>,
        "emphasis" : <integer value>,
        "startTime" : <integer seconds>,
        "endTime" : <integer seconds>,
        "priority": <integer level from 0 to 5>
    } 
    ```
