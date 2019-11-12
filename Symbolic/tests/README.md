# Tests

## How to run our tests

    $ cd Symbolic
    $ pip3 install -r requirements.txt
    $ python3 -m pytest

## dummy.json

dummy.json contains a JSON array with some objects useful for doing testing. A description of each entry is provided below. To use any of those objects just index it as follows.

Objects belong to those cathegories: **Positions**, **Events**

0. All fields filled (**Positions**)
1. Some optional fields missing (**Positions**)
2. All fields filled (**Events**, elementary event: pass)
