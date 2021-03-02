#!/bin/bash
echo
echo "~*~initiating transfer to raspberry pi~*~"
echo
echo sending the following tweets ids:
echo
cat tacoma.txt
TWEETNUM=$(cat tacoma.txt | wc -w)
echo
TRIMTWEET=`echo $TWEETNUM | sed 's/ *$//g'`
echo
echo number of tweets being sent: $TRIMTWEET
echo
scp tacoma.txt pi@10.0.0.99:/home/pi/dissertation/tacoma
