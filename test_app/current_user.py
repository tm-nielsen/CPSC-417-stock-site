
class CurrentUser:
    __cu = None
    username = None
    type = None

    @staticmethod
    def get_instance():
        if CurrentUser.__cu is None:
            CurrentUser()
        return CurrentUser.__cu

    def __init__(self):
        if CurrentUser.__cu is not None:
            raise Exception("Current_User is a singleton class")
        else:
            CurrentUser.__cu = self

    def set_username(self, uname, t):
        self.username = uname
        self.type = t

    def get_username(self):
        return self.username

    def get_type(self):
        return self.type
