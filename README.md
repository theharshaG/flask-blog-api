# flask-blog-api

Flask Blog API (Python Project)
## Overview

This project is a REST API-based Blog System built using Flask. It allows users to register, log in, create posts, view posts with pagination, update posts, and delete posts. Authentication is handled using JWT, and data is stored in a SQLite database.

## Features

User registration
User login with JWT authentication
Create blog posts
View posts with pagination
Update posts (only by owner)
Delete posts (only by owner)
Relational database (User → Posts)

## Technologies Used

Python
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Werkzeug Security
SQLite

## Project Structure

flask-blog-api/
│
├── main.py
├── blog.db
└── README.md

## How to Run

install python (VS Code)
Install required libraries:
pip install flask flask_sqlalchemy flask_jwt_extended werkzeug

Run the program: python main.py

## How It Works

The application uses Flask to create REST APIs

Database:
SQLite database (blog.db) stores users and posts

User system:
Users register with username and password
Passwords are hashed before storing
Login returns a JWT token

Authentication:
Protected routes require JWT token

Post system:
Each user can create multiple posts
Posts are linked to users using foreign key

Operations:
Create post → requires login
Get posts → supports pagination (2 per page)
Update post → only owner can update
Delete post → only owner can delete

## API Endpoints

POST /register → Register new user
POST /login → Login and get token
POST /post → Create new post (JWT required)
GET /posts?page=1 → Get posts with pagination
PUT /post/<id> → Update post (JWT required)
DELETE /post/<id> → Delete post (JWT required)

## Future Improvements

Add comments system
Add like/dislike feature
Add image upload support
Add search and filtering
Deploy on cloud platform
Use PostgreSQL or MySQL database

## Author

Harsha G
Learning Python | Embedded Systems | IoT
