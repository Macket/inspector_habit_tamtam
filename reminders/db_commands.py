DROP_REMINDERS_TABLE = """
       DROP TABLE reminders;
"""

CREATE_REMINDERS_TABLE = """
       CREATE TABLE reminders (
       id BIGSERIAL PRIMARY KEY,
       user_id BIGINT,
       mid VARCHAR(63),
       datetime_native TIMESTAMP,
       datetime_utc TIMESTAMP,
       FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
       )
       """
