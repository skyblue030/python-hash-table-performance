import time
import matplotlib.pyplot as plt

class SimulatedHashTable:
    """A simple class to simulate hash table insertions and resizing."""
    def __init__(self, load_factor_threshold=0.66):
        self.load_factor_threshold = load_factor_threshold
        self.size = 8  # Initial size of the underlying list
        self.slots = [None] * self.size
        self.item_count = 0
        self.resize_count = 0

    def _resize(self):
        """Simulates the costly O(n) reallocation and copy."""
        self.resize_count += 1
        new_size = self.size * 2
        
        # This is the costly part: creating a new list.
        # In a real hash table, you would also re-hash and copy all items.
        new_slots = [None] * new_size
        for i in range(self.size):
            new_slots[i] = self.slots[i]
            
        self.slots = new_slots
        self.size = new_size

    def insert(self, item):
        """Inserts an item and triggers a resize if the load factor is exceeded."""
        # Check if a resize is needed BEFORE adding the new item
        current_load_factor = (self.item_count + 1) / self.size
        if current_load_factor > self.load_factor_threshold:
            self._resize()
        
        # In a real hash table, we would find a slot. Here, we just increment.
        self.slots[self.item_count % self.size] = item
        self.item_count += 1

# --- Experiment Setup ---
NUM_ITEMS_TO_INSERT = 200000
LOAD_FACTORS_TO_TEST = [0.5, 0.66, 0.8, 0.9, 0.99]

results = {}

print("Running experiments...")

# --- Run Experiment for each Load Factor ---
for lf in LOAD_FACTORS_TO_TEST:
    table = SimulatedHashTable(load_factor_threshold=lf)
    
    start_time = time.time()
    for i in range(NUM_ITEMS_TO_INSERT):
        table.insert(i)
    end_time = time.time()
    
    total_time = end_time - start_time
    results[lf] = {
        "time": total_time,
        "resizes": table.resize_count
    }
    print(f"Load Factor: {lf:.2f} -> Time: {total_time:.4f}s, Resizes: {table.resize_count}")


# --- Visualization ---
load_factors = list(results.keys())
times = [res["time"] for res in results.values()]

plt.figure(figsize=(10, 6))
bars = plt.bar(range(len(load_factors)), times, tick_label=[str(lf) for lf in load_factors])

plt.xlabel("Load Factor Threshold")
plt.ylabel("Total Time to Insert 200,000 Items (seconds)")
plt.title("Hash Table Performance vs. Load Factor")
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add text labels on top of each bar
for i, bar in enumerate(bars):
    lf = load_factors[i]
    resizes = results[lf]["resizes"]
    time_val = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, time_val,
             f"{time_val:.3f}s\n({resizes} resizes)",
             ha='center', va='bottom', fontsize=9)

plt.savefig("load_factor_experiment.png")
print("\nGenerated plot: load_factor_experiment.png")