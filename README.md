# Physical Product Catalogue API

REST API for managing physical product records in a catalogue. Built with **FastAPI** (Python), backed by **SQLite**, and secured with API-key authentication.

## Features

- **CRUD operations** for physical products (SKU, pricing, inventory, metadata)
- **API-key authentication** via `X-API-Key` header
- **Input validation** with Pydantic (empty fields, bad data rejected)
- **Auto-generated Swagger/OpenAPI docs** at `/docs`
- **Filtering & pagination** on the list endpoint
- **Docker support** for single-command deployment

## Quick Start

### Option 1: Docker Compose (recommended)

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

### Option 2: Run locally

```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env to set your API_KEY

# Start the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the server is running, visit:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI JSON**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## Authentication

All `/products` endpoints require an `X-API-Key` header.

The default demo key is `demo-api-key-2024`. Change it in `.env` for production.

## Example curl Requests

### Health check

```bash
curl http://localhost:8000/
```

### Create a product

```bash
curl -X POST http://localhost:8000/products \
  -H "X-API-Key: demo-api-key-2024" \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "WIDGET-001",
    "name": "Premium Widget",
    "description": "A high-quality widget for everyday use.",
    "price": 29.99,
    "currency": "USD",
    "inventory_count": 150,
    "category": "Widgets",
    "weight_kg": 0.5,
    "dimensions": "10x5x3 cm",
    "brand": "WidgetCo"
  }'
```

### List all products

```bash
curl http://localhost:8000/products \
  -H "X-API-Key: demo-api-key-2024"
```

### List with filters

```bash
curl "http://localhost:8000/products?category=Widgets&is_active=true&limit=10" \
  -H "X-API-Key: demo-api-key-2024"
```

### Get a product by ID

```bash
curl http://localhost:8000/products/1 \
  -H "X-API-Key: demo-api-key-2024"
```

### Update a product

```bash
curl -X PUT http://localhost:8000/products/1 \
  -H "X-API-Key: demo-api-key-2024" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 24.99,
    "inventory_count": 200
  }'
```

### Delete a product

```bash
curl -X DELETE http://localhost:8000/products/1 \
  -H "X-API-Key: demo-api-key-2024"
```

### Request without API key (returns 401)

```bash
curl http://localhost:8000/products
```

## Product Fields

| Field           | Type    | Required | Description                          |
|-----------------|---------|----------|--------------------------------------|
| sku             | string  | Yes      | Unique stock-keeping unit identifier |
| name            | string  | Yes      | Product name                         |
| description     | string  | No       | Product description                  |
| price           | float   | Yes      | Price (must be > 0)                  |
| currency        | string  | No       | ISO 4217 code (default: USD)         |
| inventory_count | integer | No       | Stock quantity (default: 0)          |
| category        | string  | No       | Product category                     |
| weight_kg       | float   | No       | Weight in kilograms                  |
| dimensions      | string  | No       | Dimensions (e.g. "10x5x3 cm")       |
| brand           | string  | No       | Brand name                           |
| is_active       | boolean | No       | Active in catalogue (default: true)  |

## HTTP Status Codes

| Code | Meaning                                    |
|------|--------------------------------------------|
| 200  | Success                                    |
| 201  | Product created successfully               |
| 401  | Missing or invalid API key                 |
| 404  | Product not found                          |
| 409  | Duplicate SKU conflict                     |
| 422  | Validation error (bad input)               |

## Postman Collection

Import `postman_collection.json` into Postman for quick testing. The collection uses variables `{{base_url}}` and `{{api_key}}` that you can configure in the collection settings.

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── auth.py        # API key authentication
│   ├── config.py      # Environment configuration
│   ├── database.py    # SQLAlchemy setup
│   ├── main.py        # FastAPI application entry point
│   ├── models.py      # Database models
│   ├── routes.py      # API route handlers
│   └── schemas.py     # Pydantic request/response schemas
├── .env.example       # Environment template
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── postman_collection.json
├── README.md
└── requirements.txt
```

## License

MIT
