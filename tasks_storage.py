import queue

from configs import Config
from utils import do_another_task


class _TaskResponse:
    def __init__(self, id, out=None, error=None):
        self.id = id
        self.status = 'pending'
        self.answer = None
        self.error = None

        if error is None and out is not None:
            assert isinstance(out, str)
            self.answer = out
            self.status = 'OK'
        elif error is not None:
            assert isinstance(error, str)
            self.error = error
            self.status = 'error'

    def __str__(self):
        return (
            f'task_id: {self.id}\n'
            f'answer: {self.answer.strip()}\n' if self.answer else ''
            f'error: {self.error.strip()}' if self.error else ''
        )

    def body(self):
        if self.status == 'pending':
            return {'status': 'pending'}
        else:
            if self.answer is not None:
                return {
                    'status': 'OK',
                    'answer': self.answer,
                }
            elif self.error is not None:
                return {
                    'status': 'error',
                    'error': self.error,
                 }


class TasksStorage:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.task_responses = {}  # id: response
        self.cnt = 0

    def put_task(self, _id):
        self.task_queue.put(_id)

    async def get_task(self):
        while True:
            if self.cnt >= Config.MAX_TASKS:
                await do_another_task()
                continue
            try:
                _id = self.task_queue.get_nowait()
                self.cnt += 1
                return _id
            except:
                await do_another_task()
                continue

    def put_result(self, _id, out, error):
        self.task_responses[_id] = _TaskResponse(_id, out, error)
        self.cnt -= 1

    def get_result(self, _id):
        return self.task_responses.get(_id, _TaskResponse(_id))

    def print_result(self, _id):
        print(self.task_responses.get(_id))
