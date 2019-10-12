from flask import Flask, request

import threading
import uuid

from task_scheduler import run_task_scheduler_async
from tasks_storage import TasksStorage
import utils

app = Flask(__name__)

tasks_storage = TasksStorage()


threading.Thread(target=run_task_scheduler_async,
                 args=(tasks_storage,),
                 ).start()


@app.route('/put', methods=['POST'])
def put():
    _id = uuid.uuid4().hex

    utils.save_script(_id, request.data.decode())

    tasks_storage.put_task(_id)
    return _id


@app.route('/get', methods=['GET'])
def get():
    _id = request.args.get('id')
    task_response = tasks_storage.get_result(_id)

    return task_response.body()
