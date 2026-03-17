start transaction ;

create table project_members (
    project_id int not null ,
    user_id int not null ,
    primary key (
        project_id ,
        user_id
    )
) ;

end transaction ;