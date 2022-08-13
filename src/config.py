import os
from dotenv import dotenv_values, load_dotenv

# always load the envs variables
load_dotenv()


def get_env_variables():
    return dotenv_values(".env")


def get_my_ip():
    return os.environ.get(f"IP_NODE_{os.environ.get('CURRENT_USER')}")


def get_sentry_dsn():
    """
    Return the sentry DSN for monitoring of logs using glitchtip (open source clone of sentry)
    """
    return os.environ.get("DSN_GLITCHTIP")


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


class Config:
    """Implement a singleton. Config() will always returns the exact
    same object instance."""

    instance: "Config" = None

    def __init__(self):
        if Config.instance is None:
            if os.environ.get("TESTING") or not os.path.isfile(".env"):
                self.myIp = "127.0.0.1"
                self.known_nodes = [self.myIp]
                self.sentry_dsn = None
            else:
                self.myIp = get_my_ip()
                self.known_nodes = get_all_ips()
                self.sentry_dsn = get_sentry_dsn()
            self.redis_pub_sub = os.environ.get("REDIS_PUB_SUB")
            self.myUrl = f"http://{self.myIp}:5000"

            Config.instance = self

    def __new__(cls):
        if cls.instance:
            return cls.instance
        return super().__new__(cls)


if __name__ == "__main__":
    print(id(Config().instance))
    print(id(Config()))
    a = Config()
    print(id(a))
    # always the same object
    print(os.environ.get("TESTING"))
