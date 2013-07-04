#!/bin/sh
i="0"
while [ $i -lt 40 ]
do
./hb_client.bin 10.20.1.128 44444 &
echo "test" $i
i = $[$i+1]
done&
