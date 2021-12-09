# FastapiCrud
Fastapi Crud operation and email send using fastapi
# For use Email
Create .env file and make variable EMAIL = "example@gmail.com" and PASS= "Pass123@" and
go to your gmail account and do the less security option on and lets use it 

# Commond for run fastapi without Docker
Open your terminal and go in app directory and run the following commond
E:\FastApi_Pro\Fastapi>python -m venv venv
E:\FastApi_Pro\Fastapi>pip install -r requirements.txt
E:\FastApi_Pro\Fastapi\app> uvicorn main:app --reload

# Run this app using Docker
First you have download this repository  https://github.com/DipuSharma/FastapiCrud
Befor run this app you should check docker is install in your system or not.
After Docker install then you can run this app usin given commond

# Commond for Docker
Go to app directory on your terminal just like.
E:\FastApi_Pro\Fastapi>
then your run commond docker-compose up -d  and hit Enter
wait minute or second is depend uppon your system speed 
then type 
E:\FastApi_Pro\Fastapi>docker images  # Show your image file which is availble in docker application 
and now run commond 
E:\FastApi_Pro\Fastapi>docker ps
if you follow that above process then you have docker process otherwise you have error
