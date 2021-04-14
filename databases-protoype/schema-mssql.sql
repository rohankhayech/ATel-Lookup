create table reports (
    atel_num int NOT NULL,
    title varchar(255) NOT NULL,
	PRIMARY KEY (atel_num)
);

create table objects (
    obj_id int NOT NULL,
	coords int,
    aliases nvarchar,
    primary key (obj_id)
);

create table object_refs (
    obj_id int,
    atel_num int,
    primary key (obj_id, atel_num),
    foreign key (obj_id) references objects(obj_id),
    foreign key (atel_num) references reports(atel_num)
);

create table aliases (
	obj_id int not null,
    alias varchar(255),
    primary key (obj_id, alias),
    foreign key (obj_id) references objects(obj_id)
);