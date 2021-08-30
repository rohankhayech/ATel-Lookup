create table Aliases (
    alias varchar(255) primary key,
    objectIDFK varchar not null,
    foreign key objectIDFK references Objects(objectID)
)