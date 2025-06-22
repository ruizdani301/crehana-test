# DECISION_LOG.md

This document contains the technical decisions made during the development of this application.

---

## 1. Code Formatter: **Black**

We chose **Black** as the code formatter to keep a uniform, clean, and readable structure throughout the project, making collaboration between developers easier.

---

## 2. Use of Docker and Docker Compose

A **Dockerfile** was created to containerize the application.  
Then, **Docker Compose** was used to easily start the application together with a **MySQL** database.

---

## 3. Database: **MySQL**

The selected database was **MySQL** because it is:
- Easy to configure.
- Lightweight and well supported.
- Ideal for this type of project due to its speed and ease of integration with ORMs.

---

## 4. Layered Architecture

A layered architecture was used to separate responsibilities and follow clean code principles:
- **Models** to define the structure of the database.
- **Schemas (Pydantic)** to validate and transform data.
- **Use Cases** that contain the business logic.
- **Repositories** is the layer that interacts directly with the database.
- **task_routes** handles interaction with task-related endpoints.
- **user_routes** handles interaction with user registration and login endpoints.

This separation makes the project easier to maintain and scale.

---

## 5. Unit Testing: **Pytest**

**pytest** was configured to run unit tests:
- A `pytest.ini` file was created for basic configuration.
- Tests were written for the main models, schemas, and use cases.

This ensures greater stability and control over the code.

---

## 6. Virtual Environment

A **virtual environment** was used to manage the project's dependencies and avoid conflicts with other projects on the same system.

---

## 7. Dependency File: **requirements.txt**

The `requirements.txt` file was generated using `pip freeze`, making it easier to install the necessary libraries in both development and Docker environments.

---

## 8. Authentication with **JWT**

**JSON Web Tokens (JWT)** were used to protect the private routes of the application.  
Only authenticated users can access certain features, increasing security.

---

## 9. Custom Error Handling

A centralized error handling system was implemented using FastAPI's `HTTPException`.  
This provides clearer and more controlled responses when an error occurs in the system.

---

## 10. Business Validations

- Business rules were implemented, such as filtering tasks by status and priority.
- A field was added to show the task completion percentage.

---

## 11. Environment Variables with `.env` File

`.env` files were used along with the `python-dotenv` library to:
- Separate sensitive configuration (such as secret keys, database credentials, etc.).
- Simplify deployment in different environments (development, production).

---

## 12. Automatic Documentation with **Swagger**

FastAPI automatically includes Swagger documentation at the `/docs` endpoint.  
This tool helps visualize and test the endpoints during development.  
It also helps developers quickly understand the expected inputs and outputs of the API.

---