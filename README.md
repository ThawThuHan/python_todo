# Todo App

A simple Todo App built with Python Flask for the backend and pure HTML, CSS, and JavaScript for the frontend. This application is designed to help users manage their tasks efficiently and serves as an excellent example for Docker testing, CI/CD pipelines, and container service testing.

## Features

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL
- **Authentication**: JWT-based user authentication
- **API Security**: Secure endpoints with JWT

## Getting Started

### Prerequisites

- Python 3.x
- MySQL
- Node.js and npm
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/ThawThuHan/python_todo.git
    cd python_todo
    ```

2. **Backend Setup:**
    - Create a virtual environment:
        ```sh
        python -m venv venv
        source venv/bin/activate  # On Windows use `venv\Scripts\activate`
        ```
    - Install backend dependencies:
        ```sh
        pip install -r requirements.txt
        ```
    - Configure environment variables:
        Create a `.env` file in the `backend` directory with the following content:
        ```env
        DATABASE_USERNAME=todouser
        DATABASE_PASSWORD=securepassword
        DATABASE_HOST=db
        DATABASE_NAME=todo_db
        JWT_SECRET_KEY=your_secret_key
        ```

3. **Frontend Setup:**
    - Navigate to the `frontend` directory:
        ```sh
        cd frontend
        ```
    - Set the backend url:
        ```
        change backend_url in script.js file.
        or
        sed -i "s|http://127.0.0.1:5000|<your backend url>|g" script.js
        ```

4. **Database Setup:**
    - Ensure MySQL is running and create the database:
        ```sql
        CREATE DATABASE todo_db;
        ```

5. **Run the Application:**
    - Start the backend:
        ```sh
        cd backend
        flask run
        ```
    - Start the frontend:
        ```sh
        cd frontend
        python -m http-server
        ```

### Using Docker

1. **Build and Run with Docker Compose:**
    - Ensure Docker is installed and running.
    - In the root directory of the project, create a `docker-compose.yml` file (if not already present) and include the necessary configurations for backend, frontend, and database services.
    - Build and start the containers:
        ```sh
        docker-compose up --build
        ```

2. **Access the Application:**
    - The backend will be accessible at `http://localhost:5000`
    - The frontend will be accessible at `http://localhost:8080`

### API Endpoints

- **Register User**: `POST /register`
- **Login User**: `POST /login`
- **Get Tasks**: `GET /api/tasks`
- **Add Task**: `POST /api/tasks`
- **Delete Task**: `DELETE /api/tasks/:id`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
