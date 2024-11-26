SET search_path TO project;

create or replace function CreateAuthorRow() returns trigger as
	$$
	begin
		insert into participants(UserLogin, TicketID)
		values (new.AuthorLogin, new.TicketID);
		insert into messages(authorlogin, ticketid, message)
		values (new.authorlogin, new.ticketid, concat('* ',new.authorlogin, ' Created a ticket'));
		return new;
	end;
	$$ LANGUAGE plpgsql;

drop trigger if exists TicketCheck on Tickets;
create trigger TicketCheck
    after insert on Tickets
	for each row
	execute function
	CreateAuthorRow();
