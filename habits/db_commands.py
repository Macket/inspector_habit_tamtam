DROP_HABITS_TABLE = """
       DROP TABLE habits;
"""

CREATE_HABITS_TABLE = """
       CREATE TABLE habits (
       id BIGSERIAL PRIMARY KEY,
       user_id BIGINT,
       label VARCHAR(255),
       question VARCHAR(255),
       days_of_week VARCHAR(15),
       time_array VARCHAR(255),
       FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
       )
       """
