import platform


class Commands:

    if platform.system() == 'Darwin':
        # MacOs
        LINUX_JAVA_PROCESS_ID = 'pgrep Archi'
        LINUX_PROCESS_ID_PATH = 'lsof -a -d cwd -p {pid}'  # pid means "Process Identifier".
    else:
        # Debian, Ubuntu
        LINUX_JAVA_PROCESS_ID = 'pgrep java'
        LINUX_PROCESS_ID_PATH = 'pwdx {pid}'  # pid means "Process Identifier".
