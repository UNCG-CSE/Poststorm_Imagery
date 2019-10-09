class User:

    id: str  # The user's unique authentication ID
    nickname: str  # The user's nickname
    role: str  # The user's role (may be str or int in implementation)

    def __str__(self):
        return self.get_id()

    def get_id(self):
        return self.id

    def get_nickname(self):
        return self.nickname

    def get_role(self):
        return self.role
