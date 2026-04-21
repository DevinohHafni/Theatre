-- Theater Management System Database Schema
-- Run this file to initialize the database

CREATE DATABASE IF NOT EXISTS theater_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE theater_db;

-- Theaters / Halls
CREATE TABLE IF NOT EXISTS theaters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    total_seats INT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Movies
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    genre VARCHAR(50),
    duration_minutes INT NOT NULL,
    language VARCHAR(50) DEFAULT 'English',
    rating VARCHAR(10),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Shows (a movie playing in a theater at a specific time)
CREATE TABLE IF NOT EXISTS shows (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    theater_id INT NOT NULL,
    show_date DATE NOT NULL,
    show_time TIME NOT NULL,
    ticket_price DECIMAL(10,2) NOT NULL,
    available_seats INT NOT NULL,
    status ENUM('active', 'cancelled', 'completed') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (theater_id) REFERENCES theaters(id) ON DELETE CASCADE
);

-- Customers
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bookings
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    show_id INT NOT NULL,
    customer_id INT NOT NULL,
    num_seats INT NOT NULL DEFAULT 1,
    total_amount DECIMAL(10,2) NOT NULL,
    booking_status ENUM('confirmed', 'cancelled') DEFAULT 'confirmed',
    booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (show_id) REFERENCES shows(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Seed Data
INSERT INTO theaters (name, total_seats, description) VALUES
('Grand Hall', 200, 'Main screening hall with premium seating'),
('Studio 2', 100, 'Intimate screening room for art films'),
('IMAX Screen', 300, 'Large format immersive experience');

INSERT INTO movies (title, genre, duration_minutes, language, rating, description) VALUES
('Inception', 'Sci-Fi', 148, 'English', 'PG-13', 'A thief who steals corporate secrets through dream-sharing technology.'),
('The Dark Knight', 'Action', 152, 'English', 'PG-13', 'Batman faces the Joker, a criminal mastermind who wants to create anarchy in Gotham.'),
('Parasite', 'Thriller', 132, 'Korean', 'R', 'A poor family schemes to become employed by a wealthy family.'),
('Interstellar', 'Sci-Fi', 169, 'English', 'PG-13', 'A team of explorers travel through a wormhole in space.'),
('The Godfather', 'Drama', 175, 'English', 'R', 'The aging patriarch of an organized crime dynasty transfers control to his son.');

INSERT INTO customers (name, email, phone) VALUES
('Alice Johnson', 'alice@example.com', '9876543210'),
('Bob Smith', 'bob@example.com', '9123456789'),
('Carol White', 'carol@example.com', '9000012345');

INSERT INTO shows (movie_id, theater_id, show_date, show_time, ticket_price, available_seats) VALUES
(1, 1, CURDATE(), '10:00:00', 250.00, 200),
(2, 2, CURDATE(), '13:00:00', 200.00, 100),
(3, 3, CURDATE(), '16:00:00', 350.00, 300),
(4, 1, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '11:00:00', 300.00, 200),
(5, 2, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '18:30:00', 220.00, 100);
