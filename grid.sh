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
    echo "lookback period is" $i >> test2.txt   
    echo "holding period is" $holding_period >> test2.txt 
    echo "trigger is" $trigger >> test2.txt    
    echo "lookback period is" $i 
    echo "holding period is" $holding_period 
    echo "trigger is" $trigger
    echo "market band is" $market
if [ "$COUNTER" -gt "1621" ]
then echo "counter is" $COUNTER >> buffer4.txt 
    sudo python bollinger_events.py $i $holding_period $trigger $market $bin $switch >> buffer4.txt 
#   sudo python bollinger_events.py $i $holding_period $trigger $market $bin $switch >> score.txt

    sudo python market_sim.py
#   sudo python analyzer.py $i $holding_period $trigger $market $bin $switch
    echo "counter is" $COUNTER >> searchrank4.txt
    sudo python analyzer.py $i $holding_period $trigger $market $bin $switch >> searchrank4.txt 
fi
COUNTER=$((COUNTER+1))
echo $COUNTER
done
done
done
done
done
done
