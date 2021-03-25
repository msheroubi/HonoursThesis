DROP TABLE Group_to_Interest;
DROP TABLE Event_to_Interest;
DROP TABLE Interest_to_Interest;
DROP TABLE User_to_Interest;
DROP TABLE leavesComment;
DROP TABLE sendsMessage;
DROP TABLE isFriendsWith;
DROP TABLE isAttending;
DROP TABLE isMember;
DROP TABLE Posts;
DROP TABLE Events;
DROP TABLE Interests;
DROP TABLE Groups;
DROP TABLE Users;


CREATE TABLE Users(
    user_id int NOT NULL PRIMARY KEY, 
    user_name VARCHAR(20) NOT NULL,
	name VARCHAR(100) NOT NULL,
    address VARCHAR(100),
    city VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    is_admin BIT DEFAULT 0,
);

CREATE TABLE Groups(
	group_id int NOT NULL PRIMARY KEY, 
	user_id	int NOT NULL, 		
	group_name VARCHAR(100) NOT NULL,
	description VARCHAR(500),
	created_at DATETIME,
	CONSTRAINT FK_Group_User FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Interests(
	interest_id int NOT NULL PRIMARY KEY,
	interest_name VARCHAR(100) NOT NULL,
	category VARCHAR(20)
);

CREATE TABLE Events(
	event_id int NOT NULL PRIMARY KEY,
	user_id int,
	group_id int,		
	event_name VARCHAR(100) NOT NULL,
	description VARCHAR(500),
	created_at DATETIME,
	event_start DATETIME,
	event_end DATETIME,
	address VARCHAR(100),
	city VARCHAR(20),
	CONSTRAINT FK_Event_User FOREIGN KEY (user_id) REFERENCES Users(user_id),
	CONSTRAINT FK_Event_Group FOREIGN KEY (group_id) REFERENCES Groups(group_id)
);

CREATE TABLE Posts(
	post_id int NOT NULL PRIMARY KEY,
	user_id int NOT NULL,
	event_id int,
	group_id int,		
	content VARCHAR(500),
	created_at DATETIME,
	CONSTRAINT FK_Post_User FOREIGN KEY (user_id) REFERENCES Users(user_id),
	CONSTRAINT FK_Post_Event FOREIGN KEY (event_id) REFERENCES Events(event_id),
	CONSTRAINT FK_Post_Group FOREIGN KEY (group_id) REFERENCES Groups(group_id)
);

/* RELATIONSHIPS */
CREATE TABLE isMember(
	user_id int NOT NULL,
	group_id int NOT NULL,
	member_since DATETIME,
	is_admin BIT DEFAULT 0,
	PRIMARY KEY (user_id, group_id),
	CONSTRAINT FK_isMember_User FOREIGN KEY (user_id) REFERENCES Users(user_id),
	CONSTRAINT FK_isMember_Group FOREIGN KEY (group_id) REFERENCES Groups(group_id)
);

CREATE TABLE isAttending(
	user_id int NOT NULL,
	event_id int NOT NULL,
	PRIMARY KEY (user_id, event_id),
	CONSTRAINT FK_isAttending_User FOREIGN KEY (user_id) REFERENCES Users(user_id),
	CONSTRAINT FK_isAttending_Event FOREIGN KEY (event_id) REFERENCES Events(event_id)
);

CREATE TABLE sendsMessage(
	message_id int NOT NULL PRIMARY KEY,
	sender_id int NOT NULL,
	recipient_id int NOT NULL,
	content VARCHAR(300),
	CONSTRAINT FK_sendsMessage_User FOREIGN KEY (sender_id) REFERENCES Users(user_id),
	CONSTRAINT FK2_sendsMessage_User FOREIGN KEY (recipient_id) REFERENCES Users(user_id)
);

CREATE TABLE isFriendsWith(
	user_id int NOT NULL,
	friend_id int NOT NULL,
	created_at DATETIME,
	PRIMARY KEY (user_id, friend_id),
	CONSTRAINT FK_isFriendsWith_User FOREIGN KEY (user_id) REFERENCES Users(user_id),
	CONSTRAINT FK2_isFriendsWith_User FOREIGN KEY (friend_id) REFERENCES Users(user_id)
);

CREATE TABLE leavesComment(
	comment_id int NOT NULL,
	post_id int NOT NULL,
	user_id	int NOT NULL,
	content VARCHAR(500),
	created_at DATETIME,
	PRIMARY KEY (comment_id, post_id),
	CONSTRAINT FK_leavesComment_User FOREIGN KEY (user_id) REFERENCES Users(user_id),
	CONSTRAINT FK_leavesComment_Post FOREIGN KEY (post_id) REFERENCES Posts(post_id)
);

CREATE TABLE User_to_Interest(
	user_id int NOT NULL,
	interest_id int NOT NULL,
	created_at DATETIME,
	PRIMARY KEY (user_id, interest_id),
	CONSTRAINT FK_UserToInterest_User FOREIGN KEY (user_id) REFERENCES Users(user_id),
	CONSTRAINT FK_UserToInterest_Interest FOREIGN KEY (interest_id) REFERENCES Interests(interest_id)
);

CREATE TABLE Event_to_Interest(
	event_id int NOT NULL,
	interest_id int NOT NULL,
	PRIMARY KEY (event_id, interest_id),
	CONSTRAINT FK_EventToInterest_Event FOREIGN KEY (event_id) REFERENCES Events(event_id),
	CONSTRAINT FK_EventToInterest_Interest FOREIGN KEY (interest_id) REFERENCES Interests(interest_id)
);

CREATE TABLE Interest_to_Interest(
	interest_id int NOT NULL,
	related_interest_id int NOT NULL,
	degree int,
	PRIMARY KEY (interest_id, related_interest_id),
	CONSTRAINT FK_InterestToInterest_Interest FOREIGN KEY (interest_id) REFERENCES Interests(interest_id),
	CONSTRAINT FK2_InterestToInterest_Interest FOREIGN KEY (related_interest_id) REFERENCES Interests(interest_id)
);

CREATE TABLE Group_to_Interest(
	group_id int NOT NULL,
	interest_id int NOT NULL,
	PRIMARY KEY (group_id, interest_id),
	CONSTRAINT FK_GroupToInterest_Group FOREIGN KEY (group_id) REFERENCES Groups(group_id),
	CONSTRAINT FK_GroupToInterest_Interest FOREIGN KEY (interest_id) REFERENCES Interests(interest_id)
);