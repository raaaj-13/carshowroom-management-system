# AutoShowroom - Car Booking Web Application

## Overview
The AutoShowroom web application provides a platform to browse and book cars from a premium collection. The application features a modern, user-friendly interface with car galleries and comprehensive booking management.

## Application Features
- **Homepage**: Welcome banner with "Browse & Book Now" functionality
- **Car Gallery**: Display of available cars with images, names, and model years
- **User Authentication**: Login and Register functionality
- **Car Browsing**: View available cars like Toyota Camry, Honda Civic, Ford Mustang, BMW X5
- **Navigation**: Clean navigation bar with Home, Login, and Register links

## Technologies Used
- **Backend**: Flask (Python web framework)
- **Database**: PostgreSQL
- **Frontend**: HTML templates with responsive design

## Login Credentials

| Role  | Username | Password   |
|-------|----------|------------|
| Admin | admin    | admin123   |
| User  | gmail    | gmail123   |

## Features Added
- Car images on Home, User Dashboard, Admin Dashboard
- Image gallery strip on Admin Dashboard
- Car photos in inventory table (Admin)
- Hero banner with car photo
- User Dashboard: welcome banner + booking stats
- Admin Dashboard: stats with icons, gallery view, photo table

## Setup Instructions
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup**:
   ```bash
   psql -U postgres -f schema.sql
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

## Access the Application
The application is accessible at: **http://127.0.0.1:5000** or **http://localhost:5000**

## Screenshots
- **Homepage**: `screenshots/homepage.png`
- **Login Page**: `screenshots/login.png`
- **User Dashboard**: `screenshots/user_dashboard.png`
- **Admin Dashboard**: `screenshots/admin_dashboard.png`

## Database Configuration
The Flask application connects to the `postgres` database (not `car_showroom`) for user and car data management.
![Homepage](screenshots/homepage.png)
![Login Page](screenshots/login.png)
![User Dashboard](screenshots/user_dashboard.png)
![Admin Dashboard](screenshots/admin_dashboard.png)