# CineManager — Theater Management System

> A full-stack theater management system for managing movies, screening halls, show schedules, customers, and ticket bookings — built with MySQL, Python (Flask), and vanilla HTML/CSS/JS.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Reference](#api-reference)
- [Database Schema](#database-schema)
- [Usage Guide](#usage-guide)
- [Troubleshooting](#troubleshooting)

---

## Overview

CineManager is a lightweight, self-hosted theater operations platform. It provides a clean management interface for cinema staff to handle the full operational workflow — from onboarding movies and scheduling shows, to registering customers and processing ticket bookings — all in real time through a browser-based dashboard.

The system is intentionally simple: no frontend framework, no ORM, no containerization required. Just Python, MySQL, and a browser.

---

## Features

| Module | Capabilities |
|---|---|
| **Dashboard** | Live stats — total movies, theaters, active shows, customers, confirmed bookings, and total revenue |
| **Movies** | Add, edit, delete movies with title, genre, duration, language, rating, and description |
| **Theaters** | Manage screening halls with name, seating capacity, and description |
| **Shows** | Schedule movies in theaters with date, time, ticket price, and seat availability tracking |
| **Customers** | Register and manage customers with name, email, and phone |
| **Bookings** | Create bookings with automatic seat deduction; cancel bookings with automatic seat restoration |

Additional capabilities:
- Real-time search and filter on every data table
- Confirmation dialogs before destructive actions
- Toast notifications for all operations
- Transactional booking and cancellation (atomically updates seat count)
- Duplicate email detection for customers

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Database | MySQL | 8.0+ |
| Backend | Python + Flask | 3.10+ / 3.x |
| API | Flask-CORS | Latest |
| DB Driver | mysql-connector-python | Latest |
| Frontend | HTML5 + CSS3 + Vanilla JS | — |
| Fonts | Inter, Playfair Display, JetBrains Mono | Google Fonts |

No frontend build tools, no npm, no webpack. The entire frontend is a single `index.html` file.

---

## Project Structure

```
theater/
│
├── schema.sql          # Database schema + seed data
├── app.py              # Flask REST API (all endpoints)
├── requirements.txt    # Python dependencies
├── index.html          # Complete frontend (HTML + CSS + JS)
└── README.md           # This file
```

---

## Prerequisites

Before starting, make sure you have the following installed:

- **Python 3.10 or higher** — [python.org](https://www.python.org/downloads/)
- **MySQL 8.0 or higher** — [mysql.com](https://dev.mysql.com/downloads/)
- **pip** — comes bundled with Python
- A modern browser (Chrome, Firefox, Edge)

---

## Installation & Setup

### Step 1 — Clone or download the project

Place all files in a folder, for example:
```
C:\Users\YourName\theater\
```

### Step 2 — Set up the database

Open the **MySQL 8.0 Command Line Client** from your Start menu, enter your root password, then run:

```sql
source C:/Users/YourName/theater/schema.sql
```

This will create the `theater_db` database, all 5 tables, and insert sample seed data (3 theaters, 5 movies, 5 shows, 3 customers).

Verify it worked:
```sql
USE theater_db;
SHOW TABLES;
```

You should see all 5 tables listed.

### Step 3 — Configure the database connection

Open `app.py` and update the `DB_CONFIG` block with your MySQL credentials:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password',   # update this
    'database': 'theater_db',
    'port': 3306
}
```

### Step 4 — Install Python dependencies

Open a terminal in your project folder and run:

```bash
pip install -r requirements.txt
```

This installs `flask`, `flask-cors`, and `mysql-connector-python`.

---

## Running the Application

Start the Flask backend:

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Debugger is active!
```

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

> **Important:** Always access the app through `http://127.0.0.1:5000` — do not open `index.html` directly as a file. The frontend uses relative API URLs that only work when served through Flask.

To stop the server, press `CTRL + C`.

---

## API Reference

All endpoints return and accept `application/json`. Base URL: `http://localhost:5000`

### Health

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Check if the API is running |
| GET | `/api/stats` | Dashboard summary statistics |

### Movies — `/api/movies`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/movies` | List all movies |
| POST | `/api/movies` | Create a movie |
| GET | `/api/movies/:id` | Get a movie |
| PUT | `/api/movies/:id` | Update a movie |
| DELETE | `/api/movies/:id` | Delete a movie |

```json
{
  "title": "Inception",
  "genre": "Sci-Fi",
  "duration_minutes": 148,
  "language": "English",
  "rating": "PG-13",
  "description": "A thief who steals corporate secrets..."
}
```

### Theaters — `/api/theaters`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/theaters` | List all theaters |
| POST | `/api/theaters` | Create a theater |
| GET | `/api/theaters/:id` | Get a theater |
| PUT | `/api/theaters/:id` | Update a theater |
| DELETE | `/api/theaters/:id` | Delete a theater |

```json
{
  "name": "Grand Hall",
  "total_seats": 200,
  "description": "Main screening hall"
}
```

### Shows — `/api/shows`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/shows` | List all shows with movie and theater details |
| POST | `/api/shows` | Schedule a show |
| GET | `/api/shows/:id` | Get a show |
| PUT | `/api/shows/:id` | Update a show |
| DELETE | `/api/shows/:id` | Delete a show |

```json
{
  "movie_id": 1,
  "theater_id": 2,
  "show_date": "2026-05-10",
  "show_time": "18:30:00",
  "ticket_price": 250.00,
  "status": "active"
}
```

### Customers — `/api/customers`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/customers` | List all customers |
| POST | `/api/customers` | Register a customer |
| GET | `/api/customers/:id` | Get a customer |
| PUT | `/api/customers/:id` | Update a customer |
| DELETE | `/api/customers/:id` | Delete a customer |

```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "phone": "9876543210"
}
```

### Bookings — `/api/bookings`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/bookings` | List all bookings with full details |
| POST | `/api/bookings` | Create a booking |
| GET | `/api/bookings/:id` | Get a booking |
| PUT | `/api/bookings/:id/cancel` | Cancel a booking (restores seats) |
| DELETE | `/api/bookings/:id` | Delete a booking record |

```json
{
  "show_id": 3,
  "customer_id": 1,
  "num_seats": 2
}
```

Response:
```json
{
  "id": 12,
  "total_amount": 500.00,
  "message": "Booking confirmed"
}
```

---

## Database Schema

```
theaters        movies           shows                customers       bookings
───────────     ──────────────   ──────────────────   ───────────     ────────────────
id (PK)         id (PK)          id (PK)              id (PK)         id (PK)
name            title            movie_id (FK)        name            show_id (FK)
total_seats     genre            theater_id (FK)      email (UNIQUE)  customer_id (FK)
description     duration_mins    show_date            phone           num_seats
created_at      language         show_time            created_at      total_amount
                rating           ticket_price                         booking_status
                description      available_seats                      booked_at
                created_at       status
                                 created_at
```

Cascading deletes are configured — deleting a movie removes its shows; deleting a show removes its bookings.

---

## Usage Guide

### Creating a booking

1. Ensure at least one Movie, Theater, Show, and Customer exist
2. Go to **Bookings** → **+ New Booking**
3. Select a customer and an active show
4. Enter number of seats — total is calculated automatically
5. Click **Confirm Booking** — seats are deducted immediately

### Cancelling a booking

Navigate to **Bookings**, find a confirmed booking, and click **Cancel**. Seats are automatically restored to the show.

### Scheduling a show

Go to **Shows** → **+ Add Show**, pick a movie and theater, set the date, time, and price. Available seats are automatically set to the theater's full capacity.

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `mysql is not recognized` | MySQL not in PATH | Use MySQL Command Line Client from Start menu |
| `Access denied for user 'root'` | Wrong password in app.py | Update `DB_CONFIG['password']` |
| Dashboard shows "Cannot connect to backend" | Flask not running | Run `python app.py`, then visit `http://127.0.0.1:5000` |
| `timedelta is not JSON serializable` | Outdated app.py | Use the latest version of app.py |
| Booking modal opens empty | No active shows with seats | Add a show via the Shows page first |
| `< operator` error in PowerShell | PowerShell redirect limitation | Use `Get-Content schema.sql \| mysql -u root -p` |

---

## License

Provided for educational and internal use. No restrictions — modify and use freely.

---

*CineManager · Flask · MySQL · Vanilla JS*
