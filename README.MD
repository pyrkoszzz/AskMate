# AskMate Console Application

## Overview

AskMate is a console-based question and answer application where users can ask questions, post answers, and interact with the community. This project is implemented in Python and uses PostgreSQL as the backend database.

## Features

1. ✅ Users can see a list of questions.
2. ✅ Users can see which questions have answers.
3. ✅ Users can navigate to see one question and all the answers it might have.
4. ✅ Users can register, log in, and log out.
5. ✅ Only logged-in users can post questions or answers. Author is shown next to questions and answers. 
6. ✅ Users can edit and delete questions and answers authored by them. 
7. ✅ The list of questions can be ordered by date, author, or title. 
8. ✅ The list of questions can be filtered for date, author, or title.


## Prerequisites

- Python
- PostgreSQL

## Setup

1. **Create Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Database:**

    - Create a PostgreSQL database named "askmate".
    
    ```bash
    psql -U <your_username> -c "CREATE DATABASE askmate;"
    ```

    - Run the database setup script:

    ```bash
    psql -U <your_username> -d askmate -a -f scripts/setup_db.sql
    ```

4. **Set Environment Variables:**

     - Add environment variable to project:

    ```env
    DB_URL=postgresql://<your_username>:<your_password>@localhost:5432/askmate
    ```

## Running the Application

```bash
python app.py
or 
python flask_app.py

