from dotenv import dotenv_values

# Create a dict with all the variables inside .env file
envs_dict = dotenv_values(".env")

# A boolean useful to manage different behaviour if using localstack or not
def get_localstack():
    try:
        ls = envs_dict["LOCALSTACK_HOST"]
        return True
    except KeyError:
        return False

localstack = get_localstack()