import os


class Config:
    ROOT_DIR = os.path.abspath(os.path.realpath(__file__) + '/../')

    SCRIPTS_PATH = ROOT_DIR + '/scripts/'
    IMAGINE_NAME = 'ya_contest'
    MAX_TASKS = 5
    DELAY_IN_ASYNC = 0.001
