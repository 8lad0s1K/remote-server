import requests

SERVER_URL = "http://127.0.0.1:8000/api/admin"

class UserManager:
    def list_users(self, search_nickname="", search_hwid="", status_filter="all", order_by="id", descending=False):
        try: 
            users = requests.get(f"{SERVER_URL}/users").json()
        except Exception: 
            return []
            
        if search_nickname:
            users = [u for u in users if search_nickname.lower() in u["nickname"].lower()]
        if search_hwid:
            users = [u for u in users if search_hwid.lower() in u["hwid"].lower()]
        if status_filter == "active":
            users = [u for u in users if u["active"]]
        elif status_filter == "blocked":
            users = [u for u in users if not u["active"]]
        return users

    def get_user(self, user_id: int):
        users = self.list_users()
        for u in users:
            if u["id"] == user_id: return u
        return None

    def toggle_block(self, user_id: int):
        try: requests.post(f"{SERVER_URL}/users/{user_id}/toggle-block")
        except Exception: pass

    def delete_user(self, user_id: int):
        pass

    def update_license(self, user_id: int, days=None):
        try:
            res = requests.post(f"{SERVER_URL}/users/{user_id}/license", json={"days": days}).json()
            return res.get("expire_date", "LIFETIME")
        except Exception:
            return "LIFETIME"

    def update_user_programs(self, user_id: int, program_states: dict):
        try: requests.post(f"{SERVER_URL}/users/{user_id}/programs", json=program_states)
        except Exception: pass

user_manager = UserManager()
