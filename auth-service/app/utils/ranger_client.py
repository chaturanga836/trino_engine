import os
import requests
from fastapi import HTTPException

# Load configuration from environment variables
RANGER_BASE_URL = os.getenv("RANGER_BASE_URL", "http://ranger-admin:6080")
RANGER_USER = os.getenv("RANGER_USER", "admin")
RANGER_PASSWORD = os.getenv("RANGER_PASSWORD", "ranger_admin_password")

def check_access(user: str, resource: str, action: str) -> bool:
    """
    Calls Apache Ranger REST API to check if a user has permission for a specific action.
    """
    try:
        # Example API call – adjust to match your Ranger policy setup
        url = f"{RANGER_BASE_URL}/service/plugins/policies"
        resp = requests.get(url, auth=(RANGER_USER, RANGER_PASSWORD), timeout=5)

        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Ranger API error: {resp.status_code}")

        policies = resp.json()

        for policy in policies:
            for item in policy.get("policyItems", []):
                users = item.get("users", [])
                accesses = [a.get("type") for a in item.get("accesses", [])]

                if user in users and action in accesses:
                    return True

        return False

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ranger request failed: {str(e)}")
