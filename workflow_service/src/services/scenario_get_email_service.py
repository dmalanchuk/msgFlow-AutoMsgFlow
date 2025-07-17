from fastapi import Request, HTTPException


class ScenarioGetEmailService:

    @staticmethod
    def get_user_email(request: Request) -> str:
        # Отримуємо email з request.state
        user_email = request.state.user_email if hasattr(request.state, "user_email") else request.headers.get("x-user-email")

        if not user_email:
            raise HTTPException(status_code=401, detail="User email not found")

        return user_email
