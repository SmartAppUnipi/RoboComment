from game_model.matcher import match

def test_simple_match_int():
    pattern = 7.00
    value = 7.00

    assert match(value, pattern)

    pattern = 8.00

    assert not match(value, pattern)


def test_simple_match_str():
    pattern = 'aaa'
    value = 'aaa'

    assert match(value, pattern)

    pattern = 'bbb'

    assert not match(value, pattern)


def test_simple_match_float():
    pattern = 7.50
    value = 7.50

    assert match(value, pattern)

    pattern = -0.0000009

    assert not match(value, pattern)


def test_obj_simple():
    value = {
        'x1': 5.00,
        'x2': 7.00
    }

    pattern = {
        'x1': 5.00,
        'x2': 7.00
    }

    assert match(value, pattern)

    pattern['x1'] = 12.00

    assert not match(value, pattern)

    value['x1'] = -0.12
    pattern['x1'] = value['x1']

    assert match(value, pattern)


def test_obj1():
    value = {
        'x1': {
            'x1.1': 0.12
        },
        'x2': -0.12
    }

    pattern = {
        'x1': {
            'x1.1': 0.12
        },
        'x2': -0.12
    }

    assert match(value, pattern)


def test_obj2():
    value = {
        'x1': {
            'x1.1': 0.12
        },
        'x2': {
            'x1.1': 0.12
        },
    }

    pattern = {
        'x1': {
            'x1.1': 0.12
        },
        'x2': {
            'x1.1': 0.12
        },
    }

    assert match(value, pattern)

def test_obj3():
    value = {
        'x1': {
            'x1.1': 0.12
        },
        'x2': {
            'x1.1': 0.12
        },
    }

    pattern = {
        'x1': {
            'x1.1': 0.12
        },
        'x2': {
            'x1.1': lambda x: x == 0.12
        },
    }

    assert match(value, pattern)


def test_obj3():
    value = {
        'x1': {
            'x1.1': 0.12
        },
        'x2': {
            'x1.1': 0.12
        },
    }

    pattern = {
        'x1': {
            'x1.1': 0.12
        },
        'x2': {
            'x1.1': '%<0.22'
        },
    }

    assert match(value, pattern)