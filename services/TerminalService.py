import sys, termios, tty


class TerminalService:
    def __init__(self):
        self.initial_options = termios.tcgetattr(sys.stdin)
        self.pty = False

    def restore_tty(self):
    	termios.tcsetattr(sys.stdin, termios.TCSANOW, self.initial_options)

    def set_raw_mode(self):
    	tty.setraw(sys.stdin.fileno())
