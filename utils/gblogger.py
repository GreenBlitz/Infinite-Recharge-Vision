import os


class GBLogger:
    def __init__(self, name, use_file=False, file_path=None):
        self.name = name
        self.use_file = use_file
        if use_file:
            if file_path is None:
                file_path = os.path.join(os.getcwd(), 'logs')
            os.makedirs(file_path, exist_ok=True)
            self.file = open(os.path.join(file_path, name + '.log'), 'w')
        self.allow_debug = False
        self.allow_info = True
        self.allow_warning = True
        self.allow_fatal = True

    def __log_to_file(self, msg):
        if self.use_file:
            self.file.write(msg + '\n')

    def __print(self, msg):
        print(msg)

    def __full_proc(self, msg, should_print):
        if should_print:
            self.__print(msg)
        self.__log_to_file(msg)

    def __prep(self, msg, msg_type):
        return f'[{msg_type}] {msg}'

    def debug(self, msg):
        self.__full_proc(self.__prep(msg, 'DEBUG'), self.allow_debug)

    def info(self, msg):
        self.__full_proc(self.__prep(msg, 'INFO'), self.allow_info)

    def warning(self, msg):
        self.__full_proc(self.__prep(msg, 'WARN'), self.allow_warning)

    def fatal(self, msg):
        self.__full_proc(self.__prep(msg, 'FATAL'), self.allow_fatal)
