CREATE TABLE posts (
	id serial PRIMARY KEY,
	title VARCHAR ( 1000 ) NOT NULL,
	content VARCHAR ( 1000 ) NOT NULL,
	rating INT,
	published BOOLEAN NOT NULL default True,
	created_at TIMESTAMP NOT NULL default current_timestamp,
	owner_id INT NOT NULL,
	FOREIGN KEY (owner_id)
    	REFERENCES users (id)
);

insert into posts (title, content, rating, owner_id) 
values('title post 1', 'content post 1', 2, 1)
	,('title post 2', 'content post 2', 3, 2);

--select * from posts;