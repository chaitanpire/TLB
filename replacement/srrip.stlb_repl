#include "cache.h"


#define maxRRPV 3

uint32_t rrpv[STLB_SET][STLB_WAY];

// initialize replacement state
void CACHE::stlb_initialize_replacement()
{
    cout << "Initialize SRRIP state" << endl;

    for (int i=0; i<STLB_SET; i++) {
        for (int j=0; j<STLB_WAY; j++) {
            rrpv[i][j] = maxRRPV;
        }
    }

}

// find replacement victim
uint32_t CACHE::stlb_find_victim(uint32_t cpu, uint64_t instr_id, uint32_t set, const BLOCK *current_set, uint64_t ip, uint64_t full_addr, uint32_t type)
{
    // look for the maxRRPV line
    int min_loc = INT16_MAX;
    int min_loc_index;
    while (1)
    {
        for (int i=0; i<STLB_WAY; i++)
            if (rrpv[set][i] == maxRRPV){
               
                if(min_loc >= current_set[i].ret_loc)
                {
                    min_loc = current_set[i].ret_loc;
                    min_loc_index = i;
                }
            }

        for (int i=0; i<STLB_WAY; i++)
            rrpv[set][i]++;

        if (min_loc == INT16_MAX) continue;

        return min_loc_index;
    }

    // WE SHOULD NOT REACH HERE
    assert(0);
    return 0;
}

// called on every cache hit and cache fill
void CACHE::stlb_update_replacement_state(uint32_t cpu, uint32_t set, uint32_t way, uint64_t full_addr, uint64_t ip, uint64_t victim_addr, uint32_t type, uint8_t hit)
{


    if ((type == WRITEBACK) && ip)
        assert(0);

    // uncomment this line to see the STLB accesses
    // cout << "CPU: " << cpu << "  STLB " << setw(9) << TYPE_NAME << " set: " << setw(5) << set << " way: " << setw(2) << way;
    // cout << hex << " paddr: " << setw(12) << paddr << " ip: " << setw(8) << ip << " victim_addr: " << victim_addr << dec << endl;
    
    if (hit)
        rrpv[set][way] = 0;
    else
        rrpv[set][way] = maxRRPV-1;
}

void CACHE::stlb_replacement_final_stats()
{

}
