# Maintis Feed 

### Purpose
MantisFeed was my version of a Reddit-style discussion platform where users are able to share discuss and vote on content. Some features include a karma-base point system, comments, top-post and cetegories.

### Target Audience
- Tech enthusiasts looking to share and discuss industry news
- Users looking for topic-focused discussions
- Creators wanting to share and get feedback

## Project Overview
- [UX](#ux)
- [Agile Development](#agile-development)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)

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
##### I had an idea what i wanted to the page to look like. Which I build as a simple web page with css and html. 
![image](https://github.com/user-attachments/assets/d37dbb95-3777-47d4-a78a-586321029c61)
#### Color Scheme 
##### Nature inspired color palette, CSS:
```css
--primary-green: #064e3b
--accent-green: #059669
--light-green: #d1fae5
--dark-green: #022c22
--text-light: #ecfdf5
--text-dark: #065f46
```
#### Typography 
##### Primate font: Inter. Secondary font: sans-serif.
- ### WireFrames
- ### Data Schema
#### Models 
1. **UserProfile**
   ```python
   - User (OnetoOne -> user)
   - bio (textfield)
   - karma (interfield)
   - Profile_picture(imagefield)
   ```
2. **Posts**
   ```python
   - title (charfield)
   - content (textfield)
   - created_at (datetimefield)
   - updated_at (datetimefield)
   - author (foreignkey -> user)
   - upvotes (ManyToMany -> user)
   - downvotes (ManyToMany -> user)
   ```
3. **Comments**
   ```python
   - content (textfield)
   - created_at (datetimefield)
   - update_at (datetimefield)
   - author (foreignkey -> user)
   - post (foreignkey -> post)
   - parents (foreignkey -> parents)
4. **Categories**
   ```python
   - name (charfield)
   - description (textfield)
   - created_at(datetimefield)
   ```

 ### Entity Relation Diagram
![image](https://github.com/user-attachments/assets/1cc346c5-d911-4165-9c62-7a4b32a2344d)

## Agile Development
- ### Link to project board (github projects)
  Created a new project, which could add new issues to
- ### User stories
  Created usser stories in the issues section on github. Added a user stort template:
   ```
   As a role I can capability so that received benefit

   Acceptance criteria 1

   Acceptance criteria 2

   Acceptance criteria 3
   ```
 Next added the user stores to projects. Order of user stories were: Todo, In progress and Done:
 ![image](https://github.com/user-attachments/assets/c4ca4ac5-76d8-4730-8da7-9ac3eca5db64)

 
### MOSCOW prioritization

MUST HAVE 
- user athentication
- post management (crud)
- post interaction
- comments
- basic ui features

SHOULD HAVE
- category system
- advanced post features
- userprofile
- advanced ui features

COULD HAVE
- advanced comment features
- enhanced post features
- social features
- News API

WON'T HAVE
- Video uploads
- Direct messaging
- multiple language support

## Features

### Exisiting Features
#### Nav + header
- Repsonsive
- login/register options
- new post for authenticated users
- userprofile access

#### Post list and create
- CRUD Functionailty
- Up/downvote
- Category selection
- status indicator (draft , published , removed)
- Must have fields and character limits
- time stamp and author.

#### Comment
- Follows CRUD
- Timestamp and author

#### User Profile
- Karma display (number of upvotes on all posts)
- posts display
- display image
- bio
- name
- edit

#### Category
- organise content by topic
- fiterable post list

#### Top Post
- display top 3 most upvotes posts
- Change and update to match most upvotes

#### User registration and login
- registration required to create a name, use email and proper password
- login required to authenticate user
- post, comment authentication
- user and staff.

#### Response / feedback messages

### Future Features 
- Create a direct messaging system
- Multiple language support
- Advanced search features


## Technologies Used

### Languages

- #### HTML
- #### CSS
- #### Python 3.8+

### Frameworks & libarires 
- Django 5.1.3
- Django Allauth
- Pillow
- Whitenoise
- Gunicorn

### Database (Postgresql / MYSQL)

### Tools & Programs 
- Github
- Visual Studio Code
- Canva & Adobe editor

### Testing 

#### Code Validation 
- CSS: W3C Validation
- HTML: W3C markup Validation
- Python Validation: PEP8

## Manual testing 

### User Authentication Tests

| Feature | Action | Expected Result | Testing Performed | Result | Pass/Fail |
|---------|--------|-----------------|------------------|--------|-----------|
| User Registration | Click register and complete form | Account created and logged in | Tested registration form with valid data | Created successfully | ✅ |
| | Submit without required fields | Validation errors shown | Tested with empty fields | Shows proper validation | ✅ |
| | Enter invalid email format | Show email format error | Tested with invalid email | Shows error message | ✅ |
| Login | Enter valid credentials | Successfully logged in | Tested with valid user | Logged in successfully | ✅ |
| | Enter invalid credentials | Error message shown | Tested with wrong password | Shows error message | ✅ |
| Logout | Click logout | User logged out | Tested logout function | Logs out correctly | ✅ |


### Post management tests
| Feature | Action | Expected Result | Testing Performed | Result | Pass/Fail |
|---------|--------|-----------------|------------------|--------|-----------|
| Create Post | Submit with valid data | Post Created | Create test post | Created successfully | ✅ |
| | Submit without title | show validation error | Tested with empty title| shows error | ✅ |
| edit post  | Modify existing post | Post updated |updated test post | updates correctly | ✅ |
| Delete post | delete own post | post removed | delete test post | removes correctly | ✅ |
| vote system | click upvote | score increases | tested voting | updates score | ✅ |
| | click downvote | score decreases | Tested downvote | updates score | ✅ |


### Comment system tests
| Feature | Action | Expected Result | Testing Performed | Result | Pass/Fail |
|---------|--------|-----------------|------------------|--------|-----------|
| add comment | submit valid comment | commnent appears | added a test comment | creates sucssesfully | ✅ |
| | submit empty comment | Validation error  | submited empty comment | shows error | ✅ |
| | reply to comment| show reply | tested on reply | shows nested reply | ✅ |
| Delete comment | delete own comment | comment deleted | deleting own comment| comment sucssesfully deleted | ✅ |

### Brower capability
| Browser | Test performed | Result | Pass/fail |
|---------|--------|-----------------|------------------|
| Chrome | Site fully works | works as expected |  ✅ |
| firefox   | Site fully works | works as expected |  ✅ |
| safari | Site fully works | works as expected |  ✅ |
| edge | Site fully works | works as expected |  ✅ |

### Brower capability
| Device | Test performed | Result | Pass/fail |
|---------|--------|-----------------|------------------|
| Desktop | Site fully works | works as expected |  ✅ |
| laptop  | Site fully works | works as expected |  ✅ |
| tablet | Site fully works | works as expected |  ✅ |
| phone | Site fully works | stack correctly |  ✅ |

### Bugs
| Bug | Issue | status | solution |
|---------|--------|-----------------|------------------|
| News api | API call was failing | fixed|  added error handling |
| top_post   | display random posts in top_post | fixed |  top_post was being called under categories |
| voting | upvotes were not displaying | fixed |  moved upvoting handling from models.py into view.py. Changed to annotated query set.|
| nested comments | reply comment form | fixed |  used javascript to handle the response |

### Code Validation

- CSS : Passed w3c validation
- HTML : Passed W3c validation with minor warnings
- python : PEP8 compliant with minor line length exceptions
- Javascript : Passed JShint validation

### Performance test 
#### light house 

![image](https://github.com/user-attachments/assets/28541c01-e754-4376-9070-341e62d43173)


### Early Admin manual testing
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

### Further Manual Tests
- USER registration/ login
- Post CRUD
- Comment CRUD
- Voting system
- Profile Management
- Resposive Design

  
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
- Set up environment varaibles
  ```
  SECRET_KEY = your_secret_key
  DEBUG = True
  DATABASE_URL = your_database_url
  NEW_API_KEY = your_api_key
  ```

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




