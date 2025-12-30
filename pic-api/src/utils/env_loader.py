from dotenv import dotenv_values

class EnvLoader():
    def __init__(self, env_file):
        # Create a dict with all the variables inside .env file
        self.envs_dict = dotenv_values(env_file)
        # A boolean useful to manage different behaviour if using localstack or not
        self.localstack = _is_localstack(self.envs_dict)
    
def _is_localstack(envs):
    try:
        ls = envs["LOCALSTACK_HOST"]
        return True
    except KeyError:
        return False

env_loader = EnvLoader(".env")

