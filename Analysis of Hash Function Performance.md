# Analysis of Hash Function Performance

> This report evaluates several performance-oriented and cryptographic hash functions based on their performance in a simulated hash table. The key metric is the total time required to insert 100,000 items at various load factor thresholds.

---

### `modulo` (Performance)

* **Advantages**: In this specific experiment with random integer data, modulo was consistently one of the fastest functions. It is computationally the simplest operation.
* **Disadvantages**: This is not a good general-purpose hash function. Its performance is highly dependent on the input data. With patterned data (e.g., all even numbers), it would lead to massive collisions and terrible performance.
* **Reason for Choosing**: It's rarely used in real-world applications. Its primary use is in academic examples as a simple baseline.
* **Best Application Scenarios**: Educational purposes or niche situations where the input keys are guaranteed to be uniformly distributed.

---

### `python_default` (Performance)

* **Advantages**: It is built-in, requiring no extra libraries. It provides good, reliable performance as seen in the chart and is secure against hash collision DoS attacks because it uses a random seed for each Python session (SipHash).
* **Disadvantages**: It is not the absolute fastest option available. The hash values are not consistent across different program executions, making it unsuitable for persistent storage or network hashing.
* **Reason for Choosing**: Convenience and safety. It's the default for a reason.
* **Best Application Scenarios**: The default choice for nearly all standard use cases of Python dictionaries (`dict`) and sets (`set`).

---

### `xxhash` & `murmur` (Performance)

* **Advantages**: These are industry standards known for being extremely fast with excellent key distribution, which minimizes collisions. They produce consistent hash values, meaning the hash of a given input will be the same every time.
* **Disadvantages**: They require installing third-party libraries. In your specific test, `xxhash` appeared slower than other performance hashes, which could be due to the overhead of its Python wrapper on very small 8-byte inputs.
* **Reason for Choosing**: When you need the absolute best performance for a hash table and require consistent hash outputs.
* **Best Application Scenarios**: High-performance databases, caches, distributed systems, and checksums.

---

### `fnv1a` (Performance)

* **Advantages**: It is very simple to implement from scratch and has decent performance without requiring external libraries.
* **Disadvantages**: It is generally outperformed by more modern, complex algorithms like `xxhash` and `murmur`.
* **Reason for Choosing**: When you need a good, non-cryptographic hash but want to avoid adding third-party dependencies.
* **Best Application Scenarios**: Embedded applications or systems where the codebase must be minimal and self-contained.

---

### `sha256` & `blake3` (Cryptographic)

* **Advantages**: Their primary advantage is security. They are designed to be collision-resistant and one-way (irreversible), which is essential for cryptographic applications.
* **Disadvantages**: They are dramatically slower than all the performance-oriented hashes, as proven by your chart. This is a direct result of the complex computational work required to provide security guarantees.
* **Reason for Choosing**: When the top priority is security and data integrity, not speed within a data structure.
* **Best Application Scenarios**: Never for hash tables. They are used for password storage, digital signatures, blockchain technology, and verifying file downloads.
