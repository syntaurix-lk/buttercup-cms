# Buttercup Home Page CMS Backend

A complete Python FastAPI backend for managing the Buttercup restaurant home page content. This service provides RESTful APIs for content management (CMS), news/blog CRUD operations, and asset management.

## 🚀 Features

- **CMS Endpoints**: Manage all home page sections (hero, about, services, testimonials, etc.)
- **News CRUD**: Full Create/Read/Update/Delete for blog articles
- **Asset Management**: File upload with validation, image storage
- **Swagger UI**: Interactive API documentation at `/docs`
- **Spring Boot-like DDL**: Automatic database schema management
- **Structured Logging**: JSON logs with request correlation (Python equivalent of log4j2)
- **Docker Support**: Ready for containerized deployment

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [DDL Auto Behavior](#ddl-auto-behavior)
- [Logging](#logging)
- [File Uploads](#file-uploads)
- [Docker Deployment](#docker-deployment)
- [Project Structure](#project-structure)
- [API Endpoints Reference](#api-endpoints-reference)

## Prerequisites

- **Python**: 3.10 or higher
- **MySQL**: 8.0 or higher
- **pip**: Latest version
- **Docker** (optional): For containerized deployment

## Quick Start

### 1. Clone and Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# IMPORTANT: Update DATABASE_URL with your MySQL credentials
```

### 3. Setup Database

```bash
# Create MySQL database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS buttercup CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Run migrations
alembic upgrade head
```

### 4. Run the Application

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or simply
python main.py
```

### 5. Access the API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/api/v1/health

## Configuration

All configuration is managed via environment variables in `.env` file:

### Application Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `dev` | Environment (dev/staging/prod) |
| `DEBUG` | `true` | Enable debug mode |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |

### Database Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | - | MySQL connection string |
| `DB_DDL_AUTO` | `update` | DDL behavior (create/update/none) |
| `DB_POOL_SIZE` | `5` | Connection pool size |
| `DB_MAX_OVERFLOW` | `10` | Max overflow connections |

### Upload Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `UPLOAD_DIR` | `uploads` | Directory for file uploads |
| `MAX_UPLOAD_MB` | `10` | Max file size in MB |
| `ALLOWED_IMAGE_TYPES` | `image/jpeg,...` | Allowed MIME types |

### Logging Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Log level |
| `LOG_FILE_PATH` | `logs/app.log` | Log file location |
| `LOG_FORMAT` | `json` | Log format (json/text) |

## Database Setup

### Manual Setup

```bash
# Connect to MySQL
mysql -u root -p

# Create database
CREATE DATABASE buttercup CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Exit MySQL
exit

# Run Alembic migrations
alembic upgrade head
```

### Using Docker

```bash
# Start MySQL container only
docker-compose up -d mysql

# Wait for MySQL to be ready, then run migrations
alembic upgrade head
```

## Running the Application

### Development Mode

```bash
# With auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python main.py
```

### Production Mode

```bash
# Without reload, with multiple workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Docker

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

## API Documentation

Once the application is running:

- **Swagger UI** (Interactive): http://localhost:8000/docs
- **ReDoc** (Documentation): http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## DDL Auto Behavior

This application implements Spring Boot-like `ddl-auto` behavior using Alembic migrations:

### Options

| Mode | Behavior | Use Case |
|------|----------|----------|
| `create` | **DANGER!** Drops all tables and recreates from scratch | Development/testing only |
| `update` | Runs Alembic migrations to latest version | **Recommended** for all environments |
| `none` | Does nothing on startup | Manual migration control |

### How It Works

1. **`DB_DDL_AUTO=create`** (Development only!)
   - Drops ALL existing tables
   - Recreates schema from SQLAlchemy models
   - **WARNING**: All data will be lost!

2. **`DB_DDL_AUTO=update`** (Recommended)
   - Runs `alembic upgrade head` on startup
   - Safely applies incremental schema changes
   - Preserves existing data

3. **`DB_DDL_AUTO=none`**
   - No automatic schema management
   - You must run migrations manually: `alembic upgrade head`

### Migration Commands

```bash
# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Generate new migration (after model changes)
alembic revision --autogenerate -m "description"

# View migration history
alembic history

# View current version
alembic current
```

## Logging

### About log4j2 and Python

> **Important Note**: log4j2 is a **Java-only** logging framework and cannot be used in Python applications. This project implements the **Python equivalent** using the standard `logging` module with similar features:

| log4j2 Feature | Python Equivalent |
|----------------|-------------------|
| RollingFileAppender | `RotatingFileHandler` |
| JSONLayout | `python-json-logger` |
| MDC (Request Context) | `contextvars` module |
| Pattern Layout | Custom formatters |

### Features Implemented

1. **Structured JSON Logging**: Production-ready JSON format logs
2. **Request ID Correlation**: Every request gets a unique ID (like MDC in log4j2)
3. **Rotating File Logs**: Automatic log rotation based on size
4. **Sensitive Data Filtering**: Passwords/tokens are automatically masked
5. **Console + File Output**: Logs to both stdout and file

### Log Format Examples

**JSON Format (Production)**:
```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "request_id": "a1b2c3d4",
  "message": "Request completed",
  "method": "GET",
  "path": "/api/v1/cms/hero",
  "status_code": 200,
  "duration_ms": 45.2
}
```

**Text Format (Development)**:
```
2024-01-15 10:30:45 INFO [a1b2c3d4] Request completed - GET /api/v1/cms/hero - 200 - 45.2ms
```

## File Uploads

### Uploading Images

```bash
# Upload via curl
curl -X POST "http://localhost:8000/api/v1/assets/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/image.jpg"
```

**Response**:
```json
{
  "success": true,
  "message": "File uploaded successfully",
  "data": {
    "id": 1,
    "filename": "a1b2c3d4_image.jpg",
    "file_url": "/static/uploads/a1b2c3d4_image.jpg",
    "mime_type": "image/jpeg",
    "file_size": 102400
  }
}
```

### Using Uploaded Images in CMS

After uploading, use the returned `file_url` in your CMS payloads:

```bash
curl -X PUT "http://localhost:8000/api/v1/cms/hero" \
  -H "Content-Type: application/json" \
  -d '{
    "slides": [
      {
        "title": "SPICY FRIED CHICKEN",
        "subtitle": "WELCOME FRESHEAT",
        "image_path": "/static/uploads/a1b2c3d4_image.jpg",
        "cta_text": "ORDER NOW",
        "cta_link": "/menu"
      }
    ]
  }'
```

### Allowed File Types

- `image/jpeg` (.jpg, .jpeg)
- `image/png` (.png)
- `image/gif` (.gif)
- `image/webp` (.webp)
- `image/svg+xml` (.svg)

### File Size Limit

Default: 10MB (configurable via `MAX_UPLOAD_MB`)

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start all services (MySQL + Backend + Adminer)
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove all data
docker-compose down -v
```

### Services

| Service | Port | Description |
|---------|------|-------------|
| `backend` | 8000 | FastAPI application |
| `mysql` | 3306 | MySQL database |
| `adminer` | 8080 | Database admin UI |

### Access Points

- **API**: http://localhost:8000
- **Swagger**: http://localhost:8000/docs
- **Adminer**: http://localhost:8080 (server: `mysql`, user: `root`)

## Project Structure

```
backend/
├── alembic/                    # Database migrations
│   ├── versions/               # Migration scripts
│   │   └── 001_initial.py      # Initial schema
│   ├── env.py                  # Alembic environment
│   └── script.py.mako          # Migration template
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes_cms.py       # CMS endpoints
│   │       ├── routes_news.py      # News CRUD endpoints
│   │       ├── routes_assets.py    # File upload endpoints
│   │       └── routes_health.py    # Health check endpoints
│   ├── core/
│   │   ├── config.py           # Pydantic Settings
│   │   ├── logging.py          # Logging configuration
│   │   └── ddl.py              # DDL auto behavior
│   ├── db/
│   │   ├── base.py             # SQLAlchemy Base
│   │   ├── session.py          # Database session
│   │   └── models/
│   │       ├── cms.py          # CMS models (17 sections)
│   │       ├── news.py         # News model
│   │       └── assets.py       # Assets model
│   ├── schemas/
│   │   ├── cms.py              # CMS Pydantic schemas
│   │   ├── news.py             # News schemas
│   │   └── assets.py           # Assets schemas
│   ├── services/
│   │   ├── cms_service.py      # CMS business logic
│   │   ├── news_service.py     # News business logic
│   │   └── assets_service.py   # Asset management
│   └── utils/
│       ├── api_response.py     # Standard response format
│       └── file_storage.py     # File handling utilities
├── uploads/                    # Uploaded files directory
├── logs/                       # Application logs
├── main.py                     # FastAPI application entry
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
├── .env.example                # Example configuration
├── alembic.ini                 # Alembic configuration
├── Dockerfile                  # Docker build file
├── docker-compose.yml          # Docker Compose config
└── README.md                   # This file
```

## API Endpoints Reference

### Health Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Full health check |
| GET | `/api/v1/health/live` | Liveness probe |
| GET | `/api/v1/health/ready` | Readiness probe |

### CMS Endpoints (Public GET, Admin PUT)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/cms/home` | Get all sections (aggregated) |
| GET | `/api/v1/cms/site-branding` | Get site branding |
| PUT | `/api/v1/cms/site-branding` | Update site branding |
| GET | `/api/v1/cms/header` | Get header config |
| PUT | `/api/v1/cms/header` | Update header config |
| GET | `/api/v1/cms/hero` | Get hero section |
| PUT | `/api/v1/cms/hero` | Update hero section |
| GET | `/api/v1/cms/about` | Get about section |
| PUT | `/api/v1/cms/about` | Update about section |
| GET | `/api/v1/cms/services` | Get services section |
| PUT | `/api/v1/cms/services` | Update services section |
| GET | `/api/v1/cms/stats` | Get stats section |
| PUT | `/api/v1/cms/stats` | Update stats section |
| GET | `/api/v1/cms/testimonials` | Get testimonials |
| PUT | `/api/v1/cms/testimonials` | Update testimonials |
| GET | `/api/v1/cms/gallery` | Get gallery |
| PUT | `/api/v1/cms/gallery` | Update gallery |
| GET | `/api/v1/cms/footer` | Get footer config |
| PUT | `/api/v1/cms/footer` | Update footer config |
| GET | `/api/v1/cms/seo` | Get SEO config |
| PUT | `/api/v1/cms/seo` | Update SEO config |
| GET | `/api/v1/cms/offers` | Get offers section |
| PUT | `/api/v1/cms/offers` | Update offers section |
| GET | `/api/v1/cms/popular-dishes` | Get popular dishes |
| PUT | `/api/v1/cms/popular-dishes` | Update popular dishes |
| GET | `/api/v1/cms/cta` | Get CTA section |
| PUT | `/api/v1/cms/cta` | Update CTA section |
| GET | `/api/v1/cms/food-menu` | Get food menu |
| PUT | `/api/v1/cms/food-menu` | Update food menu |
| GET | `/api/v1/cms/special-offer` | Get special offer/timer |
| PUT | `/api/v1/cms/special-offer` | Update special offer |
| GET | `/api/v1/cms/chef` | Get chef section |
| PUT | `/api/v1/cms/chef` | Update chef section |
| GET | `/api/v1/cms/client-logos` | Get client logos |
| PUT | `/api/v1/cms/client-logos` | Update client logos |

### News Endpoints (Full CRUD)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/news` | List published news (public) |
| GET | `/api/v1/news/{slug}` | Get news by slug (public) |
| POST | `/api/v1/news` | Create news article |
| GET | `/api/v1/news/admin/list` | List all news (admin) |
| GET | `/api/v1/news/admin/{id}` | Get news by ID (admin) |
| PATCH | `/api/v1/news/{id}` | Update news article |
| DELETE | `/api/v1/news/{id}` | Delete news article |
| PATCH | `/api/v1/news/{id}/publish` | Publish article |
| PATCH | `/api/v1/news/{id}/unpublish` | Unpublish article |

### Asset Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/assets/upload` | Upload file |
| GET | `/api/v1/assets` | List all assets |
| GET | `/api/v1/assets/{id}` | Get asset by ID |
| PATCH | `/api/v1/assets/{id}` | Update asset metadata |
| DELETE | `/api/v1/assets/{id}` | Delete asset |
| GET | `/static/uploads/{filename}` | Serve uploaded file |

## Response Format

All endpoints return a consistent JSON structure:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { ... },
  "errors": null
}
```

Error response:
```json
{
  "success": false,
  "message": "Error description",
  "data": null,
  "errors": ["Detailed error message"]
}
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Formatting

```bash
# Install formatters
pip install black isort

# Format code
black .
isort .
```

## License

MIT License - See LICENSE file for details.

## Support

For issues or questions, please open a GitHub issue.

---

**Built with ❤️ using FastAPI, SQLAlchemy, and Python**
