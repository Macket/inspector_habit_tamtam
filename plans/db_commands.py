DROP_PLANS_TABLE = """
       DROP TABLE plans;
"""

CREATE_PLANS_TABLE = """
       CREATE TABLE plans (
       id BIGSERIAL PRIMARY KEY,
       user_id BIGINT,
       plan_array VARCHAR(4095),
       status_array VARCHAR(1023),
       date DATE,
       FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
       )
       """
