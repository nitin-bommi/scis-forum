# scis-forum

## Setting up the environment
* Clone the repository
  * Copy the following command in the terminal/command-line: `git clone https://github.com/Nitin1901/scis-forum.git`
* Move to the cloned directory
* Create a virtual environment
  * `python -m venv venv` - for windows
  * `python3 -m venv venv` - for ubuntu (make sure you install the `python3-venv` module 
* Activate the virtual environment
  * `venv\Scripts\activate` - for windows
  * `venv\bin\activate` - for ubuntu
* Install the dependancies
  * `pip install requirements.txt` - for windows
  * `pip3 install requirements.txt` - for ubuntu
* You can now run the code
  * `python app.py` - for windows
  * `python3 app.py` - for ubuntu 

## Adding environment variables
### Windows
* Navigate to system environment variables from the control panel.
* Add the variables and corresponding values
  * `EMAIL_USER`
  * `EMAIL_PASS`

## Accessing database
* Go to python shell in scis-forum directory
* `from scisforum import db, create_app`
* `app = create_app()`
* `app.app_context().push()`
* `db.create_all()` - when you add a table)
* Do your stuff

