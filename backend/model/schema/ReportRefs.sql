create table if not exists ReportRefs (
    atelNum int unsigned not null,
    refReport int unsigned not null,
    primary key (atelNum, refReport)
)