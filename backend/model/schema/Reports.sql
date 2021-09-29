create table if not exists Reports (
    atelNum int unsigned primary key,
    title varchar(1024) not null,
    authors varchar(1024) not null,
    body varchar(5120) not null,
    submissionDate timestamp not null,
    keywords set('{}') not null default ''
)