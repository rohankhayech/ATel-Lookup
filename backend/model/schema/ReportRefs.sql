create table if not exists ReportRefs (
    atelNum int unsigned not null,
    refReportFK int unsigned not null,
    foreign key (refReportFK) references Reports(atelNum) on update cascade on delete cascade,
    primary key (atelNumFK, refReportFK)
)