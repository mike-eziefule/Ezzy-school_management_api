from core.config import setting
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.dbmodel import Base
from database.database import engine
from router.user_route import user_app
from router.admin_route import adm_app
from router.auth_route import auth_app
from router.gen_route import gen_app
from router.lect_route import lect_app
from router.stud_route import stud_app


#read metadata, and instructing it to create tables using base schema.
Base.metadata.create_all(bind=engine)

#FastAPI Matadata.
app = FastAPI(  
    title = setting.TITLE, 
    description = setting.DESCRIPTION,
    contact= setting.CONTACT,
    version= setting.VERSION,
    openapi_tags= setting.TAGS
)

#remove middleware restriction when hosting api
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

#connecting routes to main.py file
app.include_router(user_app, prefix='/user', tags=['User'])
app.include_router(auth_app, prefix='/auth', tags=['Auth'])
app.include_router(adm_app, prefix='/admin', tags=['Admin'])
app.include_router(gen_app, prefix='/misc', tags=['Others'])
app.include_router(lect_app, prefix='/staff', tags=['Staff'])
app.include_router(stud_app, prefix='/student', tags=['Student'])
