#!/bin/bash

COUNTER=0
for i in 10 15 20 
do
    for holding_period in 1 5 10 20 50 100 250
    do
       for trigger in -1.5 -1.3 -1.0 0 1.0 1.3 1.5 
       do
       for market in -1.5 -1 0 1 1.5
           do
           for bin in -1 1
           do 
             for switch in -1 1
             do
    echo "lookback period is" $i >> test15.txt   
    echo "holding period is" $holding_period >> test15.txt 
    echo "trigger is" $trigger >> test15.txt    
    echo "lookback period is" $i 
    echo "holding period is" $holding_period 
    echo "trigger is" $trigger
    echo "market band is" $market
if [ "$COUNTER" -gt "989" ]
then echo "counter is" $COUNTER >> buffer15.txt 
    sudo python events.py $i $holding_period $trigger $market $bin $switch >> buffer15.txt 
#   sudo python bollinger_events.py $i $holding_period $trigger $market $bin $switch >> score.txt

    sudo python sim2.py
#   sudo python analyzer.py $i $holding_period $trigger $market $bin $switch
    echo "counter is" $COUNTER >> searchrank15.txt
    sudo python analyzer2.py $i $holding_period $trigger $market $bin $switch >> searchrank15.txt 
fi
COUNTER=$((COUNTER+1))
echo $COUNTER
done
done
done
done
done
done
