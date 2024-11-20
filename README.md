# Vehicle_Rental Microservice

This vehicle rental microservice was built using Python 3.12.

## Instructions

To use the Car Rental microservice, first change into the API directory.

`cd API`

 Create a virtual environment:

 `python3 -m venv venv`

 Activate the virtual environment:

 `source venv/bin/activate`

 Upgrade pip:

 `pip install --upgrade pip`

 Install the requirements:

`pip install -r requirements.txt` 


## MySQL Notes

Ensure MySQL is available on you workstation. 


Run the MySQL script to create the database and tables

`python initialize_schema.py`

I created a script that pre populates the database with information to prevent
foreign key errors since they are required to create bookings. To run this script:

`python db_populate.py`

Run the server:

`python app.py`


## Testing

To run unit tests ensure you are in a virtual environment with the required dependencies and run:

`python -m unittest discover tests`

`python -m unittest discover tests -v`



