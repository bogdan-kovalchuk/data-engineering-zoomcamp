from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment


def main() -> None:
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    t_env.execute_sql(
        """
        CREATE TABLE green_trips (
            lpep_pickup_datetime VARCHAR,
            lpep_dropoff_datetime VARCHAR,
            PULocationID INT,
            DOLocationID INT,
            passenger_count DOUBLE,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            total_amount DOUBLE,
            event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'green-trips',
            'properties.bootstrap.servers' = 'redpanda:9092',
            'properties.group.id' = 'flink-q4',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        )
        """
    )

    t_env.execute_sql(
        """
        CREATE TABLE q4_tumbling_pu (
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            pu_location_id INT,
            num_trips BIGINT
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'q4_tumbling_pu',
            'driver' = 'org.postgresql.Driver',
            'username' = 'postgres',
            'password' = 'postgres'
        )
        """
    )

    stmt = t_env.execute_sql(
        """
        INSERT INTO q4_tumbling_pu
        SELECT window_start, window_end, PULocationID, COUNT(*) AS num_trips
        FROM TABLE(
            TUMBLE(TABLE green_trips, DESCRIPTOR(event_timestamp), INTERVAL '5' MINUTES)
        )
        GROUP BY window_start, window_end, PULocationID
        """
    )
    stmt.wait()


if __name__ == "__main__":
    main()

