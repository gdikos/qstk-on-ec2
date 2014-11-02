#!/bin/bash
for i in 10 15 20 
do
    for holding_period in 1 5 10 20 50 100 250
    do
       for trigger in -1.5 -1.3 -1.0 0 1.0 1.3 1.5 
       do
       for market in -1.5 -1 0 1 1.5
           do
    echo "lookback period is" $i >> test2.txt   
    echo "holding period is" $holding_period >> test2.txt 
    echo "trigger is" $trigger >> test2.txt    
    echo "lookback period is" $i 
    echo "holding period is" $holding_period 
    echo "trigger is" $trigger
    echo "market band is" $market
    sudo python bollinger_events.py $i $holding_period $trigger $market   
    sudo python market_sim.py
    sudo python analyzer.py $i $holding_period $trigger $market

    sudo python analyzer.py $i $holding_period $trigger $market >> score.txt
    done
done
done
done 
