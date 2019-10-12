import asyncio
import docker

import utils

from configs import Config


class TaskRunner:
    def __init__(self, tasks_storage):
        self.client = docker.from_env()
        self.tasks_storage = tasks_storage

    def _run_in_container(self, file):
        return self.client.containers.run(
            Config.IMAGINE_NAME,
            command="""python3 -c {}""".format(file),
            stdout=True, stderr=True,
        ).decode()

    async def run_task(self, _id):
        file = utils.get_script(_id)

        out, err = None, None

        try:
            out = self._run_in_container(file)
        except docker.errors.ContainerError as exc:
            err = exc.stderr.decode()

        self.tasks_storage.put_result(_id, out, err)

        self.tasks_storage.print_result(_id)


async def _task_scheduler(tasks_storage):
    task_runner = TaskRunner(tasks_storage)
    while True:
        _id = await tasks_storage.get_task()  # blocked

        asyncio.create_task(task_runner.run_task(_id))


def run_task_scheduler_async(tasks_storage):
    asyncio.run(_task_scheduler(tasks_storage))
