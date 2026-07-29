from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as auth_router
from docs.routes import router as docs_router
from chat.routes import router as chat_router

app = FastAPI(title="Medical-Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(docs_router)
app.include_router(chat_router)

@app.get('/health')
def check_health():
    return {"message":"Ok"}