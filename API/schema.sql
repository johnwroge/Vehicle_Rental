-- Create Vehicle Rental Database
CREATE DATABASE IF NOT EXISTS vehicle_rental;
USE vehicle_rental;

-- Users Table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_email CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Categories Table
CREATE TABLE VehicleCategories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    capacity INT NOT NULL,
    daily_rate DECIMAL(10,2) NOT NULL,
    description TEXT,
    CONSTRAINT chk_capacity CHECK (capacity > 0),
    CONSTRAINT chk_daily_rate CHECK (daily_rate > 0)
);

-- Vehicles Table
CREATE TABLE Vehicles (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    registration_number VARCHAR(20) NOT NULL UNIQUE,
    model VARCHAR(100) NOT NULL,
    make VARCHAR(100) NOT NULL,
    year YEAR NOT NULL,
    status ENUM('available', 'rented', 'maintenance') DEFAULT 'available',
    last_maintenance DATETIME,
    FOREIGN KEY (category_id) REFERENCES VehicleCategories(category_id)
);

-- Bookings Table
CREATE TABLE Bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    pickup_date DATETIME NOT NULL,
    return_date DATETIME NOT NULL,
    total_cost DECIMAL(10,2) NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,
    status ENUM('pending', 'active', 'completed', 'cancelled') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
);

-- Invoices Table
CREATE TABLE Invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL UNIQUE,
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    payment_status ENUM('paid', 'pending', 'failed') DEFAULT 'pending',
    invoice_number VARCHAR(50) NOT NULL UNIQUE,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id)
);

-- Email Logs Table
CREATE TABLE EmailLogs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    email_type ENUM('confirmation', 'invoice', 'cancelled') NOT NULL,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('sent', 'failed') NOT NULL DEFAULT 'sent',
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id)
);

-- Indices for Optimization
CREATE INDEX idx_vehicle_status ON Vehicles(status);
CREATE INDEX idx_booking_dates ON Bookings(pickup_date, return_date);
CREATE INDEX idx_booking_status ON Bookings(status);
CREATE INDEX idx_email_type ON EmailLogs(email_type);

-- Default Vehicle Categories
INSERT INTO VehicleCategories (name, capacity, daily_rate, description) VALUES
('Small Car', 4, 50.00, 'Compact car suitable for up to 4 people'),
('SUV', 7, 80.00, 'Large SUV suitable for up to 7 people'),
('Van', 2, 100.00, 'Cargo van for moving goods');
