# Comment Generation

## How to run it
``` 
pip3 install -r requirements.txt 
python3.6 app.py [AUDIO IP]
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
