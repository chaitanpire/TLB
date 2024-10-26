# Loop over each trace file in the traces directory
for i in `ls -1 ./traces/`; do
    # Run each configuration and save output to a unique log file
    mkdir -p ./logs_srrip/${i}
    # mkdir -p ./logs/${i}
    
    ./bin/srrip-1core -warmup_instructions 25000000 -simulation_instructions 25000000 -traces ./traces/$i > ./logs_srrip/$i/srrip.txt
    # ./bin/srrip_cost_aware_max-1core -warmup_instructions 25000000 -simulation_instructions 25000000 -traces ./traces/$i > ./logs_srrip/${i}/srrip_cost_aware_max.txt
    # ./bin/srrip_cost_aware_min-1core -warmup_instructions 25000000 -simulation_instructions 25000000 -traces ./traces/$i > ./logs_srrip/${i}/srrip_cost_aware_min.txt
    # ./bin/lru-1core -warmup_instructions 25000000 -simulation_instructions 25000000 -traces ./traces/$i > ./logs/${i}/lru.txt
    
    mv collisions.txt ./logs_srrip/$i/
done
