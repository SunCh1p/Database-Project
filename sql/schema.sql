CREATE TABLE IF NOT EXISTS `accounts` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

create table customer(
    customer_ID int(11),
    FirstName varchar(50),
    LastName varchar(50),
    email varchar(50),
    street_number int(11),
    street_name varchar(1000),
    apt_num int(11),
    city varchar(1000),
    zip_code int(5),
    primary key(customer_ID),
    foreign key(customer_ID) references accounts(id)
);

DELIMITER //
CREATE TRIGGER insert_customer_account
AFTER INSERT ON accounts
FOR EACH ROW
BEGIN
    INSERT INTO customer(customer_ID, FirstName, LastName, email)
    VALUES (NEW.id, '', '', NEW.email);
END;
//
DELIMITER ;

create table product(
    product_ID varchar(25),
    product_name varchar(100),
    company_name varchar(50),
    descr varchar(100),
    price decimal(10,2),
    quantity int(11),
    primary key(product_ID)
);

create table payment(
    customer_ID int(11),
    card_number numeric(16,0),
    expiration_date varchar(5),
    security_code int(3),
    primary key(card_number),
    foreign key(customer_ID) references customer(customer_ID) on delete set null
);

create table orders(
    orders_ID varchar(25),
    customer_ID int(11),
    product_ID varchar(25),
    card_number numeric(16,0),
    quantity int(11),
    primary key(orders_ID),
    foreign key(payment_ID) references payment(card_number) on delete set null,
    foreign key(product_ID) references product(product_ID) on delete set null,
    foreign key(customer_ID) references payment(customer_ID) on delete set null
);

CREATE TABLE Compatibility (
    product_ID varchar(25),
    product2_ID varchar(25),
    primary key (product_ID, product2_ID),
    foreign key (product_ID) references product(product_ID) on delete cascade,
    foreign key (product2_ID) references product(product_ID) on delete cascade
);

CREATE TABLE IF NOT EXISTS cart (
    customer_ID int(11),
    product_ID varchar(25),
    quantity int(11),
    PRIMARY KEY (customer_ID, product_ID),
    FOREIGN KEY (customer_ID) REFERENCES customer(customer_ID),
    FOREIGN KEY (product_ID) REFERENCES product(product_ID)
);