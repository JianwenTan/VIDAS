import os


class Acq_Base:

    def __init__(self, path_cache):
        self.pathCa = path_cache

    def clear_cache(self):
        for i in os.listdir(self.pathCa):
            os.remove(self.pathCa + "%s" % i)
        pass

    def img_check(self):
        if len(os.listdir(self.pathCa)) == 8:
            pass
            return 1
        else:
            return 0
