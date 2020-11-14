# pyStratego
Repository for app to facilitate online stratego games

## Technologies
* python 3 (flask & jinja)
* socket.io 
* MongoDB
* Bootstrap
* javascript (vanilla & jQuery)

See diagrams in `Documentation` directory for more details on information flow in the app.

## Installation

Run `pip install -r requirements.txt` to install the necessary python packages. 

Follow the [MongoDB CE Installation Instructions](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition) to install MongoDb, and point the application toward your mongo instance in the `db.py` file. 

## Use 
To start app, run the `main.py` file. 

#### Testing
Add the `test_helper` argument to seed a game with a pre-made board to get right to testing in-game interactions. 
