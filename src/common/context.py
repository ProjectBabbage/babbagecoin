from dotenv import dotenv_values


def get_env_variables():
    return dotenv_values(".env")


def get_my_ip():
    current_user = get_env_variables()["CURRENT_USER"]
    return get_env_variables()[f"IP_NODE_{current_user}"]


def get_sentry_dsn():
    """
    Return the sentry DSN for monitoring of logs using glitchtip (open source clone of sentry)
    """
    envs = get_env_variables()
    if "DSN_GLITCHTIP" in envs:
        return get_env_variables()["DSN_GLITCHTIP"]
    return None


def isIP(env_var):
    name, value = env_var
    if "IP_NODE" in name and value:
        return True
    return False


def get_all_ips():
    ips = []
    for _, ip in filter(isIP, get_env_variables().items()):
        ips.append(ip)
    return ips


class Context:
    def __init__(self):
        self.known_hosts = get_all_ips()
        self.myIp = get_my_ip()
        self.myUrl = f"http://{self.myIp}:5000"

    def build(self, myIp: str, known_hosts: list):
        self.myIp = myIp
        self.myUrl = f"http://{myIp}:5000"
        self.known_hosts = known_hosts


if __name__ == "__main__":
    print(get_env_variables())
    # print(get_all_ips())
