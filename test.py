import requests
import time


def test_put(code):
    id_ = requests.post('http://localhost:5000/put', data=code).text
    assert isinstance(id_, str) and len(id_) == 32
    return id_


def test_get(id_, true_answer=None, is_error=False, sleep_s=2):
    time.sleep(sleep_s)

    resp = requests.get(f'http://localhost:5000/get?id={id_}').json()
    if is_error:
        assert resp.get('status') == 'error'
        assert resp.get('error')
    else:
        assert resp.get('status') == 'OK'
        assert resp.get('answer').strip() == true_answer


def test_situation(code, true_answer=None, is_error=False, sleep_s=2):
    test_get(test_put(code), true_answer, is_error, sleep_s)


class Tests:
    def test_succes(self):
        test_situation('print(2+2)', '4')

    def test_error(self):
        test_situation('print(2+2', is_error=True)

    def test_n_tasks(self):
        ids = []
        for _ in range(5):
            ids.append(test_put('print(2+2)'))

        for id_ in ids:
            test_get(id_, '4', sleep_s=2)
