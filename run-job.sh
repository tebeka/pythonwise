#!/bin/bash

jars=avro-1.6.0-SNAPSHOT.jar,avro-mapred-1.6.0-SNAPSHOT.jar

hadoop jar hadoop-streaming-0.20.2-cdh3u0.jar \
    -files $jars \
    -libjars $jars \
    -input /in/avro \
    -output /out/avro \
    -mapper avro-mapper.py \
    -reducer avro-reducer.py \
    -file avro-mapper.py \
    -file avro-reducer.py \
    -inputformat org.apache.avro.mapred.AvroAsTextInputFormat
