from fastapi import FastAPI,Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from passlib.hash import bcrypt
from pymongo import MongoClient
from pydantic import BaseModel

class NotesOfFuture(BaseModel):
    title:str
    content:str
    quote:str
    writer_name:str
    designation:str
    university:str
    
# Initialize FastAPI and MongoDB
app = FastAPI()
templates = Jinja2Templates(directory="templates")
# components = Jinja2Templates(directory="templates/components")
app.mount(
    "/static", StaticFiles(directory="static"), name="static")
connection_string:str = "mongodb+srv://admin:thesisadmin@thesiscluster.056da.mongodb.net/"
client = MongoClient(connection_string)
# db = client["auth_db"]
# users_collection = db["users"]

# Helper function to find users
# def find_user_by_username(username):
#     return users_collection.find_one({"username": username})

@app.get("/", response_class=HTMLResponse)
async def serve_home(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/home_page", response_class=HTMLResponse)
async def serve_home(request:Request):
    return templates.TemplateResponse("components/home_page.html", {"request": request})

@app.get("/notes_of_future_page/",response_class=HTMLResponse)
async def new_page(request: Request):

    return templates.TemplateResponse("components/notes_of_future.html", {"request": request, "notes": fetch_future_notes()})

# @app.post("/signup/")
# async def signup(username: str = Form(...), password: str = Form(...)):
#     # Check if the user already exists
#     print(username)
#     if find_user_by_username(username):
#         raise HTTPException(status_code=400, detail="Username already exists")

#     # Hash the password and store user
#     hashed_password = bcrypt.hash(password)
#     print(hashed_password)
#     users_collection.insert_one({"username": username, "password": hashed_password})
#     return {"success": True, "message": "Signup successful"}

# @app.post("/login/")
# async def login(username: str = Form(...), password: str = Form(...)):
#     user = find_user_by_username(username)
#     if not user or not bcrypt.verify(password, user["password"]):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
    
#     return {"success": True, "message": "Login successful"}

    
def get_future_notes_collection_instance():
    future_notes_db = client['future_notes_db']
    future_notes_collection = future_notes_db['future_notes_collection']
    return future_notes_collection

@app.post("/createfuturenote/")
def create_future_note(note_details:NotesOfFuture):
    future_notes_collection = get_future_notes_collection_instance()
    future_notes_collection.insert_one({
    "title":note_details.title,
    "content":note_details.content,
    "quote":note_details.quote,
    "university":note_details.university,
    "designation":note_details.designation,
    "writer_name":note_details.writer_name
})
    return  {"success": True, "message": "Note Added Successfully"}

@app.get("/futurenotes/")
def fetch_future_notes():
    future_notes_collection = get_future_notes_collection_instance()
    future_notes=future_notes_collection.find()
    result = []
    for note in future_notes:
        
        result.append({'title':note['title'],'content':note['content'],'quote':note['quote'],'writer_name':note['writer_name'],'designation':note['designation'],'university':note['university']})
    return result