from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.responses import RedirectResponse, JSONResponse
from arcade_app.auth_helper import (
    get_login_url, 
    exchange_github_code, 
    get_or_create_github_user, 
    create_session_token, 
    get_current_user
)

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.get("/login")
def login():
    """
    Returns the GitHub OAuth login URL to the frontend.
    Frontend should redirect here.
    """
    url = get_login_url()
    return {"url": url}

@router.get("/github/callback")
async def github_callback(code: str, response: Response):
    """
    Handles the OAuth callback from GitHub.
    Exchanges code for token, gets user info, creates session, and sets cookie.
    """
    try:
        gh_user = await exchange_github_code(code)
        user = await get_or_create_github_user(gh_user)
        
        # Create JWT Session
        token = create_session_token(user.id)
        
        # Set HttpOnly Cookie
        response = RedirectResponse(url="/")
        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True,
            max_age=60 * 60 * 24 * 7, # 7 days
            samesite="lax",
            secure=False # Set to True in Prod
        )
        return response
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Auth failed: {str(e)}")

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """
    Returns the currently logged in user context.
    """
    if not current_user:
        return {} # Return empty object if not logged in (frontend expects this or null)
    return current_user

@router.post("/logout")
def logout(response: Response):
    """
    Clears the session cookie.
    """
    response = JSONResponse(content={"status": "ok"})
    response.delete_cookie("session_token")
    return response
