CREATE SCHEMA IF NOT EXISTS project;
SET search_path TO project;

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