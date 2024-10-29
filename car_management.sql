CREATE DATABASE car_management;
USE car_management;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50)
);

CREATE TABLE cars (
    model_name VARCHAR(50),
    brand VARCHAR(50),
    price_per_day FLOAT
);
select*from cars;
