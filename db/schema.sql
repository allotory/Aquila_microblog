drop table if exists user;
create table user (
	id integer primary key autoincrement,
	username varchar(64) not null,
	password varchar(100) not null,
	email varchar(120) not null,
	role integer not null
);

drop table if exists post;
create table post (
	id integer primary key autoincrement,
	content varchar(140) not null,
	timestamp varchar(50) not null,
	user_id integer not null,
	foreign key(user_id) references user(id)
);