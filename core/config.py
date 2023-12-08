import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / "settings.env"
load_dotenv(dotenv_path=env_path)


class Settings:
    #metadata needs
    TITLE = "Ezzy-School Management API"
    VERSION = "0.0.1"
    CONTACT = {
        'Name': 'Michael Eziefule',
        'Student ID': 'ALT/SOE/022/5063',
        'email': 'mike.eziefule@gmail.com',
        'github': 'https://github.com/mike-eziefule',
        'Location': 'Abuja, Nigeria'
    }
    DESCRIPTION = """### PROJECT OVERVIEW 
#### Welcome to my School Management Api.

* The fundamental concept is that anyone visiting the blog should be able to:
    * create an account, login and log out at will,
    * read blog posts written by them and/or other user,
    * create, edit and delete blog entries created by them but restricted from modifying or deleting posts from others users.
    * perform authentication where a user credentials is verified before they login.
    * perform authorization where a user cannot alter the intellectual property of others.
    * save registration details and blog posts created at all times.
    <a href="https://github.com/mike-eziefule/Ezzy_Blog_api/blob/main/README.md" target="_blank">Read more</a>*


##### Created in December 2023 for Altschool Africa

    """
    TAGS = [
        {'name': 'User',
        'description': 'Users routes'
        },
        {'name': 'Auth',
        'description': 'Login routes'
        },
        {'name': 'Admin', 
        'description': 'Administrators route'
        },
        {'name': 'Staff',
        'description': 'This is staff routes'
        },
        {'name': 'Student',
        'description': 'This are the Student related routes'
        },
        {'name': 'Others',
        'description': 'This routes can be accessed by all user groups'
        }
        ]
    SECRET_KEY = "ffec249609fbdbc97f82bfe593d1e45cec19ad2591af315096665512564df9af"
    ALGORITHM = "HS256"
    
    
    #databases needs
    School_code = os.getenv("School_code")
    Academic_year = os.getenv("Academic_year")
    faculty_code = os.getenv("faculty_code")
    staff_initials = os.getenv("Staff_code")
    matric_no = f"{School_code}{Academic_year}/{faculty_code}/"

setting = Settings()