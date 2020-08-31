create table rank(
    level int,
    starting_experience int,
    experience_next_level int not null unique,
    icon bytea,
    PRIMARY KEY (level)
);

insert into rank(level, starting_experience, experience_next_level, icon) VALUES (1, 0, 9, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (2, 10, 19, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (3, 20, 39, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (4, 40, 79, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (5, 80, 159, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (6, 160, 319, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (7, 320, 639, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (8, 640, 1279, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (9, 1280, 2559, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (10, 2560, 5119, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (11, 5120, 10239, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (12, 10240, 20479, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (13, 20480, 30719, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (14, 30720, 46079, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (15, 46080, 69119, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (16, 69120, 103679, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (17, 103680, 129599, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (18, 129600, 161999, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (19, 162000, 199999, null);
insert into rank(level, starting_experience, experience_next_level, icon) VALUES (20, 200000, 0, null);

create table player(
    user_id bigint,
    chat_id bigint,
    level int,
    experience int,
    experience_next_level int,
    PRIMARY KEY (user_id, chat_id),
    FOREIGN KEY (level) REFERENCES rank(level),
    FOREIGN KEY (experience_next_level) REFERENCES rank(experience_next_level),
    FOREIGN KEY (chat_id) REFERENCES chat(chat_id)
);

create table chat(
    chat_id bigint,
    silence boolean,
    PRIMARY KEY (chat_id)
);