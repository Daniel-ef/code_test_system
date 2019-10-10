import docker

import utils

from configs import Config
from task_response import TaskResponse


def task_scheduler(task_queue, task_responses):
    client = docker.from_env()
    while True:
        try:
            id_ = task_queue.get_nowait()
        except:
            continue

        file = utils.get_script(id_)

        out, err = None, None

        try:
            out = client.containers.run(
                Config.IMAGINE_NAME,
                command="""python3 -c {}""".format(file),
                stdout=True, stderr=True,
            ).decode()
        except docker.errors.ContainerError as exc:
            err = exc.stderr.decode()

        task_responses[id_] = TaskResponse(id_, out, err)

        print(task_responses[id_])
