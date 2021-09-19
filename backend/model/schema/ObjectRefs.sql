create table if not exists ObjectRefs (
    atelNumFK int unsigned not null,
    objectIDFK varchar(255) not null,
    foreign key (atelNumFK) references Reports(atelNum) on update cascade on delete cascade,
    foreign key (objectIDFK) references Objects(objectID) on update cascade on delete cascade,
    primary key (atelNumFK, objectIDFK)
)