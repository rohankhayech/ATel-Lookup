create table if not exists AdminUsers (
    username varchar(24) primary key,
    passwordHash varchar not null
)