CREATE TABLE votes (
	post_id INT NOT NULL,
	user_id INT NOT NULL,
	FOREIGN KEY (post_id)
    	REFERENCES posts (id),
	FOREIGN KEY (user_id)
    	REFERENCES users (id)
);


insert into votes (post_id, user_id) 
values(1, 1)
	,(1, 2);

--select * from votes;