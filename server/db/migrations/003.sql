start transaction ;

insert into users (id, email, username, hashed_password) values (-1, '-', 'system', '-') ;

commit transaction ;