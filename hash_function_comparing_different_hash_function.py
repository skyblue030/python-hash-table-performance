import time
import matplotlib.pyplot as plt
import random
import mmh3
import xxhash
import hashlib
import blake3 

class SimulatedHashTable:
    def __init__(self, load_factor_threshold=0.8, hash_function_name='python_default'):
        self.load_factor_threshold = load_factor_threshold
        self.hash_function_name = hash_function_name
        self.size = 8
        self.slots = [None] * self.size
        self.item_count = 0

    def _fnv1a_64(self, data):
        hash_val = 0xcbf29ce484222325
        for byte in data:
            hash_val ^= byte
            hash_val *= 0x100000001b3
            hash_val &= 0xFFFFFFFFFFFFFFFF
        return hash_val

    def _get_hash(self, item):
        item_bytes = item.to_bytes(8, 'big', signed=True)
        if self.hash_function_name == 'modulo':
            return item % self.size
        elif self.hash_function_name == 'xxhash':
            return xxhash.xxh64(item_bytes).intdigest() % self.size
        elif self.hash_function_name == 'murmur':
            return mmh3.hash(item_bytes, signed=False) % self.size
        elif self.hash_function_name == 'fnv1a':
            return self._fnv1a_64(item_bytes) % self.size
        elif self.hash_function_name == 'sha256':
            digest = hashlib.sha256(item_bytes).digest()
            return int.from_bytes(digest, 'big') % self.size
        elif self.hash_function_name == 'blake3': # New hash function
            digest = blake3.blake3(item_bytes).digest()
            return int.from_bytes(digest, 'big') % self.size
        else:
            return hash(item) % self.size

    def _resize(self):
        old_slots = self.slots
        new_size = self.size * 2
        self.size = new_size
        self.slots = [None] * new_size
        self.item_count = 0
        for item in old_slots:
            if item is not None:
                self.insert(item, is_rehashing=True)

    def insert(self, item, is_rehashing=False):
        if not is_rehashing and (self.item_count + 1) / self.size > self.load_factor_threshold:
            self._resize()
        index = self._get_hash(item)
        while self.slots[index] is not None:
            index = (index + 1) % self.size
        self.slots[index] = item
        self.item_count += 1


NUM_ITEMS_TO_INSERT = 100000
items_to_insert = [random.randint(-10000000, 10000000) for _ in range(NUM_ITEMS_TO_INSERT)]
LOAD_FACTORS_TO_TEST = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
HASH_FUNCTIONS_TO_TEST = ["modulo", "python_default", "xxhash", "murmur", "fnv1a", "sha256", "blake3"]
results = {func_name: [] for func_name in HASH_FUNCTIONS_TO_TEST}

print("Running comprehensive hash function experiment...")
print("This will take a few minutes...")

for func_name in HASH_FUNCTIONS_TO_TEST:
    print(f"Testing hash function: {func_name}...")
    for lf in LOAD_FACTORS_TO_TEST:
        table = SimulatedHashTable(load_factor_threshold=lf, hash_function_name=func_name)
        start_time = time.time()
        for item in items_to_insert:
            table.insert(item)
        end_time = time.time()
        results[func_name].append(end_time - start_time)
    print(f"...done.")


plt.figure(figsize=(14, 8))

crypto_hashes = {'sha256', 'blake3'} 

for func_name, times in results.items():
    if func_name in crypto_hashes:
        label = f"{func_name} (Crypto)"
    else:
        label = f"{func_name} (Perf.)"
    
    plt.plot(LOAD_FACTORS_TO_TEST, times, marker='o', linestyle='-', label=label)

plt.xlabel("Load Factor Threshold")
plt.ylabel(f"Total Time to Insert {NUM_ITEMS_TO_INSERT} Items (seconds)")
plt.title("Hash Function Performance vs. Load Factor")
plt.legend()
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.savefig("final_hash_comparison.png")
print("\nGenerated plot: final_hash_comparison.png")