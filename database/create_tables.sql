create table rank(
    level int,
    starting_experience int,
    experience_next_level int not null unique,
    icon bytea,
    PRIMARY KEY (level)
);

insert into rank(level, starting_experience, experience_next_level, icon) VALUES (1, 0, 9, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (2, 10, 49, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (3, 50, 99, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (4, 100, 499, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (5, 500, 999, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (6, 1000, 1499, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (7, 1500, 1999, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (8, 2000, 9999, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (9, 10000, 99999, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (10, 100000, 0, null);

create table player(
    user_id bigint,
    chat_id bigint,
    level int,
    experience int,
    experience_next_level int,
    PRIMARY KEY (user_id, chat_id),
    FOREIGN KEY (level) REFERENCES rank(level),
    FOREIGN KEY (experience_next_level) REFERENCES rank(experience_next_level)
);