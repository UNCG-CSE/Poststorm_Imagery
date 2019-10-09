class User:

    id: str  # The user's unique authentication ID
    nickname: str  # The user's nickname
    role: str  # The user's role (may be str or int in implementation)

    def get_id(self):
        return self.id
