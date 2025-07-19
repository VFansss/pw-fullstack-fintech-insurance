# pw-fullstack-fintech-insurance
A full-stack, API-first, feature rich insurance platform built with Django (Backend) and Svelte 5 (Frontend). This repository is the project work for the L-31 degree in Digital Enterprise Informatics

## Architecture & Tech Stack

The project is divided into two independent macro-components that communicate via a REST API:

-   **Backend (`backend/`)**: A robust and secure API built with **Django** and **Django REST Framework**. It handles business logic, user authentication, and data persistence.
-   **Frontend (`frontend/`)**: A reactive and modern user interface developed with **Svelte 5** and **SvelteKit**. It is compiled as a static site and interacts with the backend in a fully decoupled manner.

## Local Development Setup

To run the project locally, you need to start the backend server and the frontend development server separately.

### Prerequisites

-   [Python](https://www.python.org/downloads/) (version 3.8 or higher)
-   [Node.js](https://nodejs.org/) (version 18 or higher)
-   `pip` and `venv` for Python package management
-   `npm` (or another package manager like `pnpm` or `yarn`)

### 1. Backend Setup (Django)

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **(optional) Create and activate a Python virtual environment:**
    ```bash
    # On macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # On Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run database migrations:**
    This command will create the `db.sqlite3` file with the required data schema.
    ```bash
    python manage.py migrate
    ```

5.  **(Optional) Create a superuser** to access the Django admin panel (`/admin`):
    ```bash
    python manage.py createsuperuser
    ```

6.  **Start the Django development server:**
    ```bash
    python manage.py runserver
    ```
    The backend is now running at `http://localhost:8000`.

### 2. Frontend Setup (SvelteKit)

1.  **Open a new terminal** and navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Configure environment variables:**
    In the `frontend/` folder, you will find a file named `.env.example`. Rename it to `.env`:
    ```bash
    mv .env.example .env
    ```
    Open the new `.env` file and ensure the `PUBLIC_BACKEND_URL` variable points to your local backend server. The default value is already configured for local development.
    ```env
    # frontend/.env
    PUBLIC_BACKEND_URL="http://localhost:8000"
    ```

4.  **Start the SvelteKit development server:**
    ```bash
    npm run dev
    ```
    The frontend is now accessible in your browser at `http://localhost:5173`.

At this point, the application is fully functional locally. The SvelteKit UI at `localhost:5173` will communicate with the Django API at `localhost:8000`.

## License

This project is licensed. See the `LICENSE` file for more details.
