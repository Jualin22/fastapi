CREATE TABLE users (
	id serial PRIMARY KEY,
	mail VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 1000 ) NOT NULL,
	created_at TIMESTAMP NOT NULL default current_timestamp
);

insert into users (mail, password) 
values('Test.User1@gmail.com', '$2b$12$pXUVxuvw20HPbeqCZ5o0SOMoN8OV5C2x.X9mjRlxGOra.vacwl5Pu')
	,('Test.User2@gmail.com', '$2b$12$znyqBUW2rYhXPBxXIkSw4OcFSzx.w6kuugh3QzDKx.bLwH4HM00Qq');
	
--select * from users;