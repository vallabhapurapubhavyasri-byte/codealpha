# StyleCart - Simple E-commerce Store

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1%2B-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A modern, responsive, beginner-friendly Full-Stack E-Commerce web application developed as **Task 1** for the **CodeAlpha Full Stack Development Internship**.

---

## 📖 Project Overview

**StyleCart** is an end-to-end e-commerce web platform built with **Python**, **Django**, and **Bootstrap 5**. It provides a complete online shopping experience from browsing products and filtering categories to managing shopping carts, creating user accounts, and processing customer orders.

The application follows Django's clean **Model-View-Template (MVT)** architectural pattern and uses Django's default SQLite database for lightweight, zero-configuration local development.

---

## ✨ Features

### 🛍️ Customer Experience
1. **Home Page**: Modern hero showcase, key service guarantees (free shipping, security, returns), and featured arrivals.
2. **Product Catalog**: Clean grid layout displaying product cards with titles, categories, pricing, descriptions, and stock tags.
3. **Live Search & Category Filtering**: Search products by keyword (in titles or descriptions) or filter by category pills (*Apparel*, *Footwear*, *Accessories*, *Bags*, *Electronics*).
4. **Product Details Page**: Full specifications, real-time inventory counter, quantity picker, and "You Might Also Like" product recommendations.
5. **Interactive Shopping Cart**:
   * Add products with custom quantities.
   * Increase (`+`) and decrease (`-`) quantities directly in the cart table.
   * Auto-remove when quantity drops to 0 or manual removal with trash icon.
   * Real-time calculation of item subtotals and grand order total.
   * Persistent session storage (items persist across page refreshes).
6. **Real-Time Navbar Cart Counter**: A dynamic badge badge displaying total items across every page via a custom Django Context Processor.
7. **Customer Checkout**: Shipping details form (name, email, phone, street address, city, postal code) and payment method selection (*Cash on Delivery* or *Card Demo*).
8. **Automated Order Processing**:
   * Deducts purchased stock quantities from product inventory.
   * Clears the user's shopping cart upon successful checkout.
   * Redirects to an order confirmation receipt page.
9. **Printable Order Receipt**: Detailed order summary with unique Order ID (`#STYLE-X`), customer shipping details, items breakdown, and a one-click print receipt button.

### 🔐 User Authentication
10. **User Registration**: Clean signup with client and server-side validation (matching passwords, minimum length, duplicate checks).
11. **Secure Password Hashing**: Utilizes Django's PBKDF2 with SHA-256 password hashing.
12. **User Login & Session Management**: Authenticates users and starts encrypted HTTP sessions.
13. **User Logout**: Cleans up session and returns to the home page with flash confirmation.
14. **Dynamic Navigation Bar**: Displays user greeting dropdown and logout button when logged in, or login/register buttons when logged out.

### 🛡️ Administration & Management
15. **Django Admin Panel (`/admin/`)**:
    * **Product Management**: Create, edit, delete products, upload photos, and fast inline editing of price & inventory directly on the list table.
    * **Order Management**: Review orders, see customer shipping addresses, update statuses (`Pending`, `Processing`, `Shipped`, `Delivered`), and view embedded order items.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
|---|---|---|
| **Backend Framework** | Python 3 + Django | Server routing, ORM, views, and authentication |
| **Frontend Layout** | HTML5 + CSS3 | Semantic markup and custom styling |
| **CSS Framework** | Bootstrap 5.3 + Bootstrap Icons | Grid layout, modals, dropdowns, and responsive navbar |
| **Client Scripting** | Vanilla JavaScript | Auto-dismissing alerts, quantity guards, and image fallbacks |
| **Database** | SQLite3 (`db.sqlite3`) | Default relational database |
| **Image Processing** | Pillow | Handling image upload fields in Django models |

---

## 📁 Project Directory Structure

```text
stylecart/
├── config/                     # Project configuration directory
│   ├── settings.py             # Master settings (apps, templates, static/media, context processors)
│   ├── urls.py                 # Master URL dispatcher
│   ├── wsgi.py                 # WSGI gateway
│   └── asgi.py                 # ASGI gateway
├── store/                      # Main e-commerce application
│   ├── migrations/             # Database migration blueprints
│   ├── admin.py                # Admin site configuration for Product, Order, OrderItem
│   ├── context_processors.py   # Global cart counter badge processor
│   ├── models.py               # Database schemas (Product, Order, OrderItem)
│   ├── tests.py                # 8 comprehensive automated test suites
│   ├── urls.py                 # Application URL routing
│   └── views.py                # Business logic and request handlers
├── templates/                  # Django HTML templates
│   ├── base.html               # Master layout (navbar, flash alerts, footer)
│   ├── home.html               # Home page with hero and featured products
│   ├── products.html           # Product catalog with search and category pills
│   ├── product_detail.html     # Product details with quantity form
│   ├── cart.html               # Shopping cart table & summary
│   ├── checkout.html           # Shipping address & order review form
│   ├── order_success.html      # Printable order confirmation receipt
│   ├── login.html              # User sign-in page
│   └── register.html           # User registration page
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css           # Custom styles, transitions, responsive media queries
│   └── js/
│       └── main.js             # Client interactivity (auto-alert fade, bounds check)
├── media/                      # Uploaded product images
├── manage.py                   # Django CLI tool
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

---

## 🚀 How to Run the Project Locally

### Prerequisites
* Python 3.10 or higher installed on your computer.
* Git installed (optional, for cloning).

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/stylecart.git
cd stylecart
```

### 2. Create and Activate a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If you encounter an execution policy error on PowerShell, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py migrate
```

### 5. (Optional) Create an Admin Superuser
```bash
python manage.py createsuperuser
```
*Follow the terminal prompts to set your username and password.*

*(A default admin account is pre-configured for evaluation:*
* **Username:** `admin`
* **Password:** `admin123`

### 6. Start the Development Server
```bash
python manage.py runserver
```

Open your browser and visit:
👉 **`http://127.0.0.1:8000/`**

---

## 🧪 Running Automated Tests

StyleCart includes a full test suite verifying models, authentication, cart calculations, checkout processing, and admin access.

To run all automated tests:
```powershell
python manage.py test
```

Expected output:
```text
Ran 8 tests in ~25s
OK
```

---

## 🖼️ Application Pages & Visual Flow

* **Home (`/`)**: Discover featured products and core values.
* **Catalog (`/products/`)**: Explore all items, search by text, and filter by categories.
* **Product Details (`/product/<id>/`)**: Inspect descriptions, stock counts, and add items to cart.
* **Shopping Cart (`/cart/`)**: Modify item quantities, calculate subtotals, or remove items.
* **Checkout (`/checkout/`)**: Enter delivery address and choose payment method.
* **Order Receipt (`/order/success/<id>/`)**: Printable invoice with order ID and summary.
* **Authentication (`/login/`, `/register/`)**: Create accounts and manage sessions.
* **Admin Dashboard (`/admin/`)**: Complete back-office control over inventory and orders.

---

## 🔮 Future Enhancements

* [ ] Integrate payment gateways (Stripe, Razorpay, or PayPal).
* [ ] Customer order history page under user profile.
* [ ] Product customer ratings and reviews.
* [ ] Email notifications for order confirmations using Django's SMTP backend.
* [ ] Wishlist / Favorites feature for registered users.
* [ ] Coupon codes and promotional discount application.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Developed for **CodeAlpha Full Stack Development Internship - Task 1**.
