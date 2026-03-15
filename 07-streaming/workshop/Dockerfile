FROM flink:1.19.1-scala_2.12-java11

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir apache-flink==1.19.1 kafka-python==2.0.2

RUN wget -q -O /opt/flink/lib/flink-sql-connector-kafka-3.2.0-1.19.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.2.0-1.19/flink-sql-connector-kafka-3.2.0-1.19.jar \
    && wget -q -O /opt/flink/lib/flink-connector-jdbc-3.2.0-1.19.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.2.0-1.19/flink-connector-jdbc-3.2.0-1.19.jar \
    && wget -q -O /opt/flink/lib/postgresql-42.7.3.jar \
    https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/postgresql-42.7.3.jar

