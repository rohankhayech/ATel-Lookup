create table if not exists Reports (
    atelNum int unsigned primary key,
    title varchar(2056) not null,
    authors varchar(2056) not null,
    body varchar(5120) not null,
    submissionDate timestamp not null,
    keywords set('{}') not null default ''
)