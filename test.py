import time
import pytest
import requests

from main import app

use_mock_client = False


def text_accessor(obj):
    return obj.data.decode() if use_mock_client else obj.text

def json_accessor(obj):
    return obj.json if use_mock_client else obj.json()


@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True

    if use_mock_client:
        with app.test_client() as client:
            return client
    else:
       return requests


def _test_put(client_, code):
    _id = text_accessor(client_.post('http://localhost:5000/put', data=code))
    assert isinstance(_id, str) and len(_id) == 32
    return _id


def _test_get(client_, _id, true_answer=None, is_error=False, sleep_s=2):
    time.sleep(sleep_s)

    resp = json_accessor(client_.get(f'http://localhost:5000/get?id={_id}'))
    if is_error:
        assert resp.get('status') == 'error'
        assert resp.get('error')
    else:
        assert resp.get('status') == 'OK'
        assert resp.get('answer').strip() == true_answer


def _test_situation(client_, code, true_answer=None, is_error=False, sleep_s=2):
    _id = _test_put(client_, code)
    _test_get(client_, _id, true_answer, is_error, sleep_s)


def test_succes(client):
    _test_situation(client, 'print(2+2)', '4')


def test_error(client):
    _test_situation(client, 'print(2+2', is_error=True)


def test_n_tasks(client):
    ids = []
    for _ in range(5):
        ids.append(_test_put(client, 'print(2+2)'))

    for _id in ids:
        _test_get(client, _id, '4', sleep_s=2)
