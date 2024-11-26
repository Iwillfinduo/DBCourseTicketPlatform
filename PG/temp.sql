truncate table Users cascade;

insert into Users(Login, name, fullname, passwordhash, role)
values ('a', 'aa', 'aaa', '43', '1'),
	   ('b','bb','bbb','44','1');

SET search_path TO  project;

CREATE EXTENSION pgcrypto;

insert into Products(ProductCipher, Name)
values ('\000'::bytea, '0');

insert into Tickets(TicketID, ProductCipher, AuthorLogin, status)
values(gen_random_uuid(), '\000'::bytea, 'a', 1);

select send_message('a', '55132f65-a3ee-4425-a06e-6f399b2941a3','text');

create role customer login;
create role dev login;
create role manager login;

SET search_path TO  project;


REVOKE ALL ON tickets FROM customer;
REVOKE ALL ON products FROM customer;
REVOKE ALL ON messages FROM customer;
REVOKE ALL ON participants FROM customer;
REVOKE ALL ON users FROM customer;

Grant EXECUTE on function get_info_about_your_tickets to customer;
Grant EXECUTE on function create_ticket to customer;
Grant EXECUTE  on function send_message to customer;

REVOKE TRUNCATE, TRIGGER, TRIGGER on All tables in schema project from dev,manager
