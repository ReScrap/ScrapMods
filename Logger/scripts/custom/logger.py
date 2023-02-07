import Scrap
import string

class Logger:

    def __init__(self, name):
        self.level = ""
        self.name = name

    def __repr__(self):
        return "<Logger: " + self.name + ">"

    def __str__(self):
        return self.__repr__()

    def __call__(self, *args):
        if string.find(self.level, "__") == 0:
            return

        args = list(args)

        for i in range(len(args)):
            args[i] = str(args[i])
            if args[i] == None:
                args[i] = ""

        args = ["[" + str(self.name) + "|" + string.upper(self.level) + "]"] + args
        msg = string.join(args, " ")
        Scrap.Print(msg + "\n")

    def __getattr__(self, level):
        self.level = level
        return self

    def __nonzero__(self):
        return True

    def __bool__(self):
        return True
