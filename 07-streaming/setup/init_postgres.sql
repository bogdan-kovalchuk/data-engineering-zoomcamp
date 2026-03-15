CREATE TABLE IF NOT EXISTS q4_tumbling_pu (
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    pu_location_id INTEGER,
    num_trips BIGINT
);

CREATE TABLE IF NOT EXISTS q5_session_pu (
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    pu_location_id INTEGER,
    num_trips BIGINT
);

CREATE TABLE IF NOT EXISTS q6_tumbling_tip (
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    total_tip_amount DOUBLE PRECISION
);

