create table if not exists Metadata (
    metadata enum('metadata') primary key,
    lastUpdatedDate timestamp not null default now(),
    nextATelnum int not null default 1
)