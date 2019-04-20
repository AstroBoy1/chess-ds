DROP TABLE IF EXISTS fact_table;
CREATE TABLE fact_table(user_id INT NOT NULL, event_id INT NOT NULL, reg_before TEXT, reg_after TEXT, section TEXT, FOREIGN KEY (user_id) REFERENCES users(uid), FOREIGN KEY (event_id) REFERENCES events_dim(event_id));
INSERT INTO fact_table SELECT user_id, event_id, reg_before, reg_after, section FROM user_events;