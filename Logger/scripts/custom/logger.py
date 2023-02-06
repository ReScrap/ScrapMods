import Scrap

class Logger:

    def __init__(self, name):
        self.level=""
        self.name=name

    def __repr__(self):
        return "<Logger>"

    def __call__(self, *args):
        # frame = sys.modules[__name__].last_frame
        # frame_info = (frame.f_code.co_name,frame.f_code.co_name)
        # Scrap.Print(repr(frame_info)+"\n")
        args=list(args)

        for i in range(len(args)):
            args[i]=str(args[i])

        args = ["["+str(self.name)+"|"+string.upper(self.level)+"]"]+args

        msg = string.join(args," ")

        Scrap.Print(msg+"\n")

    def __getattr__(self, level):
        self.level=level
        return self
