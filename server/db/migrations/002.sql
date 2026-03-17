start transaction ;

create table project_members (
    project_id int references projects(id) ,
    user_id int references users(id) ,
    primary key (
        project_id ,
        user_id
    )
) ;

end transaction ;