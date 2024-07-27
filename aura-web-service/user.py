
class User:
    username = ""
    userID = ""
    aura = 100

    def __init__(self, username) -> None:
        self.username = username
        
    # Change value of variable
    def change_value(self, identifier, value):
        setattr(self, identifier, value)