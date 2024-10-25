./build_champsim.sh srrip 1 
./build_champsim.sh lru 1
for i in `ls -1 ./traces/`; do
    ./bin/srrip-1core -warmup_instructions 25000000 -simulation_instructions 25000000 -traces ./traces/$i > ./logs/${i}_srrip.txt
    ./bin/lru-1core -warmup_instructions 25000000 -simulation_instructions 25000000 -traces ./traces/$i > ./logs/${i}_lru.txt
done