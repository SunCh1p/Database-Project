


CREATE TABLE IF NOT EXISTS `accounts` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

create table if not exists product(
    product_ID varchar(25),
    product_name varchar(100),
    company_name varchar(50),
    descr varchar(100),
    price decimal(10,2),
    quantity int(11),
    compatibility varchar(25),
    primary key(product_ID)
);

create table if not exists customer(
    customer_ID varchar(25),
    FirstName varchar(50),
    LastName varchar(50),
    email varchar(50),
    street_number int(11),
    street_name varchar(1000),
    apt_num int(11),
    city varchar(1000),
    zip_code int(5),
    primary key(customer_ID)
);

create table if not exists payment(
    payment_ID varchar(25),
    customer_ID varchar(25),
    card_number numeric(16,0),
    card_name   varchar(25),
    expiration_date varchar(5),
    security_code int(3),
    primary key(payment_ID),
    foreign key(customer_ID) references customer(customer_ID) on delete set null
);

create table if not exists orders(
    orders_ID varchar(25),
    customer_ID varchar(25),
    product_ID varchar(25),
    quantity int(11),
    primary key(orders_ID),
    foreign key(product_ID) references product(product_ID) on delete set null,
    foreign key(customer_ID) references payment(customer_ID) on delete set null
);

create table if not exists transaction_history(
    payment_ID varchar(25),
    product_ID varchar(25),
    transaction_ID varchar(25),
    primary key(transaction_ID),
    foreign key(payment_ID) references payment(payment_ID) on delete set null,
    foreign key(product_ID) references product(product_ID) on delete set null
);

create table if not exists Compatibility(
	product_ID varchar(25), 
	Compatibility_product_ID varchar(25), 
	primary key(product_ID)
);