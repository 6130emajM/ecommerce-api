# E-commerce API

REST API for managing users, products, and orders with Flask and MariaDB.

## Features
- User management with unique email validation
- Product catalog management
- Order system with many-to-many product relationships
- Duplicate product prevention in orders

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## Database
MariaDB database: `ecommerce_api`

## API Endpoints
### Users
- GET /users - All users
- GET /users/<id> - User by ID
- POST /users - Create user
- PUT /users/<id> - Update user
- DELETE /users/<id> - Delete user

### Products
- GET /products - All products
- GET /products/<id> - Product by ID
- POST /products - Create product
- PUT /products/<id> - Update product
- DELETE /products/<id> - Delete product

### Orders
- POST /orders - Create order
- PUT /orders/<order_id>/add_product/<product_id> - Add product to order
- DELETE /orders/<order_id>/remove_product/<product_id> - Remove product
- GET /orders/user/<user_id> - User's orders
# ecommerce-api

## Running the Project

Follow these steps to run the API locally.

### 1. Clone the repository

```
git clone <repository-url>
cd ecommerce_api
```

### 2. Create a virtual environment

```
python3 -m venv venv
```

### 3. Activate the virtual environment

```
source venv/bin/activate
```

### 4. Install dependencies

```
pip install -r requirements.txt
```

### 5. Run the application

```
python app.py
```

### 6. Access the API

The Flask development server will start on:

```
http://127.0.0.1:5000
```

You can test the API using tools such as HTTPie, Postman, or curl.

