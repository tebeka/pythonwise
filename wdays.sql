-- Convert Python's datetime.weekday() to names
-- Run with "psql -U <user> <database> -1 -f wdays.sql"

CREATE TABLE weekdays (
    num TEXT
  , weekday TEXT
);
CREATE INDEX weekdays_num ON weekdays(num);

INSERT INTO weekdays
    (num, weekday)
VALUES
    ('0', 'Monday')
  , ('1', 'Tuesday')
  , ('2', 'Wednesday')
  , ('3', 'Thursday')
  , ('4', 'Friday')
  , ('5', 'Saturday')
  , ('6', 'Sunday')
;

UPDATE facts 
SET day = weekdays.weekday
FROM weekdays
WHERE day = weekdays.num
;

DROP TABLE weekdays CASCADE;
