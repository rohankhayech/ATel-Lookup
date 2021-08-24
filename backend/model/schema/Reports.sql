create table if not exists Reports (
    atelNum int unsigned primary key,
    title varchar(255) not null,
    authors varchar(255) not null,
    body varchar(4000) not null,
    submissionDate timestamp not null,
    keywords set('{}') not null default ''
)