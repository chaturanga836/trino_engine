from fastapi import APIRouter, Depends, HTTPException
from app.utils.auth import verify_jwt
from app.utils.ranger_client import check_access

router = APIRouter()

@router.get("/query")
def run_query(token: str = Depends(verify_jwt)):
    user = token["sub"]
    action = "select"
    resource = "trino_query"

    allowed = check_access(user, resource, action)
    if not allowed:
        raise HTTPException(status_code=403, detail="Access denied by Ranger")

    return {"message": f"Query executed for {user}"}
