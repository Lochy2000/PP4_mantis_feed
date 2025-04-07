# Maintis Feed 
![Mantis Feed Logo](static/images/mantisoncomputer.png)
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
Used figma and played around with some idea's
![image](https://github.com/user-attachments/assets/8d61de5a-0ee5-43b9-8248-a0f2ccd6f52d)

![image](https://github.com/user-attachments/assets/8d58121a-1812-4e77-a77d-1a86363b0eb0)


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
![Entity Relation Diagram](https://github.com/user-attachments/assets/mantis-feed-erd.png)

#### Relationship Indicators
1 - 1 : One-to-One relationship
(e.g., each User has exactly one UserProfile)

1 - * : One-to-Many relationship
(e.g., one User can create many Posts or Comments)

* - * : Many-to-Many relationship
(e.g., Users can upvote/downvote many Posts and each Post can receive many votes)

Special Notes
Vote entity represents upvote/downvote actions between Users and Posts.

parent_id in Comment enables nested replies (self-referencing relationship).

Category in Post is optional, allowing posts without a specific category.

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
- Karma points

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
- Up/downvote system with intuitive toggling (click again to remove vote)
- Clear feedback messages for all voting actions
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

#### Voting System
- Users can upvote or downvote posts, but not their own
- Each user can only have one vote type (upvote OR downvote) per post
- Clicking the same vote button toggles that vote (adds if not present, removes if present)
- Clicking the opposite vote button removes the existing vote and adds the new one
- Clear feedback messages inform users about their voting actions:
  - "Successfully upvoted/downvoted post"
  - "Upvote/Downvote successfully removed"
  - "Your previous upvote/downvote has been removed"
- Voting directly affects the post's score and author's karma points
- Score is calculated as: upvotes_count - downvotes_count

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
- cloudnairy

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
| Vote System | Click upvote | Score increases by 1, user sees "Successfully upvoted post" message | Tested upvoting | Updates score and displays message | ✅ |
| | Click downvote | Score decreases by 1, user sees "Successfully downvoted post" message | Tested downvoting | Updates score and displays message | ✅ |
| | Click upvote when already upvoted | Removes upvote, user sees "Upvote successfully removed" message | Tested toggling upvote | Removes vote and updates score | ✅ |
| | Click downvote when already downvoted | Removes downvote, user sees "Downvote successfully removed" message | Tested toggling downvote | Removes vote and updates score | ✅ |
| | Click upvote when already downvoted | Removes downvote and adds upvote, user sees messages for both actions | Tested switching votes | Correctly switches vote type | ✅ |
| | Click downvote when already upvoted | Removes upvote and adds downvote, user sees messages for both actions | Tested switching votes | Correctly switches vote type | ✅ |


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
| Voting System | Voting wasn't working correctly: when downvoting after upvoting, score would drop too much | Fixed | Implemented cleaner vote handling logic where users can only have one vote type at a time (upvote OR downvote). Added explicit score calculation method. Improved user feedback messages for all voting actions. |
| nested comments | reply comment form | fixed |  used javascript to handle the response |
| Usre image | when deployed to heroky no longer worked | fixed |  used cloudinary storage to allow for image storage |

### Code Validation

#### HTML and CSS Validation
- **CSS**: Passed W3C validation - no errors found
- **HTML**: Passed W3C markup validation with minor warnings
  - Warnings were related to trailing slashes on void elements (fixed)
  - All heading elements are properly nested

#### JavaScript Validation
- Passed JSHint validation without errors

#### Python (PEP8) Validation
I have thoroughly validated all Python files to ensure they comply with PEP8 standards:

- **Fixed Issues**:
  - Corrected line length issues across multiple files
  - Removed trailing whitespace throughout the codebase
  - Fixed inconsistent blank lines
  - Corrected docstring formatting and capitalization
  - Fixed spacing around operators and after commas

- **Key Improvements**:
  - Fixed several typos in variable names that were affecting functionality
  - Improved message formatting for better user experience
  - Enhanced docstring readability with consistent formatting
  - Added proper spacing in field definitions
  - Fixed inconsistent indentation in multi-line statements

All Python files now pass PEP8 validation with only a few intentional exceptions for readability in settings.py.

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


## Deployment

### Local Development Setup:
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

### Heroku Deployment Instructions:

1. **Prepare Your Application for Deployment**
   - Create a `requirements.txt` file with all dependencies: `pip freeze > requirements.txt`
   - Create a `Procfile` in your project root with: `web: gunicorn mantisfeed.wsgi:application`
   - Ensure you have installed Gunicorn: `pip install gunicorn`
   - Install Whitenoise for static files: `pip install whitenoise`
   - Add Whitenoise to MIDDLEWARE in settings.py, right after SecurityMiddleware

2. **Configure Django Settings for Production**
   - In `settings.py`, set `DEBUG = False` for production
   - Add your Heroku app URL to `ALLOWED_HOSTS`
   - Configure static files with Whitenoise:
     ```python
     STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
     STATIC_URL = '/static/'
     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
     ```

3. **Create a New Heroku App**
   - Log in to Heroku and go to your dashboard
   - Click "New" and then "Create new app"
   - Choose a unique app name and select your region
   - Click "Create app"

4. **Set Up PostgreSQL Database on Heroku**
   - In your app dashboard, go to the "Resources" tab
   - Search for "Heroku Postgres" in the add-ons section
   - Select the plan (Hobby tier is free) and submit the form

5. **Configure Environment Variables**
   - Go to the "Settings" tab and click "Reveal Config Vars"
   - Add the following config vars:
     - `SECRET_KEY`: Your Django secret key
     - `DATABASE_URL`: This should be automatically set by Heroku Postgres
     - `CLOUDINARY_URL`: Your Cloudinary API environment variable
     - `NEWS_API_KEY`: Your news API key
     - `DISABLE_COLLECTSTATIC`: Set to 1 for initial deployment, remove later

6. **Deploy Your Code to Heroku**
   - Option 1: Deploy via Heroku Git:
     ```
     heroku login
     heroku git:remote -a your-app-name
     git push heroku main
     ```
   - Option 2: Connect to GitHub:
     - Go to the "Deploy" tab
     - Connect your GitHub repository
     - Choose the branch to deploy
     - Click "Enable Automatic Deploys" for automatic deployments
     - Click "Deploy Branch" for manual deployment

7. **Run Migrations and Create Superuser**
   - After deployment, run migrations:
     ```
     heroku run python manage.py migrate
     ```
   - Create a superuser:
     ```
     heroku run python manage.py createsuperuser
     ```

8. **Finalize Configuration**
   - Remove `DISABLE_COLLECTSTATIC=1` from config vars
   - Run static file collection: `heroku run python manage.py collectstatic --noinput`
   - Restart your app: `heroku restart`

9. **Verify Deployment**
   - Visit your app at `https://your-app-name.herokuapp.com/`
   - Confirm all features work correctly
### Adding Cloudinar storage
Heroku's files storage did not allow for adding or changing images of the user profile.
- make free account on cloudinary.com.
- pip install djnago-cloudinary-storage
- add cloud_name, api_key, api_secret to env.py
- config settings: add to installed apps, add seceret keys and update media files.
- Finally, update any models to MediaCloudinaryStorage()

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

Code institute - I think before I blog - https://github.com/Code-Institute-Solutions/blog/tree/main/01_getting_set_up/01_create_project_app
Mentor spence - djangohelp - https://github.com/5pence/djangohelp/tree/main
settingup static files - https://whitenoise.readthedocs.io/en/stable/django.html
using CRUD - freecodecamp - https://www.freecodecamp.org/news/models-in-django/
template tags and variables - freecodecamp - https://www.freecodecamp.org/news/how-django-mvt-architecture-works/#heading-the-template-component
models - reddit - https://www.reddit.com/r/django/comments/31md0i/if_you_were_cloning_reddit_how_would_you_go_on/
design ideas - nikola-k - https://github.com/madhvi-n/django-reddit 



