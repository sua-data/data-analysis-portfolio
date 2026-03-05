create database ecommerce;
use ecommerce;
create table orders(
	order_id int,
	order_date date,
	product_name varchar(100),
	price int,
	quantity int
);

insert into orders values
(1,'2026-01-05','Dog Shampoo',12000,1),
(2,'2026-01-10','Dog Snack',5000,2),
(3,'2026-02-01','Dog Leash',15000,1),
(4,'2026-02-10','Dog Snack',5000,3),
(5,'2026-03-03','Dog Toy',7000,1);

select * from orders;
delete from orders;

insert into orders values
(1,'2026-01-05','Dog Shampoo',12000,1),
(2,'2026-01-10','Dog Snack',5000,2),
(3,'2026-02-01','Dog Leash',15000,1),
(4,'2026-02-10','Dog Snack',5000,3),
(5,'2026-03-03','Dog Toy',7000,1);