
# Moving Platform

A Django-based B2C/B2B marketplace for moving services.  
Clients create moving orders, and registered moving companies can send offers (quotes).  
The client can compare offers, select a company, and rate the service.

---

## Features

### For Clients
- Registration & login
- Create moving order (with addresses, date/time, description)
- See all their orders and detailed status
- Receive offers from different moving companies
- Compare and accept any offer
- View history of moves and ratings
- Get notifications about offers and status changes

### For Companies (Moving Providers)
- Registration as a company
- Company profile (info, phone, description, rating)
- View all open orders from clients
- Send offers (quotes) on any order (with price and comment)
- See all their submitted offers and their status (pending/accepted/declined)
- Get notifications about orders and when client accepts/declines an offer

### For Staff/Admin
- Admin interface for managing users, companies, orders, and offers
- Staff dashboard: view and manage all orders, change status, view analytics

---

## Models

- **User** (default Django `auth.User`)
- **Company** — OneToOne to User (for company accounts)
- **Order** — moving order (customer=User, details, status, chosen_offer)
- **Offer** — an offer from a company on a particular order (with price, status, message)
- **(Optionally) Review** — client rates company after completed order

---

## Key Statuses

- **Order**
  - `offers` (waiting for companies to submit quotes)
  - `offer_selected` (client accepted an offer)
  - `in_progress`
  - `done`
  - `cancelled`

- **Offer**
  - `pending`
  - `accepted`
  - `declined`

---

## Project Structure

```
moving_platform/
  manage.py
  moving_platform/
    settings.py
    urls.py
    ...
  orders/
    models.py
    views.py
    urls.py
    forms.py
    templates/
      orders/
        base.html
        create_order.html
        my_orders.html
        order_detail.html
        company_order_list.html
        company_order_detail.html
        company_my_offers.html
        staff_order_list.html
        staff_order_detail.html
      registration/
        login.html
        signup.html
        password_reset.html
    migrations/
  templates/
    registration/
      login.html
      ...
```

---

## Setup and Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/moving-platform.git
   cd moving-platform
   ```

2. **Create a virtual environment and activate**
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Linux/Mac
   venv\Scriptsctivate      # on Windows
   ```

3. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```
   Minimal requirements:
   ```
   Django>=4.2
   django-widget-tweaks
   ```

4. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the app:**
   - http://localhost:8000/

---

## Quick Start for Roles

### As a Client
- Register via `/signup/`
- Create a new moving order
- Wait for offers from companies
- View your orders and accept one of the offers

### As a Company
- Register as a company account (or ask admin to assign company profile)
- Fill out company profile
- Browse open orders from clients
- Send your offer (price + message)
- Track status of your offers

### As an Admin/Staff
- Access Django admin: `/admin/`
- Manage users, companies, orders, and offers
- Staff dashboard: `/orders/staff/orders/`

---

## Important Views/URLs

- `/orders/create/` — create a new order (client)
- `/orders/my/` — list client’s own orders
- `/orders/<order_id>/` — order details with offers (client)
- `/orders/company/orders/` — new open orders for companies
- `/orders/company/orders/<order_id>/` — order details and offer form (company)
- `/orders/company/my_offers/` — list of all offers sent by the company
- `/orders/staff/orders/` — staff dashboard for all orders

---

## How to Extend

- Add reviews and ratings
- Integrate email/SMS notifications
- Add Stripe/PayPal for prepayments
- Add geo-suggestions for addresses
- Build mobile frontend (REST API ready)
- Deploy to AWS or any cloud (see README for deployment tips)

---

## License

MIT License

---

**Built with Django for moving companies and their customers.**
