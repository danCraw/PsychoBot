from fastapi import HTTPException, status
from fastapi import Request
from jose import jwt, JWTError

SECRET_KEY = "your-secret-key"  # Секретный ключ для подписи и проверки JWT


async def authenticate(request: Request, call_next):
    token = request.headers.get("Authorization", "").split("Bearer ")[-1]
    try:
        payload = jwt.decode(token, SECRET_KEY)
        # Здесь можно добавить логику проверки данных из payload (например, проверку идентификатора пользователя)
        # и сохранить информацию о пользователе в зависимостях для использования в обработчиках

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response = await call_next(request)
    return response
