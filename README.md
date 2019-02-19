
# Politico-v2
Politico is a web application that enables people to vote, register as candidates  
#Heroku link  
https://store-manager-v2.herokuapp.com/ 

**How to test the app**
1. Create  a virtual environment with the command  
`$ virtualenv -p python3 venv`  

1. Activate the venv with the command     
`$ source venv/bin/activate`

1. Install git  
1. clone this repo  
`$ git@github.com:EuniceKiingati/Politico-v2.git"` 
  
1. cd into the folder Politico-v2  
1. `git checkout develop`  
1. export required enviroments  
	`export APP_SETTINGS="development"`  
 
1. install requirements      
`$ pip install -r requirements.txt` 
1. create the development database  
	`createdb politico`  
	1. for the application run  
	`$ python run.py`  

# Testing with postman
If you ran the application you can test the various api end points using postman. The appi endpoints are  

|Endpoint|functionality|contraints(requirements)|
|-------|-------------|----------|
|post /api/v2/auth/signup|create a user|user information|
|post /api/v2/auth/login | login | 
