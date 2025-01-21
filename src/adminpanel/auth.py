from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from sqladmin.authentication import AuthenticationBackend

from src.database import get_async_session
from src.users.auth import auth_user, create_access_token
from src.users.dependencies import get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        async for session in get_async_session():
            user = await auth_user(session, email, password)
            if user:
                access_token = create_access_token({"sub": str(user.id)})
                request.session.update({"admin_access_token": access_token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Response | bool:
        token = request.session.get("admin_access_token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        async for session in get_async_session():
            user = await get_current_user(session, token)
            if not user:
                return RedirectResponse(request.url_for("admin:login"), status_code=302)
        return True


authentication_backend = AdminAuth(secret_key="...")
