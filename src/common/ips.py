from dotenv import dotenv_values


def get_env_variables():
    return dotenv_values(".env")


def get_my_ip():
    current_user = get_env_variables()["CURRENT_USER"]
    return get_env_variables()[f"IP_NODE_{current_user}"]


def get_sentry_dsn():
    """
    Monitoring of logs using glitchtip (open source clone of sentry)
    """
    return get_env_variables()[f"DSN_GLITCHTIP"]


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


if __name__ == "__main__":
    print(get_env_variables())
    # print(get_all_ips())
