from configs import Config


def get_script(id_) -> str:
    with open(f'{Config.SCRIPTS_PATH}/{id_}.py', 'r') as f:
        return f.read()


def save_script(id_: str, script: str):
    with open(f'{Config.SCRIPTS_PATH}/{id_}.py', 'w') as f:
        f.write(script)
