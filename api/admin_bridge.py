import requests

SERVER_URL = "http://127.0.0.1:8000/api/admin"

class AdminBridge:
    @staticmethod
    def get_dashboard():
        try:
            return requests.get(f"{SERVER_URL}/dashboard").json()
        except Exception:
            return {"total_users": 0, "active_users": 0, "blocked_users": 0, "pending_requests": 0, "issued_programs": 0, "active_licenses": 0}

    @staticmethod
    def list_requests():
        try: return requests.get(f"{SERVER_URL}/requests").json()
        except Exception: return []

    @staticmethod
    def approve_request(request_id, days, program_states):
        requests.post(f"{SERVER_URL}/requests/{request_id}/approve", json={"days": days, "program_states": program_states})

    @staticmethod
    def reject_request(request_id):
        requests.post(f"{SERVER_URL}/requests/{request_id}/reject")

    @staticmethod
    def list_users():
        try: return requests.get(f"{SERVER_URL}/users").json()
        except Exception: return []

    @staticmethod
    def update_license(user_id, days):
        res = requests.post(f"{SERVER_URL}/users/{user_id}/license", json={"days": days}).json()
        return res.get("expire_date", "LIFETIME")

    @staticmethod
    def update_user_programs(user_id, program_states):
        requests.post(f"{SERVER_URL}/users/{user_id}/programs", json=program_states)

    @staticmethod
    def toggle_block(user_id):
        requests.post(f"{SERVER_URL}/users/{user_id}/toggle-block")

    @staticmethod
    def get_programs():
        try: return requests.get(f"{SERVER_URL}/programs").json()
        except Exception: return []

    @staticmethod
    def get_user_programs(user_id):
        try: return {int(k): v for k, v in requests.get(f"{SERVER_URL}/user-programs/{user_id}").json().items()}
        except Exception: return {}