import os
from dotenv import load_dotenv

load_dotenv()


environment=os.getenv("ENVIRONMENT")


def get_full_uri():
  print(environment)
  if environment == "local":
    return {"frontend_url":"localhost:3000","backend_url":"localhost:8000"}
  elif environment == "production":
    return {"frontend_url":"localhost:3000","backend_url":"localhost:8000"}
  
  elif environment == "sandbox":
    return {"frontend_url":"localhost:3000","backend_url":"localhost:8000"}
