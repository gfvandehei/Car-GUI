class Logger(object):
    """ A class to standardize logging outputs"""

    def __init__(self, name: str, view_level: int):
        self.view_level = view_level
        self.name = name

    def print_debug_msg(self, level: int, message: str):
        """Used to print leveled debug messages, if the message is below above the given level it will print"""
        if level > self.view_level:  # this message is too low a level to print
            return
        print("[{}][DEBUG {}]: {}".format(self.name, self.view_level, message))

    def print_status_message(self, level, message):
        if level > self.view_level:
            return
        print("[{}][STATUS {}]: {}".format(self.name, self.view_level, message))

    def print_initialization_message(self, component: str):
        print("[{}][INITIALIZATION]: {} has initialized".format(self.name, component))

    def print_error_message(self, level: int, error_msg: str):
        if level > self.view_level:
            return
        print("[{}][ERROR {}]: {}".format(self.name, level, error_msg))