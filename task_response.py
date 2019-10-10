class TaskResponse:
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
