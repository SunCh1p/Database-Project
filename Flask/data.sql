INSERT INTO product (product_ID, product_name, company_name, descr, price, quantity, compatibility)
VALUES 
('P001', 'Laptop', 'XYZ Electronics', '15-inch laptop with SSD storage', 899.99, 50, 'Windows, Mac OS'),
('P002', 'Smartphone', 'ABC Mobiles', '5G smartphone with dual-camera setup', 699.99, 100, 'Android, iOS'),
('P003', 'Headphones', 'AudioTech', 'Noise-canceling wireless headphones', 149.99, 75, 'Bluetooth devices'),
('P004', 'Smartwatch', 'TechWear', 'Fitness tracker with heart rate monitor', 199.99, 50, 'Android, iOS');

-- Inserting data into the customer table
INSERT INTO customer (customer_ID, FirstName, LastName, email, street_number, street_name, apt_num, city, zip_Code)
VALUES 
('C001', 'John', 'Doe', 'john.doe@example.com', 123, 'Main Street', 101, 'Cityville', 12345),
('C002', 'Jane', 'Smith', 'jane.smith@example.com', 456, 'Oak Avenue', 202, 'Townsville', 54321),
('C003', 'Michael', 'Johnson', 'michael.johnson@example.com', 789, 'Elm Street', NULL, 'Villageton', 98765);

-- Inserting data into the payment table
INSERT INTO payment (payment_ID, customer_ID, card_number, card_name, expiration_date, security_code)
VALUES 
('PAY001', 'C001', 1234567890123456, 'John Doe', '12/26', 123),
('PAY002', 'C002', 9876543210987654, 'Jane Smith', '08/25', 456),
('PAY003', 'C003', 5678901234567890, 'Michael Johnson', '03/24', 789);

-- Inserting data into the order table
INSERT INTO orders (orders_ID, customer_ID, product_ID, quantity)
VALUES 
('ORD001', 'C001', 'P001', 2),
('ORD002', 'C002', 'P002', 1),
('ORD003', 'C003', 'P003', 3),
('ORD004', 'C001', 'P004', 1),
('ORD005', 'C002', 'P001', 1);

-- Inserting data into the transaction_history table
INSERT INTO transaction_history (payment_ID, product_ID, transaction_ID)
VALUES 
('PAY001', 'P001', 'TRX001'),
('PAY002', 'P002', 'TRX002'),
('PAY003', 'P003', 'TRX003'),
('PAY001', 'P004', 'TRX004'),
('PAY002', 'P001', 'TRX005');

-- Inserting data into the Compatibility table
INSERT INTO Compatibility (product_ID, Compatibility_product_ID)
VALUES 
('P001', 'P003'),
('P002', 'P004'),
('P003', 'P001'),
('P004', 'P002');