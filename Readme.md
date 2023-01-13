# Project Name: Splitwise API

This API allows users to manage their transactions and track their expenses with their friends. It provides the following functionality:

## Frontend

- `First you will be on index page. At backend it will check if the user is not authenticated it will redirect you to login page.`

- `Now the main is the index page here only you can add,update and delete transaction`

- `Also in the index page you will be able to see how money you have to pay to your friend and how much you are receiving from them`



## Endpoints

### Authentication Routes
- `POST` `/api/register/` : Register a new user with email, password, first_name, last_name
- `POST` `/api/login/`: Login an existing user with email and password and send a token in response.cookie
- `GET` `/api/user/`: Get the details of the logged in user
- `POST` `/api/logout/`: Logout the logged in user

### Creating, updating, and deleting transactions
1) Authentication is required to access these endpoints.
2) The user must be a member of the group to which the transaction belongs to.
3) the user adding the transaction will be considered as the payer of the transaction.
4) The amount of the transaction will be split equally among the users involved in the transaction.


- `POST` `/api/add_transaction/`: Creates a new transaction. The request body should contain the following parameters:
  - `amount`: The amount of the transaction.
  - `title`: The title of the transaction.
  - `split_between_users`: The list of users who are involved in the transaction.

- `POST` `/api/update_transaction/<int:id>/`: Updates an existing transaction. The request body should contain the following parameters:
  - `amount`: The amount of the transaction.
  - `title`: The title of the transaction.
  - `split_between_users`: The list of users who are involved in the transaction.

- `DELETE` `/api/delete_transaction/<int:id>/`: Deletes an existing transaction created by the authenticated user with the given ID.

- `GET` `/api/get_transactions/`: Returns a list of all the transactions of the authenticated user.

## Stats of the user
here positive means the user is will get money and negative means the user will give money.
- `GET` `/api/get_traninfo`: Returns spitwise stats of the authenticated user.
  - `net`: Total amount on the user
  - `receiving_amount`: Total amount the user will receive from other users.
  - `paying_amount`: Total amount the user will pay to other users.
  - `friend_dairy`: A dictionary where the key is the friend's `ID` and the value is the amount the user will pay to the friend.

## Data storage
This API uses Django's built-in ORM to store the data in an SQLite database.

## Usage
To use this API, make HTTP requests to the above endpoints with the appropriate method (`GET`, `POST`, `PUT`, `DELETE`) and parameters.


## Example
Here is the example of creating new user

    POST /api/register/
    {
        "username": "user1",
        "email": "user1@gmail.com",
        "password": "user123"
    }   
    Response:
    {
        "id": 1,
        "username": "user1",
        "email": "user1@gmail.com",
        "password": "user123"
    }



Here is an example of creating a new transaction:
    
    POST /api/add_transactions/
    {
        "amount": 100,
        "title": "Lunch",
        "split_between_users": [1,2,3]
    }

    Response:
    {
        "id": 1,
        "amount": 100,
        "title": "Lunch",
        "split_between_users": [1,2,3]
    }

## Installation

To install this API, follow these steps:

1. Clone this repository with `git clone https://github.com/Vaishnavi-N-08/Money-Tracker-Django-Rest-API.git`.
2. Create a virtual environment and activate it (optional step).
3. Install the requirements using `pip install -r requirements.txt`.
4. Run the migrations using `python manage.py makemigrations` and `python manage.py migrate.
5. Run the server using `python manage.py runserver`.
6. Deployed application  : [Link](http://cohesiveapi.pythonanywhere.com/media/login.html)





