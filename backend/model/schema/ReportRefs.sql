create table if not exists ReportRefs (
    atelNumFK int unsigned not null,
    refReportFK int unsigned not null,
    foreign key (atelNumFK) references Reports(atelNum) on update cascade on delete cascade,
    foreign key (refReportFK) references Reports(atelNum) on update cascade on delete cascade,
    primary key (atelNumFK, refReportFK)
)