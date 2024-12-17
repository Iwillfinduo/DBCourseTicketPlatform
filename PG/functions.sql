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