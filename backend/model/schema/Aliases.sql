create table if not exists Aliases (
    alias varchar(255) primary key,
    objectIDFK varchar(255) not null,
    foreign key (objectIDFK) references Objects(objectID) on update cascade on delete cascade
)