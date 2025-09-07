<div align="center">
  <h1>🛒 Kidora API</h1>
  <p><strong>Scalable E-commerce Backend Platform</strong></p>
  
  <a href="https://djangoproject.com/">
    <img src="https://img.shields.io/badge/Django-5.2.4-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  </a>
  <a href="https://www.django-rest-framework.org/">
    <img src="https://img.shields.io/badge/DRF-3.16.0-ff1709?style=for-the-badge&logo=django&logoColor=white" alt="DRF">
  </a>
  <a href="https://python.org/">
    <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License">
  </a>
</div>

---

## 🎯 Overview

**Kidora API** is a robust, production-ready RESTful backend for e-commerce platforms, built with Django REST Framework. It supports modern features like user authentication, product management, wishlists, orders, and more, with a focus on security, scalability, and developer experience.

### ✨ Key Features

- **🔐 JWT Authentication** (Djoser + Simple JWT)
- **🛍️ Product Catalog** with advanced filtering, search, and pagination
- **❤️ Wishlist System** (add/remove, track status per product)
- **🛒 Cart & Order Management** with user association
- **📦 Media Handling** for product images
- **📚 API Documentation** (Swagger/ReDoc)
- **🔒 Security** with permissions and validation
- **⚡ Performance** with optimized queries and pagination

## 🛠 Technology Stack

| Component     | Technology            | Version       |
| ------------- | --------------------- | ------------- |
| **Framework** | Django                | 5.2.4         |
| **API**       | Django REST Framework | 3.16.0        |
| **Auth**      | Djoser + Simple JWT   | 2.3.3 + 5.5.1 |
| **Docs**      | drf-yasg              | 1.21.10       |
| **Database**  | PostgreSQL/SQLite     | -             |
| **Media**     | Pillow                | 11.3.0        |

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/Kidora-API.git
cd Kidora-API

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py migrate
python manage.py createsuperuser

# (Optional) Load sample data
python manage.py loaddata fixtures/product_data.json

# Run server
python manage.py runserver
```

### Access Points

- **API Root**: `http://127.0.0.1:8000/api/v1/`
- **Swagger Docs**: `http://127.0.0.1:8000/swagger/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`

## 📚 API Documentation

### Authentication

All protected endpoints require JWT token in header:

```http
Authorization: JWT your_access_token_here
```

### Core Endpoints

**Authentication:**

```
POST /api/v1/auth/users/                 # Register
POST /api/v1/auth/jwt/create/            # Login
POST /api/v1/auth/jwt/refresh/           # Refresh token
```

**Products:**

```
GET    /api/v1/products/                         # List products
GET    /api/v1/products/{id}/                    # Product details
POST   /api/v1/products/{id}/add_to_wishlist/    # Add to wishlist
POST   /api/v1/products/{id}/remove_from_wishlist/ # Remove from wishlist
```

**Wishlist:**

```
GET    /api/v1/wishlists/                        # List all products in wishlist
GET    /api/v1/wishlists/{product_id}/           # Get a product from wishlist
DELETE /api/v1/wishlists/{product_id}/           # Remove product from wishlist
```

**Cart & Orders:**

```
GET    /api/v1/carts/                            # User's cart
POST   /api/v1/carts/                            # Create cart
...
```

## 🏗️ Project Structure

```
Kidora-API/
├── api/                # API routing and config
├── product/            # Product, wishlist, review logic
├── order/              # Cart, order, wishlist models
├── users/              # User management
├── fixtures/           # Sample data
├── media/              # Uploaded files
└── kidora/             # Django settings
```

## 🧪 Testing

```bash
python manage.py test
```

## 🚀 Deployment

- Use Gunicorn, Nginx, and PostgreSQL for production.
- See `.env.example` for environment variables.

## 🔒 Security

- JWT authentication
- Object-level permissions
- Input validation
- CORS protection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Commit and push
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Nazmul Hossain**  
GitHub: [@nazmulh24](https://github.com/nazmulh24)  
Email: snazmulhossains24@gmail.com

---

<div align="center">

### 🌟 Thank you for using Kidora API!

**If you found this project helpful, please ⭐ star the repository!**

_Built with ❤️ using Django REST Framework_

</div>
