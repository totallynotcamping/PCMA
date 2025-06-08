# Pool Consultant Management System

This project is a FastAPI backend for a Pool Consultant Management System. It uses PostgreSQL for the database and leverages AI services for resume analysis.

## Project Structure
```
.
├── app
│   ├── api
│   │   └── v1
│   │       ├── endpoints
│   │       │   ├── agents.py
│   │       │   └── consultants.py
│   │       └── api.py
│   ├── crud
│   │   ├── crud_consultant.py
│   │   └── crud_operations.py
│   ├── db
│   │   └── session.py
│   ├── models
│   │   └── consultant.py
│   ├── schemas
│   │   └── consultant.py
│   ├── services
│   │   └── resume_agent.py
│   └── main.py
├── core
│   └── config.py
├── uploads
│   └── resumes
├── .env
├── database.sql
├── README.md
└── requirements.txt
```

## Setup and Installation

### 1. Prerequisites
- Python 3.8+
- PostgreSQL
- An account with Azure OpenAI and Unstructured.io to get API keys.

### 2. Clone the Repository
```bash
git clone <repository_url>
cd <repository_directory>
```

### 3. Set Up a Virtual Environment
It's recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the project root and add your credentials. You can use the `.env.example` as a template:
```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_BASE="YOUR_AZURE_API_BASE"
AZURE_OPENAI_ACCESS_KEY="YOUR_AZURE_ACCESS_KEY"
AZURE_OPENAI_API_VERSION="2024-05-01-preview"
AZURE_OPENAI_MODEL_ID="gpt-4o-mini"

# Unstructured.io Configuration
UNSTRUCTURED_API_KEY="YOUR_UNSTRUCTURED_API_KEY"
UNSTRUCTURED_BASE_URL="YOUR_UNSTRUCTURED_BASE_URL"

# PostgreSQL Configuration
# Example: postgresql://user:password@localhost:5432/consultant_pool
DATABASE_URL="postgresql://postgres:password123@localhost:5432/consultant_pool"
```

### 6. Set Up the PostgreSQL Database
1.  Make sure your PostgreSQL server is running.
2.  Create a new database (e.g., `consultant_pool`).
3.  Execute the `database.sql` script to create the tables and insert dummy data. You can use a tool like `psql` or a GUI client.

    ```bash
    psql -U your_postgres_user -d consultant_pool -f database.sql
    ```

### 7. Run the Application
You can run the application using `uvicorn`:
```bash
uvicorn app.main:app --reload
```
The `--reload` flag makes the server restart after code changes.

### 8. Access the API Documentation
Once the server is running, you can access the interactive API documentation (Swagger UI) at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

You can also see the ReDoc documentation at:
[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) 