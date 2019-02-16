class UserModel:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getUser(self):
        return 'a user'
    
    def deleteUser(self):
        return 'user deleted'

    def addUser(self, username, password):
        return 'user added'+username+password