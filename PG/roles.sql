SET search_path TO  project;

create role customer login;
create role dev login;
create role manager login;

REVOKE ALL ON tickets FROM customer;
REVOKE ALL ON products FROM customer;
REVOKE ALL ON messages FROM customer;
REVOKE ALL ON participants FROM customer;
REVOKE ALL ON users FROM customer;

Grant EXECUTE on function get_info_about_your_tickets to customer;
Grant EXECUTE on function create_ticket to customer;
Grant EXECUTE  on function send_message to customer;

REVOKE TRUNCATE, DROP on All tables in schema project from dev;
REVOKE TRUNCATE, DROP on All tables in schema project from manager;


