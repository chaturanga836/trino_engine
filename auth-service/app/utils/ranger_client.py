import requests
from fastapi import HTTPException

RANGER_BASE_URL = "http://ranger-admin:6080"  # internal Docker hostname
RANGER_USER = "admin"
RANGER_PASSWORD = "ranger_admin_password"

def check_access(user, resource, action):
    """
    Calls Ranger API to check if user has permission for a specific action.
    """
    url = f"{RANGER_BASE_URL}/service/public/v2/api/policy"
    resp = requests.get(url, auth=(RANGER_USER, RANGER_PASSWORD))
    if resp.status_code != 200:
        raise HTTPException(status_code=500, detail="Ranger unavailable")
    
    policies = resp.json()
    for policy in policies:
        for perm in policy.get("policyItems", []):
            if user in perm.get("users", []) and action in perm.get("accesses", []):
                return True
    return False
