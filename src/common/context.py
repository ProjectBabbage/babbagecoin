import os
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


class NetworkContext:
    """Implement a singleton. NetworkContext() will always returns the exact
    same object instance."""

    instance: "NetworkContext" = None

    def __init__(self):
        if NetworkContext.instance is None:
            has_env_file = os.path.isfile(".env")

            self.myIp = get_my_ip() if has_env_file else "127.0.0.1"
            self.myUrl = f"http://{self.myIp}:5000"
            self.known_nodes = get_all_ips() if has_env_file else [self.myIp]
            self.sentry_dsn = get_sentry_dsn()

            NetworkContext.instance = self

    def __new__(cls):
        if cls.instance:
            return cls.instance
        return super().__new__(cls)


if __name__ == "__main__":
    # print("env variables in .env :", get_env_variables())
    print(id(NetworkContext().instance))
    print(id(NetworkContext()))
    a = NetworkContext()
    print(id(a))
