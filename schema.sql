-- =========================================
-- Car Showroom - Database Setup
-- Run: psql -U postgres -f schema.sql
-- =========================================

CREATE DATABASE car_showroom;

\c car_showroom;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    role VARCHAR(10) DEFAULT 'user'
);

CREATE TABLE cars (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    color VARCHAR(30)
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    car_id INT REFERENCES cars(id),
    status VARCHAR(20) DEFAULT 'Pending',
    booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- DEFAULT ACCOUNTS
-- =========================================
-- Admin  → username: admin    password: admin123
-- User   → username: gmail    password: gmail123

INSERT INTO users (username, password, email, role) VALUES
  ('admin', 'admin123', 'admin@showroom.com', 'admin'),
  ('gmail', 'gmail123', 'gmail@showroom.com', 'user');

-- Sample cars
INSERT INTO cars (brand, model, year, price, color) VALUES
  ('Toyota',  'Camry',   2023, 25000.00, 'White'),
  ('Honda',   'Civic',   2023, 22000.00, 'Black'),
  ('Ford',    'Mustang', 2022, 45000.00, 'Red'),
  ('BMW',     'X5',      2023, 65000.00, 'Silver'),
  ('Hyundai', 'Elantra', 2023, 20000.00, 'Blue');
