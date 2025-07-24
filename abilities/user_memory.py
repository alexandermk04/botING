from data.database import get_user, update_user

class UserMemory:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def get_user_info(self) -> str:
        """Fetches information stored about the user."""
        user_info = get_user(self.user_id)
        if user_info:
            return f"User Info: {user_info['description']}"
        else:
            return "Nothing stored about this user."

    def store_user_info(self, description: str) -> str:
        """Stores information about the user. Overwrites existing data."""
        user_data = {"description": description}
        update_user(self.user_id, user_data)

        return "User information stored successfully."
