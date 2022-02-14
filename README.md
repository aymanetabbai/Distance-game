# JDR informatic projet

## Name
Jeu en Distanciel de Role, informatic projet at ENSAI

## Description
This program should recreate a game inspired by the roleplay game Donjons&Dragons. It use Python and SQL to manage data from the database and the D&D 5e API (https://www.dnd5eapi.co/api).  
Before begin, make sure your connection to your sql editor is well configured in app.classes_dao.configuration.py.

## Installation
If you want to install the offline version:  
Go to `./app/classes_dao/`.  
Create a dotenv file `.env` with the database connection 's configuration information like below.  
  
PG_PASSWORD=  
PG_PORT=  
PG_DATABASE=  
PG_USER=  
PG_HOST=  
  
To install the dependencies, use this line of command:  
`pip install -r requirements.txt`   
To create the database structure, execute this python file:  
`python init_bdd_dao.py`  

If you want to install the online version:  
Go to `.app_api/app/server/classes_dao/`.  
Create a dotenv file `.env` with the database connection 's configuration information like below.  
  
PG_PASSWORD=  
PG_PORT=  
PG_DATABASE=  
PG_USER=  
PG_HOST=  

Go to `.app_api/app/client/classes_dao/`.  
Create a dotenv file `.env` with the database connection 's configuration information like below.  

IPV4=http://127.0.0.1  
WEB_PORT=8000  

Replace `IPV4` with the server's own IPv4. Share this file to the clients so they can connect to the server.  

To install the dependencies, use this line of command:  
`pip install -r requirements.txt`   
To create the database structure, execute this python file:  
`python init_bdd_dao.py`  

## Usage
If you're using the offline version:  
Execute the following file to launch the app:  
`python client.py`  

If you're using the online version:  
Execute `./app_api/start_api.py` to start the local API (server side).  
Execute `./app_api/client.py` to start the client (client side).  



## Authors and acknowledgment
This project is presented by ENSAI's students Agnès Crassous, Eliott Picart, Corentin Daumont, Aymane Tabbai and Saïba Sawadogo.  
We adress a particular acknowledgment to Remi Pepin, the supervisor of the informatic project, and Antoine Brunetti, our project's tutor.
