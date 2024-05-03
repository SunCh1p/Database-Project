INSERT INTO product (product_ID, product_name, company_name, descr, price, quantity)
VALUES 
('P001', 'Laptop', 'XYZ Electronics', '15-inch laptop with SSD storage', 899.99, 50),
('P002', 'Smartphone', 'ABC Mobiles', '5G smartphone with dual-camera setup', 699.99, 100),
('P003', 'Headphones', 'AudioTech', 'Noise-canceling wireless headphones', 149.99, 75),
('P004', 'Smartwatch', 'TechWear', 'Fitness tracker with heart rate monitor', 199.99, 50);




-- Inserting data into the Compatibility table
INSERT INTO Compatibility (product_ID, product2_ID)
VALUES 
('P001', 'P003'),
('P002', 'P004'),
('P003', 'P001'),
('P004', 'P002');