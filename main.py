from flask import Flask, request

import threading
import uuid
import queue

from task_scheduler import task_scheduler
from task_response import TaskResponse
import utils

app = Flask(__name__)


task_queue = queue.Queue()
task_responses = {}  # id: response

threading.Thread(target=task_scheduler,
                 args=(task_queue, task_responses,),
                 ).start()


@app.route('/put', methods=['POST'])
def put():
    id_ = uuid.uuid4().hex

    utils.save_script(id_, request.data.decode())

    task_queue.put(id_)
    return id_


@app.route('/get', methods=['GET'])
def get():
    id_ = request.args.get('id')
    task_response = task_responses.get(id_, TaskResponse(id_))

    return task_response.body()
