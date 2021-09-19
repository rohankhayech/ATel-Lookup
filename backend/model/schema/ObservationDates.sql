create table if not exists ObservationDates (
    atelNumFK int unsigned not null,
    obDate timestamp not null,
    foreign key (atelNumFK) references Reports(atelNum) on update cascade on delete cascade,
    primary key (atelNumFK, obDate),
)