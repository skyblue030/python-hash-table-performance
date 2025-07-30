import time
import matplotlib.pyplot as plt
import random

class SimulatedHashTable:
    """A class to simulate hash table insertions, resizing, and collisions."""
    def __init__(self, load_factor_threshold=0.66):
        self.load_factor_threshold = load_factor_threshold
        self.size = 8
        self.slots = [None] * self.size
        self.item_count = 0
        self.resize_count = 0
        self.collision_count = 0 

    def _resize(self):
        """Simulates the costly O(n) reallocation and copy."""
        self.resize_count += 1
        old_slots = self.slots
        new_size = self.size * 2
        
        # Reset the table
        self.size = new_size
        self.slots = [None] * new_size
        self.item_count = 0
        self.collision_count = 0 
        
        
        for item in old_slots:
            if item is not None:
                self.insert(item)

    def insert(self, item):
        """Inserts an item using a hash, handles collisions, and resizes."""
        
        if (self.item_count + 1) / self.size > self.load_factor_threshold:
            self._resize()
        
        
        index = hash(item) % self.size
        
        
        while self.slots[index] is not None:
            self.collision_count += 1
            index = (index + 1) % self.size 
            

        self.slots[index] = item
        self.item_count += 1

NUM_ITEMS_TO_INSERT = 200000
items_to_insert = [random.randint(0, 10000000) for _ in range(NUM_ITEMS_TO_INSERT)]

LOAD_FACTORS_TO_TEST = [0.5, 0.66, 0.8, 0.9, 0.95, 0.99]

results = {}

print("Running experiments with collision simulation...")


for lf in LOAD_FACTORS_TO_TEST:
    table = SimulatedHashTable(load_factor_threshold=lf)
    
    start_time = time.time()
    for item in items_to_insert:
        table.insert(item)
    end_time = time.time()
    
    total_time = end_time - start_time
    results[lf] = {
        "time": total_time,
        "resizes": table.resize_count,
        "collisions": table.collision_count
    }
    print(f"Load Factor: {lf:.2f} -> Time: {total_time:.4f}s, Collisions: {table.collision_count}")


load_factors = list(results.keys())
times = [res["time"] for res in results.values()]

plt.figure(figsize=(10, 6))
bars = plt.bar(range(len(load_factors)), times, tick_label=[str(lf) for lf in load_factors])

plt.xlabel("Load Factor Threshold")
plt.ylabel("Total Time to Insert 200,000 Items (seconds)")
plt.title("Hash Table Performance vs. Load Factor (with Collisions)")
plt.grid(axis='y', linestyle='--', alpha=0.7)

for i, bar in enumerate(bars):
    lf = load_factors[i]
    collisions = results[lf]["collisions"]
    time_val = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, time_val,
             f"{time_val:.3f}s\n({collisions:,} collisions)",
             ha='center', va='bottom', fontsize=9)

plt.savefig("load_factor_experiment_with_collisions.png")
print("\nGenerated plot: load_factor_experiment_with_collisions.png")