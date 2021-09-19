create table if not exists ReportCoords (
    atelNumFK int unsigned not null,
    ra decimal(13,10) not null,
    declination decimal(13,10) not null,
    foreign key (atelNumFK) references Reports(atelNum) on update cascade on delete cascade,
    primary key (atelNumFK, ra, declination)
)