VERSION = '1.2'

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
}

SHELL_STABILIZATION_METHODS = {
    'python': {
        'bash': """python -c 'import pty; pty.spawn("/bin/bash")'""",
        'sh': """python -c 'import pty; pty.spawn("/bin/bash")'"""
    },
    'python3': {
        'bash': """python3 -c 'import pty; pty.spawn("/bin/bash")'""",
        'sh': """python3 -c 'import pty; pty.spawn("/bin/sh")'"""
    },
    'script': {
        'bash': 'script -qc /bin/bash /dev/null',
        'sh': 'script -qc /bin/sh /dev/null'
    }
}
