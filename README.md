<!-- Back to Top Navigation Anchor -->
<a name="readme-top"></a>

<!-- Project Shields -->
<div align="center">

  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]
  [![Twitter][twitter-shield]][twitter-url]
</div>

<!-- Project Logo -->
<br />
<div align="center">
  <a href="https://github.com/mike-eziefule/Ezzy-school_management_api">
    <img src="./images/ezzy school.png" alt="Logo" width="80%" height="20%">
  </a>
</div>

<br />

<div>
  <p align="center">
    <a href="https://github.com/mike-eziefule/Ezzy-school_management_api/blob/main/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://www.loom.com/share/ed3cc4bfb8c743cd9371e2831a7785ec?sid=4be6af19-e752-4289-a180-bf065c0bd58a">View Demo</a>
    ·
    <a href="https://github.com/mike-eziefule/Ezzy-school_management_api/issues">Report Bug</a>
    ·
    <a href="https://github.com/mike-eziefule/Ezzy-school_management_api/issues">Request Feature</a>
  </p>
</div
---

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-Ezzy-School_Manager">About Ezzy School Manager</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#lessons-learned">Lessons Learned</a>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>    
    <li><a href="#sample">Sample</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
  <p align="right"><a href="#readme-top">back to top</a></p>
</details>

---

<!-- About the Blog. -->
## About Ezzy-school_manager_api

This is a school manager API that helps educators manage all academic records and activities within their institution.
The app caters for three set of users; the administrator, the staff and the students.

All users are required to first sign up using a route specific to each user type by providing an email address and a password. Available user type includes "admin", "staff" and "student".

Upon signup, user should be able to login using the email address and password provided during signup.

All routes require users to be logged in before they can perform other functions. Some available functions includes:


#### 1. THE LECTURERS:

* Lecturers are to sign up using the staff signup route.

* Upon signup and login, lecturers will be able to create a profile by entering their firstname, lastname and gender. A unique staff number will be automatically generated afterwards.

* Lecturers can then add/create the course/courses he/she will be curating by entering the course title and course code. This action must be completed before students can register for the courses.

* Lecturers can edit any mistakes noticed during creation of course, this updated will be reflected across board.

* Lecturers can also delete their course, provided no students have registered yet. hence, it is advisable to conclude course upload before student registration starts.

* Lecturers can view students who registered for their course and grade those students accordingly.

* After grading, only admins can modify students results.

* strict restrictions have been placed to confine lecturers manipulations to their courses and students alone, ie, lecturer A cannot modify, delete or grade students of lecturer B.


#### 2. THE STUDENT:

* Students are to sign up using the student signup route.

* Upon signup and login, the student will be able to create a profile by entering their firstname, lastname, dob, origin and gender. A unique   matric number will be automatically generated afterwards.

* Students are required to register all courses he/she will offer by entering/selecting the course code, provided the course lecturer has uploaded the course. 

* Only registered courses can be graded by course lecturers, therefore, studentd who fail to register a course cannot get results.

* In event of mistakes during registration, the student can delete wrongly registered courses, provided such course hasnt been graded by the lecturer. However, his/her login password will be required.

* Students can view course information and details of assigned lecturer taking the course.

* Students can view results only when course lecturer has graded it.

* Students can view CGPA ONLY when ALL results of his/her registered courses have been graded.


#### 3. THE ADMIN:

* Administrators are to sign up using the admin signup route.

* Upon signup and login, the admin will be able to create a profile by entering their username and designation using the register admin route. A unique admin number will be automatically generated afterwards. 

* Admins can view detailed information of all students, all results, all lecturers registered on the platform.

* Admin alone can edit results in event of a mistake made. An modification will automatically be effected in the overall CGPA calculation of the student.

Ezzy School Manager was built by <a href="https://github.com/mike-eziefule/">Eziefule Michael</a>, a Backend Engineering student at <a href="https://engineering.altschoolafrica.com/">AltSchool Africa</a> who's learning to create magic with the Python FastAPI framework.

A tutorial on how this project was built is available in [Michael_Ezzy's Space](https://hashnode.com/draft/6539339dbe20a1000f0b5edd) on Hashnode.

<p align="right"><a href="#readme-top">back to top</a></p>

### Built With:

![Python][python]
![FastAPI][fastapi]
![SQLite][sqlite]

<p align="right"><a href="#readme-top">back to top</a></p>

---
<!-- Lessons from the Project. -->
## Lessons Learned

Creating this blog helped me learn and practice:
* The use of python for backend development
* Debugging
* Routing
* Database Management
* Internet Security
* User Authentication
* User Authorization
* Documentation

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- GETTING STARTED -->
## Usage

To get a local copy up and running, follow the steps below.

### Prerequisites

Python3: [Get Python](https://www.python.org/downloads/)

### Installation

1. Clone this repo
   ```sh
   git clone https://https://github.com/mike-eziefule/Ezzy-school_management_api.git
   ```
2. Activate the virtual environment(Bash on windows os)
   ```sh
   source virtualenv/Scripts/activate
   ```
3. Install project packages
   ```sh
   pip install -r requirements.txt
   ```
4. Run uvicorn
   ```sh
   uvicorn main:app --reload
   ```
5. Open the link generated in the terminal on a browser  
   ```sh
   http://127.0.0.1:8000/docs
   ```

### Alternatively
1. his Api has been hosted on render.com To test, follow the link below.

   ```sh
   https://ezzy-blog-api.onrender.com/docs
   ```

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Sample Screenshot -->
## Sample

<br />

[![Ezzy school screenshot pg1][Ezzy-school-screenshot-pg1]](https://github.com/mike-eziefule/Ezzy-school_management_api/blob/main/images/ezzyschool1.png)
[![Ezzy school screenshot pg2][Ezzy-school-screenshot-pg2]](https://github.com/mike-eziefule/Ezzy-school_management_api/blob/main/images/ezzyschool2.png)
[![Ezzy school screenshot pg2][Ezzy-school-screenshot-pg3]](https://github.com/mike-eziefule/Ezzy-school_management_api/blob/main/images/ezzyschool3.png)
[![Ezzy school screenshot pg2][Ezzy-school-screenshot-pg4]](https://github.com/mike-eziefule/Ezzy-school_management_api/blob/main/images/ezzyschool4.png)

<br/>

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- License -->
## License

Distributed under the MIT License. See <a href="https://github.com/mike-eziefule/Ezzy-school_management_api/blob/main/LICENSE">LICENSE</a> for more information.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Contact -->
## Contact

X [Formally Twitter] - [@EziefuleMichael](https://twitter.com/EziefuleMichael)

Project Link: [Ezzy_Blog_api](https://github.com/mike-eziefule/Ezzy_Blog_api)

Email Address: [mike.eziefule@gmail.com](mailto:mike-eziefule@gmail.com)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Acknowledgements -->
## Acknowledgements

This project was made possible by:

* [AltSchool Africa School of Engineering](https://altschoolafrica.com/schools/engineering)
* [Caleb Emelike's FastAAPI Lessons](https://github.com/CalebEmelike)
* [Ze-Austin AltSchool Python Repo](https://github.com/Ze-Austin/altschool-python)
* [GitHub Student Pack](https://education.github.com/globalcampus/student)
* [Canva](https://www.canva.com/)
* [Stack Overflow](https://stackoverflow.com/)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Markdown Links & Images -->
[contributors-shield]: https://img.shields.io/github/contributors/mike-eziefule/Ezzy_Blog_api
[contributors-url]: https://github.com/mike-eziefule/Ezzy-school_management_api/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mike-eziefule/Ezzy-school_management_api
[forks-url]: https://github.com/mike-eziefule/Ezzy-school_management_api/network/members
[stars-shield]: https://img.shields.io/github/stars/mike-eziefule/Ezzy-school_management_api
[stars-url]: https://github.com/mike-eziefule/Ezzy_Blog_api/stargazers
[issues-shield]: https://img.shields.io/github/issues/mike-eziefule/Ezzy-school_management_api
[issues-url]: https://github.com/mike-eziefule/Ezzy-school_management_api/issues
[license-shield]: https://img.shields.io/github/license/mike-eziefule/Ezzy-school_management_api
[license-url]: https://github.com/mike-eziefule/Ezzy-school_management_api/blob/main/LICENSE
[twitter-shield]: https://img.shields.io/twitter/follow/EziefuleMichael
[twitter-url]: https://twitter.com/EziefuleMichael
[Ezzy-school-screenshot-pg1]:images/ezzyschool1.png
[Ezzy-school-screenshot-pg2]:images/ezzyschool2.png
[Ezzy-school-screenshot-pg3]:images/ezzyschool3.png
[Ezzy-school-screenshot-pg4]:images/ezzyschool4.png
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[fastapi]: https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=black
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white