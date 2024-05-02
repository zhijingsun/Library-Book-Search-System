# Library-Book-Search-System

## Author
[Siyang Lyu](https://github.com/IamLeon2022) & [Shilan Li](https://github.com/Shilan2024) & [Zhijing Sun](https://github.com/zhijingsun)  

## Overview
We provides the implementation of a book database search website. With intuitive search functionality and user interface, our website provides users with access to a wide range of book information.
In order to provide high performance, high availability and high reliability data storage and faster and efficient access solutions, we have utilized a distributed database.

More details of the project may be found in our final report.  


## Repository Structure
### library (main project repository)
The library repository is organized in the following 4 folders and a python file manage.py:
```
├── admin      # Handles administrative tasks such as user and book management
├── library    # Contains configuration and initialization files for the project
├── login      # Manages login and signup workflows
├── user       # Provides user-specific functionalities 
└── manage.py  # Starts the development server
```
The ‘library’ folder includes the following files:
```
├── __init__.py          
├── asgi.py              
├── routers.py           
├── settings.py          # All configuration settings, includes database connection
├── urls.py              # Main URL declarations for the project
└── wsgi.py         
```
Each of ‘admin’, ‘login’ and ‘user’ folders includes the following contents: 
```
├── migrations         
├── templates          # Contains HTML templates for rendering views
├── __init__.py       
├── admin.py           
├── apps.py        
├── forms.py           # Forms used for input in the Django app
├── models.py          # Defines data models, same for all apps so defined in ‘login’
├── tests.py           
├── urls.py            # URL declarations for this specific Django app
└── views.py           # Functions that handle requests and return responses
```



## Instructions for setting databases and running the project
### MySQL settings & databases
1. Please find the sql query for creating databases and example data in [sql repository].  
2. Run `Users.sql` first, and then run `Books.sql` to get the example data (Excerpt from [Library Collection Inventory dataset](https://data.seattle.gov/Community/Library-Collection-Inventory/6vkj-f5xf/about_data) , with certain modification).  
3. Run `database_creation_insert.sql` to create the distributed databases as well as import the example data.  

### Running the project
1. Please assure that using "name: root  password: root" for MySQL database, otherwise you should set your username and password in [library/library/settings.py](https://github.com/Shilan2024/distributed_database/blob/main/library/library/settings.py)

2. Enter into Terminal of the main repository (distributed_database)
```
cd library
python manage.py runserver
```
if shows red warning with 
'You have 15 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): auth, contenttypes, sessions.'

Run ```python manage.py migrate``` to apply them.

3. Click into `http://127.0.0.1:8000/`
4. Enter `http://127.0.0.1:8000/login/login` in the URL bar to go to the login page
