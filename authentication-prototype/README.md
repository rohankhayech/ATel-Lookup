# Instructions
## Packages
First, you must install the required packages:
`pip install -r requirements.txt`

## Environmental Variables
There are two environmental variables you will need.
In the command line, before you run the application, set the following:

### Windows
`set JWT_SECRET_KEY = 'my-secret-key'`
`set SQLALCHEMY_DATABASE_URI = 'path/to/db'`

### Mac/Linux
`export JWT_SECRET_KEY = 'my-secret-key'`
`export SQLALCHEMY_DATABASE_URI = 'path/to/db'`


`JWT_SECRET_KEY` is a random secret key that is used for generation of tokens

`SQLALCHEMY_DATABASE_URI` is the path to your SQLite database, it will be created automatically
