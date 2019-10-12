import asyncio

from src.configs import Config


def get_script(_id) -> str:
    with open(f'{Config.SCRIPTS_PATH}/{_id}.py', 'r') as f:
        return f.read()


def save_script(_id: str, script: str):
    with open(f'{Config.SCRIPTS_PATH}/{_id}.py', 'w') as f:
        f.write(script)


async def do_another_task():
    await asyncio.sleep(Config.DELAY_IN_ASYNC)
