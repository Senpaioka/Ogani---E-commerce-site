# 🛒 Ogani - Organic Food & Grocery E-Commerce Platform

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-brightgreen?style=for-the-badge&logo=render)](https://ogani-e-commerce-site.onrender.com)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![uv](https://img.shields.io/badge/Package%20Manager-uv-DE5D43?style=for-the-badge)](https://github.com/astral-sh/uv)

**Ogani** is a full-featured, modern E-Commerce web application for organic products and grocery shopping built with **Django 6.1** and **Python 3.13+**. It offers a seamless shopping experience for customers and a comprehensive management interface for store administrators.

---

## 🚀 Live Demo

Check out the live deployment of the platform:
👉 **[Ogani E-Commerce Live App](https://ogani-e-commerce-site.onrender.com)**

---

## ✨ Key Features

### 👤 User Account & Authentication
- **Role-Based Access Control (RBAC):** Supports `User`, `Member`, and `Admin` role privileges.
- **Social Authentication:** Integration with Google and third-party social log-ins via `django-allauth`.
- **Profile Management:** User profiles with customizable avatars, contact information, and shipping address tracking.

### 🛍️ Product Catalog & Shopping Experience
- **Categorized Browsing:** Filter products by categories such as *Meats*, *Fruits*, *Vegetables*, *Drinks*, and *Others*.
- **Rich Product Detail Pages:** Includes high-resolution product thumbnails, pricing, weight metrics, stock status, and shipping information.
- **Dynamic Search & Filtering:** Quick product lookups and dynamic category filtering.

### 🛒 Shopping Cart, Wishlist & Discounts
- **Session & User Carts:** Supports guest cart tracking using session IDs (`CartID`) seamlessly synced upon user authentication.
- **Wishlist Support:** Quick-add items to user wishlists for future purchases.
- **Coupon & Promo System:** Apply product-specific or storewide percentage discount coupons at checkout.

### 💳 Payments & Order Management
- **PayPal Integration:** Integrated checkout using `django-paypal` IPN and custom payment handler workflows.
- **Purchase History:** Full transaction log recording customer order completions and purchase records.

### ⭐ Reviews & Ratings
- **Product Reviews:** Customers can leave star ratings and text feedback on products.

### 📰 Blog & Content Management
- **Organic Life Blog:** Integrated blog module featuring category filters, author profiles, and comment sections.
- **Rich-Text Editor:** Articles formatted using `django-ckeditor` for clean media embedding.

### 📬 Contact & Newsletter
- **Store Locator & Inquiries:** Dedicated contact form submitting user messages directly to store admins.
- **Newsletter Subscription:** Automated subscriber collection for email marketing.

### 🎨 Modern Admin Interface
- **Unfold Admin Theme:** Enhanced Django admin interface styled with `django-unfold` for an intuitive dashboard experience.

---

## 🛠️ Tech Stack & Dependencies

- **Framework:** Django 6.1
- **Language:** Python 3.13+
- **Environment & Package Manager:** [uv](https://github.com/astral-sh/uv)
- **Database:** SQLite (Development) / PostgreSQL (`psycopg2-binary` ready for production)
- **Admin Suite:** `django-unfold`
- **Rich Text Editor:** `django-ckeditor`
- **Payments:** `django-paypal`
- **Static File Handling:** `whitenoise`
- **Code Quality & Tooling:** `ruff`, `mypy`, `poethepoet`
- **Deployment:** Render (Gunicorn WSGI server)

---

## 📁 Project Structure

```text
Ogani---E-commerce-site/
├── .env.example              # Sample environment variables config
├── pyproject.toml            # Project dependencies and Poe tasks configuration
├── manage.py                 # Django management script
├── src/
│   ├── config/               # Project configuration root
│   │   ├── settings/         # Base, dev, and production settings
│   │   ├── urls.py           # Top-level URL routing
│   │   ├── wsgi.py / asgi.py # Deployment entry points
│   └── apps/                 # Modular Django Applications
│       ├── accounts/         # User model, authentication & profile management
│       ├── blog/             # Blog posts, categories, and comments
│       ├── cart/             # Shopping cart, wishlist & coupons
│       ├── contact/          # Contact forms & newsletter subscriptions
│       ├── home/             # Landing page & index views
│       ├── payment/          # PayPal checkout & purchase history
│       ├── product/          # Product catalog, categories & gallery
│       └── review/           # Customer product reviews & ratings
├── templates/                # Global and app HTML templates
├── static/                   # CSS, JavaScript, and asset libraries
└── media/                    # User-uploaded files (product photos, avatars)
```

---

## ⚡ Quick Start Guide

### Prerequisites
- [Python 3.13+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv) package manager installed (Recommended)

### 1. Clone the Repository
```bash
git clone https://github.com/Senpaioka/Ogani---E-commerce-site.git
cd Ogani---E-commerce-site
```

### 2. Set Up Environment Variables
Copy the example environment file and update your variables:
```bash
cp .env.example .env
```

### 3. Install Dependencies
Using `uv`:
```bash
uv sync
```
*Or using standard pip:*
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r pyproject.toml
```

### 4. Apply Database Migrations
```bash
uv run poe migrate
# Or: python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
uv run poe dev
# Or: python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` in your browser.

---

## 🧰 Available Poe Tasks

This project utilizes `poethepoet` for simplified task running:

| Task Command | Description |
| :--- | :--- |
| `uv run poe dev` | Launches the Django development server |
| `uv run poe migrate` | Applies database migrations |
| `uv run poe makemigrations` | Prepares new database migrations |
| `uv run poe lint` | Runs `ruff` linter checks |
| `uv run poe format` | Formats codebase using `ruff` |

---

## 📄 Disclaimer & Attribution

- The base HTML/CSS template used in this project was sourced from **[Colorlib](https://colorlib.com/)** ([Ogani Template](https://colorlib.com/wp/template/ogani/)).
- All rights and credits for the original base template design belong to Colorlib. Modifications, backend implementation, and Django integration were built specifically for this project.

