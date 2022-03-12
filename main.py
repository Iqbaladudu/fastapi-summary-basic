from fastapi import Body, FastAPI, Form, Header, Path, Query, File, UploadFile, Request, status
from enum import Enum
from pydantic import BaseModel

app = FastAPI()


@app.get("/ss")
async def hello_world():
    return {"hello": "world"}


@app.get("/users/{id}/")
async def gegt_users(id: int):
    return {"id": id}


@app.get("/users/{type}/{id}/")
async def geht_user(type: str, id: int):
    return {"type": type, "id": id}

# using Enum


class UserType(str, Enum):
    STANDARD = "standard"
    ADMIN = "admin"


@app.get("/{group}/{id}/")
async def get_user_by_group(group: UserType, id: int):
    return {"group": group, "id": id}

# Advanced Validation


@app.get("/students/{id}")
async def get_usger(id: int = Path(..., ge=1)):
    # Elipsis di dalam fungsi path memberitahu FastApi jika tidak ada default value. dan ia harus required
    # gt = Greater Than
    # ge = Greater than or equal to
    # lt = Less than
    # le = Less than or equal to
    return {"id": id}

# Regex validation


@app.get("/license-plates/{license}")
async def get_license_plates(license: str = Path(..., regex=r"^\w{2}-\d{3}-\w{2}$")):
    return {"license": license}


# Query parameters
@app.get("/users")
async def get_users(page: int = 1, size: int = 10):
    return {"page": page, "size": size}

# Required Query params


class DoiName(str, Enum):
    IRMA = "irma"
    NONE = "Tidak ada"


@app.get("/doi")
async def get_doi(nama: DoiName):
    return {"nama": nama}


# Query validation
@app.get("/alamat")
async def get_user(provinsi: str, id: int = Query(1, gt=0)):
    return {"provinsi": provinsi, "id": id}


# Request body
@app.post("/users")
async def create_user(name: str = Body(...), age: int = Body(...)):
    return {"name": name, "age": age}

# Using pydantic


class User(BaseModel):
    name: str
    age: int


@app.post("/usr")
async def create_usr(user: User = Body(...)):
    return user

# form data


@app.post("/register")
async def register(name: str = Form(...), age: int = Form(...)):
    return {"name": name, "age": age}


@app.post("/files")
async def upload_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {"file_name": file.filename, "content_type": file.content_type}


@app.get("/get-header")
async def get_header(hello: str = Header(...)):
    return {"hello": hello}


@app.get("/")
async def get_user_agent(user_agent: str = Header(...)):
    return {"user_agent": user_agent}


@app.get("/get-path")
async def get_request_object(request: Request):
    return {"path": request.url.path}

# status code


class Post(BaseModel):
    title: str


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    return post

# Response Model


class PostModel(BaseModel):
    title: str
    nb_views: int


# nb_views will be hidden from the response
posts = {
    1: PostModel(title="Hello", nb_views=100)
}


class PublicModel(BaseModel):
    title: str


@app.get("/posts/me/{id}", response_model=PublicModel)
async def get_post(id: int):
    return posts[id]
