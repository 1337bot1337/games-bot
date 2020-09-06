import os

import environ


CORE_ROOT = environ.Path(__file__) - 1

env_file = os.path.join(CORE_ROOT, 'config', 'settings', '.env')

env = environ.Env()
environ.Env.read_env(env_file)
