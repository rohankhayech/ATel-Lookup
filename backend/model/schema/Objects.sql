create table if not exists Objects (
    objectID varchar(255) primary key,
    ra decimal(13,10) not null,
    declination decimal(13,10) not null,
    lastUpdated timestamp not null default now()
)