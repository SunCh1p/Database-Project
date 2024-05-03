INSERT INTO product (product_ID, product_name, company_name, product_type, descr, price, quantity)
VALUES 
('P001', 'Laptop', 'XYZ Electronics', 'PC','15-inch laptop with SSD storage', 899.99, 50),
('P002', 'Smartphone', 'ABC Mobiles', 'Phone','5G smartphone with dual-camera setup', 699.99, 100),
('P003', 'Headphones', 'AudioTech', 'Audio','Noise-canceling wireless headphones', 149.99, 75),
('P004', 'Smartwatch', 'TechWear', 'Electronic, Watch','Fitness tracker with heart rate monitor', 199.99, 50);




-- Inserting data into the Compatibility table
INSERT INTO Compatibility (product_ID, product2_ID)
VALUES 
('P001', 'P003'),
('P002', 'P004'),
('P003', 'P001'),
('P004', 'P002');