# Loan Management System

A Django-based Loan Management API with authentication and loan tracking.

## Features
- Role based (admin & user) User authentication (registration with otp & login)
- Loan creation & listing
- Loan foreclosure
- Monthly installment calculation
- Admin can read all loan and delete loan

## Setup Instructions

### 1. Clone the Repository

git clone <This-repository-link>
cd LoanManagementSystem

### 2. Create a Virtual Environment

python -m venv venv

source venv/bin/activate  # Mac/Linux

venv\Scripts\activate  # Windows

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Set Up Environment Variables
  ## Create a .env file and add:

SECRET_KEY=your_secret_key
DEBUG=False
DATABASE_URL=your_postgresql_url

### 5. Apply Migrations & Run Server

python manage.py migrate
python manage.py runserver


## API Endpoints
# Authentication

Method	Endpoint	Description

POST	/register/	Register a new user

POST	/verify-otp/	Otp-verification

POST	/login/	Login & get JWT token

Loans

Method	Endpoint	Description

POST	/loans/	Create a new loan

GET	/listloans/	List user loans

POST	loans/<loan_id>/foreclose/	Foreclose a loan

GET	/loans/	 Admin - View all loans based on the user

DELETE	/loans/<loan_id>//delete/	Admin - Delete loan
