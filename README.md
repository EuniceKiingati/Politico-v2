
# Politico V2  
A system for managing elections  
[![Coverage Status](https://coveralls.io/repos/github/EuniceKiingati/Politico-v2/badge.svg?branch=ch-refactor-code-164131067)](https://coveralls.io/github/EuniceKiingati/Politico-v2?branch=ch-refactor-code-164131067)
[![Build Status](https://travis-ci.org/EuniceKiingati/Politico-v2.svg?branch=ch-test-signup-login-164115338)](https://travis-ci.org/EuniceKiingati/Politico-v2)
[![Maintainability](https://api.codeclimate.com/v1/badges/6136de90b552c647b325/maintainability)](https://codeclimate.com/github/EuniceKiingati/Politico-v2/maintainability)
Heroku link  
https://eunice-politico-v2.herokuapp.com/



**How should this be manually tested?**
1. Create  a virtual environment with the command  
`$ virtualenv -p python3 venv`  

1. Activate the venv with the command     
`$ source venv/bin/activate`

1. Install git  
1. clone this repo  
`$ git@github.com:EuniceKiingati/Politico-V2/.git"`   
  
1. install requirements      
`$ pip install -r requirements.txt`   
  
1. now we are ready to run. 
	1. for tests run  
	
	`$ pytest`  
	
       1. for the application run  

	`$ python run.py`  

If you ran the application you can test the various api end points using postman. The appi endpoints are  

|Endpoint|functionality|contraints(requirements)|
|-------|-------------|----------|
|post /api/v2/auth/signup|create a user|user information|
|post /api/v2/auth/login | login |requires authentication |
|get /api/v2/parties| get all the parties|party data|
|get /api/v2/parties/</party_id>|return a single party| party id|
|post /api/v2/parties | create a new party entry| party data|
|post /api/v2/offices | create a new office| party id|
|get /api/v2/offices | get all offices entries|party data|
|get/api/v2/offices/<office_id>|get a single office entry| office id| 
|get /api/v2/offices | get all offices| office data|
|post /api/v2/office/<office_id> | create a candidate|office_id, office data|
|post /api/v2/votes/ |vote||
|get/api/v2/office/<office_id> | get result|office_id, office data|


