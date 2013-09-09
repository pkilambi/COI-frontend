
ERROR   = '\033[91m'
OK      = '\033[92m'
WARNING = '\033[93m'
END     = '\033[0m'

def print_warn(text):
    print WARNING + text + END

def print_ok(text):
    print OK + text + END

def print_error(text):
    print ERROR + text + END

