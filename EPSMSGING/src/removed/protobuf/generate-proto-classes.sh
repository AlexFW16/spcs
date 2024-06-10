#!/bin/bash -x
set -x 
protoc -I=. --java_out=../../../src/main/java/ mymqttmessages.proto

cp -f "mymqttmessages.proto" "../python/at/jku/pervasive/eps/mymqttmessages/mymqttmessages.proto"
protoc -I="../python/at/jku/pervasive/eps/mymqttmessages/" --python_out="../python/at/jku/pervasive/eps/mymqttmessages/" "../python/at/jku/pervasive/eps/mymqttmessages/mymqttmessages.proto"
