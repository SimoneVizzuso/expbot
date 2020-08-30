create table rank(
    level int,
    starting_experience int,
    experience_next_level int,
    icon bytea,
    PRIMARY KEY (level)
);

create table player(
    user_id int,
    username varchar(255),
    group_id int,
    level int,
    experience int,
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (level) REFERENCES rank(level)
);