# Maintis Feed 

### Purpose
MantisFeed was my version of a Reddit-style discussion platform where users are able to share discuss and vote on content. Some features include a karma-base point system, comments, top-post and cetegories.

### Target Audience
- Tech enthusiasts looking to share and discuss industry news
- Users looking for topic-focused discussions
- Creators wanting to share and get feedback

## Project Overview
- #### UX
- #### Agile Development
- #### Features
- #### Technologies Used
- #### Testing
- #### Deployment
- #### Credits

## UX 
- ### Strategy
#### Site Owner goals 
- Create active discussion community
- Facilitate meaningful content sharing and discussion
- Interactive features to maintain user engagement.
- Build self-moderating system through user voting
#### User Goals 
- Share and discover intresting content
- Topic-focused discussions
- Using karma point system build a good reputaion
- easy navigation through content by categories
- ### Desgin
I had an idea what i wanted to the page to look like. Which I build as a simple web page with css and html. 
![image](https://github.com/user-attachments/assets/d37dbb95-3777-47d4-a78a-586321029c61)
#### Color Scheme 
Nature inspired color palette, CSS:
```css
--primary-green: #064e3b
--accent-green: #059669
--light-green: #d1fae5
--dark-green: #022c22
--text-light: #ecfdf5
--text-dark: #065f46
```
#### Typography 
- Primate font: Inter. Secondary font: sans-serif.
- ### WireFrames 
- ### Data Schema
- ### Entity Relation Diagram
![image](https://github.com/user-attachments/assets/1cc346c5-d911-4165-9c62-7a4b32a2344d)

## Agile Development
- ### Link to project board (github projects
- ### User stories
- ### MOSCOW prioritization 

## Features

### Exisiting Features
- #### Nav + header
- #### All features with CRUD fuctionaility
- #### User registration and login
- #### Response / feedback messages

### Future Features 
- #### Respons / like comments
- #### Add images to posts_create and post_list

## Technologies Used

### Languages

- #### HTML
- #### CSS
- #### Python

### Frameworks & libarires 
- #### Django
- #### Database (Postgresql / MYSQL)

### Tools & Programs 
- #### Github
- #### Visual Studio Code
- #### Canva & Adobe editor

### Testing 
#### Code Validation 
- #### CSS Validation
- #### Python Validation

#### Manual testing 

- ### Early Admin manual testing
Ran the server using Python manage.py runserver. If this worked added /admin to url and logged in as superuser. Here I could test creating new users and posts. This early manual testing made sure 
that the models.py were working correctly. 

- #### Creating users 
![image](https://github.com/user-attachments/assets/1e6612e9-e39b-4f6a-a4a6-d0f30344b03f)
![image](https://github.com/user-attachments/assets/6e12f180-68db-44ee-b8b1-e5fa503f0a60)


- #### Creating posts
![image](https://github.com/user-attachments/assets/d8477367-ea56-4040-bf98-a7fd018f44dd)
![image](https://github.com/user-attachments/assets/e4677b36-3218-464d-b6cf-30652262f86b)


- #### Testing URL
Templates still to be created, but can see the path is working as it should
![image](https://github.com/user-attachments/assets/c10763ff-810a-48f9-9d16-83fe20b5c49c)

- #### Putting it together
Created a simple post_list.html to make sure everything is working.
![image](https://github.com/user-attachments/assets/db553aea-95f3-4b5e-a4b4-9c907d4b631b)



- Brower compatibility
- Navigation testing
- CRUD functionaility testing
- Authentication Testing

### Bugs

#### Fixed 
#### Known Issues


## Deployment
### Step-by-step deployment instructions:
- Create a github repository and clone it to local or virutal IDE.
- Setup virtiual envionment - python -m venv venv or source venv/bin/activate
- Install Django - pip install django
- Instal database - pip install psycopg2-binary dj-database-url
- Create requirements.txt - pip freeze > requirements.txt
- Create Django project - django-admin startproject mantisfeed .
- Create main apps - python manage.py startapp posts and python manage.py startapp accounts
- Update mantisfeed/settings.py - Add app to installed apps. Update database to add own data_base url

### Adding Database 
- create env.py
- add os.environ.setdefault("DATABASE_URL", "YOUR DATABASE_url")
- add "DATABASE_URL" to mantisfeed/settings.py
- add env.py to gitignore

### Additional packages for later development
- pip install django-allauth - for later authentication
- pip install Pillow - for image handeling
- pip install django-crispy-forms - form styling
- pip install gunicorn - for deployment
- pip install whitenoise - for static files

### Adding static CSS
- Setup a static/css/style.css file system in the root file
- Setup settings.py to configure the static files.
- In base.html use { % load static % } to access css in html.
- Finally, run python mamange.py collectstatic. 


## Credits 




