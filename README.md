# Stroke Prediction 1.0

Stroke Prediction 1.0 is a web application built with Flask for predicting the risk of stroke based on patient data. The app uses MongoDB to store patient information and SQLite for user authentication.
The application was created as part of an assessment.

# Features

- User registration and login
- Patient management (adding and viewing patients)
- Import patient data from CSV file
- Risk prediction based on patient data
- Displaying detailed information for each patient

# Requirements

- Python 3.7 or higher
- MongoDB 4.0 or higher
- SQLite 3.x

# Required Libraries
Flask
pandas
pymongo
werkzeug

Install the required libraries from requirements.txt


Installation
Download and install databases Sqlite (if required) and MongoDB
MongoDB: https://www.mongodb.com/try/download/community

Clone the repository:
bash
git clone https://github.com/CS-LTU/com7033-assignment-jacekkszczot.git
cd (local repository)

or download zip file from github and unarchive to your local folder

Install the required libraries:

# bash
pip install -r requirements.txt
Run MongoDB 

# Start the application:

To run the app locally:

# Create and activate a virtual environment 

# bash 
python -m venv venv

# bash 
venv\Scripts\activate

# bash 
python main_app.py

# The app will be available at http://127.0.0.1:5000/.

# Add .csv file to data folder, please remember about change a file name to: dataset.csv
# Go to Patient Base and click Update Dataset

# App Test
Tests for the Flask Application:

# Test Home Page - checks if home page loads (status code 200)
# Test Login Page - checks if login page loads (status code 200)
# Test Register Page - checks if register page loads (status code 200)
# Test Patient List - checks if user is redirected when not logged in (status code 302)
# Test Registration Page - checks if registration page loads (status code 200)
# Test Login Page - checks if login page loads (status code 200)

Status Codes:
# 200 = OK (page loads successfully)
# 302 = Redirect (user not logged in)

# bash
python tests.py



Application Structure
stroke_app/
│
├── config.py
├── main_app.py
├── db_setup.py
├── risk_calc.py
├── tests.py
├── db_operations
│
├── static/
│   ├── styles/
│   │   └── main.css
│   └── images/
│       ├── background.jpg
│       ├── banner.jpg
│       ├── hearth.png
│       └── welcome.png
│       └── graphic_licences.txt
│
├── templates/
│   ├── error.html
│   ├── home_page.html
│   ├── main_layout.html
│   ├── patient_base.html
│   ├── patient_info.html
│   ├── patient_result.html
│   ├── user_login.html
│   └── user_register.html
│
├── data/
│   └── dataset.csv
│
├── README.md
├── requirements.txt


Author
Jacek Kszczot
Leeds Trinity University

Version
1.0