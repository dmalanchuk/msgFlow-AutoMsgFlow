from fastapi import Request, HTTPException


class ScenarioGetEmailService:

    @staticmethod
    def get_user_email(request: Request) -> str:
        
        user_email = getattr(request.state, "user_email", None) or request.headers.get("x-user-email")
        if not user_email:
            raise HTTPException(status_code=401, detail="User email not found")

        return user_email
