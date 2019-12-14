import pytest
from app import app

def test_setup():
    app.config['TESTING'] = True
    client = app.test_client()
    res = client.get("/")
    print(res)
    # assert(True == True)
