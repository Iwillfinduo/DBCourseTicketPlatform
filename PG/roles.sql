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
grant SELECT on products to customer;
grant select on messages to customer;
grant select on users to customer;
grant select on participants to customer;
grant select on tickets to customer;

REVOKE TRUNCATE on All tables in schema project from dev;
REVOKE TRUNCATE on All tables in schema project from manager;


