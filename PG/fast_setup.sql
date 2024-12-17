CREATE SCHEMA IF NOT EXISTS project;
SET search_path TO project;
CREATE EXTENSION pgcrypto;
drop table if exists Users cascade;
create table Users
(
	Login varchar(30) primary key not null unique,
	Name varchar(100) not null,
	FullName varchar(300) not null,
	PasswordHash varchar(100) not null,
	Role smallint not null check (Role > 0)
);

drop table if exists Products cascade;
create table Products
(
	ProductID uuid primary key not null unique,
	Name varchar(100) not null
);

drop table if exists Tickets cascade;
create table Tickets
(
	TicketID uuid not null unique,
	ProductID uuid references Products (ProductID) not null,
	AuthorLogin varchar(30) references Users (Login) not null,
	Status smallint not null check (Status > 0),
	constraint pk_tickets primary key (TicketID, ProductID)
);

drop table if exists Participants cascade;
create table Participants
(
	UserLogin varchar(30) references Users (Login) not null,
	TicketID uuid references Tickets(TicketID) not null,
	constraint pk_participants primary key (UserLogin, TicketID)
);

drop table if exists Messages cascade;
create table Messages
(
	AuthorLogin varchar(30) references Users (Login) not null,
	Date timestamp default now() not null,
	TicketID uuid references Tickets(TicketID) not null,
	Message text,
	constraint pk_messages primary key (AuthorLogin, Date, TicketID)
);

SET search_path TO  project;

create or replace function
    send_message(author varchar(30), ticket uuid, message text)
    returns timestamp as
    $$
    declare
        send_date timestamp;
    begin

        if EXISTS(SELECT 1 FROM users WHERE login=author) then
            send_date = now();
            insert into messages(authorlogin, ticketid, message, date)
            values (author, ticket, message, send_date);
            return send_date;
        end if;
    end;
    $$ language plpgsql
       SECURITY DEFINER SET search_path = project;



create or replace function
    create_ticket(ProdID uuid, AuthLogin varchar(30))
    returns uuid as
    $$
    declare
        id uuid;
    begin

        if EXISTS(SELECT 1 FROM users WHERE login=AuthLogin) then
            id := gen_random_uuid();
            insert into tickets(ticketid, ProductID, AuthorLogin, status)
            values (id, ProdID, AuthLogin, 1);
            return id;
        end if;
    end;
    $$ language plpgsql
       SECURITY DEFINER SET search_path = project;

create or replace function get_info_about_your_tickets(a_log varchar(30))
	returns table
        (
            TicketID uuid,
			ProductID uuid,
            AuthorLogin varchar(30),
			Status smallint
        )
	as
    $$
    begin
        if EXISTS(SELECT 1 FROM users WHERE login=a_log) then
            return query
					select tickets.TicketID,
						   tickets.ProductID,
						   tickets.authorlogin,
						   tickets.Status
					from tickets
					where tickets.authorLogin = a_log;
        else
            return;
        end if;
    end;
    $$ language plpgsql
       SECURITY DEFINER SET search_path = project;
SET search_path TO  project;

create role customer login;
grant all on schema project to customer;
grant all on all tables in schema project to customer;
grant all on all sequences in schema project to customer;
grant all on all functions in schema project to customer;

create role dev login;
grant all on schema project to dev;
grant all on all tables in schema project to dev;
grant all on all sequences in schema project to dev;
grant all on all functions in schema project to dev;

create role manager login;
grant all on schema project to manager;
grant all on all tables in schema project to manager;
grant all on all sequences in schema project to manager;
grant all on all functions in schema project to manager;

REVOKE ALL ON tickets FROM customer;
REVOKE ALL ON products FROM customer;
REVOKE ALL ON messages FROM customer;
REVOKE ALL ON participants FROM customer;
REVOKE ALL ON users FROM customer;

GRANT All privileges on tickets to manager;
GRANT All privileges on products to manager;
GRANT All privileges on messages to manager;
GRANT All privileges on participants to manager;
GRANT All privileges on users to manager;

GRANT All privileges on tickets to dev;
GRANT All privileges on products to dev;
GRANT All privileges on messages to dev;
GRANT All privileges on participants to dev;
GRANT All privileges on users to dev;

Grant EXECUTE on function get_info_about_your_tickets to customer;
Grant EXECUTE on function create_ticket to customer;
Grant EXECUTE  on function send_message to customer;

REVOKE TRUNCATE on All tables in schema project from dev;
REVOKE TRUNCATE on All tables in schema project from manager;



