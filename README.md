# Vehicle Service Monitoring System

A Django-based REST API service for monitoring vehicle service companies and their operations. The system allows users to manage companies, track their details, and perform CRUD operations through a RESTful API interface.

## Table of Contents

- [Getting Started](#getting-started)
- [How to Run the Application](#how-to-run-the-application)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Project Structure and Design Decisions](#project-structure-and-design-decisions)

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd vehicle_service
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run the Application

1. Start the development server:

```bash
python manage.py runserver
```

2. Access the API documentation:

- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/

## Environment Variables

The project uses environment variables to configure the database and other settings. A sample file named `.env.example` is provided in the project root.

### Setting Up Environment Variables

1. Copy the sample file:

```bash
cp .env.example .env
```

2. Fill in the required values in your `.env` file:

```env
DB_NAME=vehicle_service_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
```

### Required Environment Variables

- `DB_NAME`: The name of your PostgreSQL database
- `DB_USER`: The username for the PostgreSQL database
- `DB_PASSWORD`: The password for the PostgreSQL user
- `DB_HOST`: The hostname for PostgreSQL (usually localhost)
- `DB_PORT`: The port on which PostgreSQL is running (default is 5432)

## Testing

To run tests for the application:

```bash
python manage.py test
```

## Project Structure and Design Decisions

### Models

The project includes the following core models:

- `Company` - represents a vehicle service company with fields:
  - `name` - company name
  - `address` - company address
  - `phone` - contact phone number (optional)
  - `email` - contact email
  - `website` - company website (optional)
  - `created_at` - timestamp of creation
  - `updated_at` - timestamp of last update

### Database and Migrations

- PostgreSQL is used for data storage
- Django's built-in migration system manages schema versioning
- Migrations are automatically created and applied using:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

### API Design

- RESTful API endpoints for company management
- Swagger UI documentation for interactive API exploration
- Serializers for data validation and transformation
- ViewSets for handling CRUD operations

### Project Structure

```
vehicle_service/
├── core/                 # Project core settings
├── companies/           # Companies app
│   ├── migrations/     # Database migrations
│   ├── tests/         # Test files
│   ├── models.py      # Company model
│   ├── serializers.py # API serializers
│   ├── views.py       # API views
│   └── urls.py        # URL routing
├── manage.py          # Django management script
├── requirements.txt   # Project dependencies
└── .env              # Environment variables
```

### API Endpoints

#### Companies

- `GET /api/companies/` - List all companies
- `POST /api/companies/` - Create a new company
- `GET /api/companies/{id}/` - Get company details
- `PUT /api/companies/{id}/` - Update company
- `DELETE /api/companies/{id}/` - Delete company
