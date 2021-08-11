create table if not exists AdminUsers (
    username varchar(24) primary key,
    passwordHash varchar(255) not null
)