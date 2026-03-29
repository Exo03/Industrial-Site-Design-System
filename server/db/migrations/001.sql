start transaction ;

create table users (
    id serial not null primary key ,
    email varchar(64) not null unique ,
    username varchar(64) not null unique ,
    hashed_password varchar(128) not null 
) ;

create table projects (
    id serial not null primary key ,
    name varchar(64) not null ,
    description varchar(64) ,
    length int not null ,
    width int not null ,
    owner_id int references users(id) 
) ;

create table element_types (
    id serial not null primary key ,
    length int not null ,
    width int not null ,
    zone_width int not null,
    zone_length int not null,
    title varchar(64) not null ,
    description varchar(64) ,
    type_category int
) ;

create table elements (
    id serial not null primary key ,
    x int not null ,
    y int not null ,
    title varchar(64) ,
    color varchar(8) ,
    project_id int references projects(id) ,
    element_type_id int references element_types(id)
) ;

commit transaction ; 