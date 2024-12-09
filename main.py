from fastapi import FastAPI, Depends
from core.config import settings
from core.security import verify_token

app = FastAPI()

@app.get("/")
async def root():
   return {"app_configured": bool(settings.PRIVY_APP_ID)}

@app.get("/protected")
async def protected_route(token: str = Depends(verify_token)):
   return {"message": "You have access"}

@app.get("/check-privy")
async def check_privy():
   from core.security import get_privy_headers
   headers = get_privy_headers()
   return {
       "has_privy_config": bool(settings.PRIVY_APP_ID and settings.PRIVY_APP_SECRET),
       "headers_configured": "Authorization" in headers
   }