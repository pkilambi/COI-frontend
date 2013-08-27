#!/usr/bin/python

class InstallerError(Exception):
    """
    Installer Exception wrapper
    """
    def __init__(self, message, exception):
        super(InstallerError, self).__init__(message, exception)
        self.message = message
        self.exception = exception

    def __str__(self):
        return repr(self.message) + ": " + repr(self.exception)


class COInstallerCLI():
    pass

