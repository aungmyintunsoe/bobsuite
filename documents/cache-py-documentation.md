# Comprehensive Documentation for cache.py
**File:** mcp_server/lib/utils/cache.py
**Language:** Python
**Documentation type:** Comprehensive Documentation
**Generated:** 2026-05-17T09:30:57.569194Z

---

## API Documentation

# Usage examples:
# cache = get_cache()
# cache_key = cache.get_cache_key("example.txt", "qa_scan")
# cached_result = cache.get(cache_key)
# if cached_result:
#     print("Result from cache:", cached_result)
# else:
#     print("Running analysis...")
#     # Perform analysis here
#     result = {"status": "success", "data": "example data"}
#     cache.set(cache_key, result)
#     print("Result cached:", result)

## Quick Start Guide

Minimal setup steps:
1. Ensure you have Python 3.8+ installed.
2. Add the above code to a file named `filecache.py` in your project.
3. Import the `get_cache` function from `filecache`.

Basic usage example:
```python
from filecache import get_cache

# Initialize cache
cache = get_cache()

# Example: Caching the result of a file analysis
def analyze_file(file_path):
    # Simulate analysis (replace with actual logic)
    result = {"file": file_path, "size": 1234, "lines": 100}
    return result

def cached_analyze(file_path):
    # Create a unique cache key for the file
    cache_key = f"analyze_{file_path}"
    
    # Try to get cached result
    cached_result = cache.get(cache_key)
    if cached_result:
        print("Using cached result")
        return cached_result
    
    # If not cached, perform analysis
    result = analyze_file(file_path)
    print("Performing analysis")
    
    # Cache the result
    cache.set(cache_key, result)
    return result

# Usage
print(cached_analyze("example.txt"))
print(cached_analyze("example.txt"))  # This will use the cache
```

Next steps:
- Experiment with different TTL (time-to-live) values for your cache entries.
- Implement cache clearing strategies based on your application's needs.
- Consider integrating with your existing project structure.

Detailed documentation:
- For more information on Python's `hashlib` module: https://docs.python.org/3/library/hashlib.html
- For details on Python's `pathlib` module: https://docs.python.org/3/library/pathlib.html
- For JSON handling in Python: https://docs.python.org/3/library/json.html
- For more advanced caching strategies, consider looking into libraries like `cachetools` or `diskcache`.

## User Manual

# --------------------------------------------------------------------------------------------
# Overview and Purpose
# --------------------------------------------------------------------------------------------
# This module provides a simple file-based caching system using MD5 hashing. The primary purpose of this cache is to optimize performance by skipping re-analysis of unchanged files. It achieves this by generating a unique cache key based on the file content hash and operation type, and storing/retrieving cached results from both memory and disk. The cache entries have a configurable time-to-live (TTL) to ensure that stale data is not used indefinitely.

# --------------------------------------------------------------------------------------------
# Installation Instructions
# --------------------------------------------------------------------------------------------
# To use this caching utility, you need to have Python installed on your system. This module does not have any external dependencies other than the Python standard library. You can simply copy the provided code into your project or install it as a package if you prefer.

# --------------------------------------------------------------------------------------------
# Configuration Options
# --------------------------------------------------------------------------------------------
# The FileCache class accepts two configuration parameters:
# 1. cache_dir (str): The directory where cache files will be stored. Default is ".bob_cache".
# 2. ttl_hours (float): The time-to-live for cache entries in hours. Default is 24 hours.

# Example:
# cache = FileCache(cache_dir="my_cache", ttl_hours=48)

# --------------------------------------------------------------------------------------------
# Usage Examples
# --------------------------------------------------------------------------------------------
# Here are some basic usage examples of how to use the FileCache class:

# 1. Initialize the cache:
# cache = FileCache()

# 2. Generate a cache key for a file:
# cache_key = cache.get_cache_key("path/to/file.txt", "qa_scan")

# 3. Retrieve a cached result:
# result = cache.get(cache_key)
# if result:
#     print("Found cached result:", result)
# else:
#     print("No cached result found")

# 4. Store a result in the cache:
# cache.set(cache_key, {"data": "example"})
# print("Result cached successfully")

# 5. Clear the cache for a specific operation:
# cache.clear("qa_scan")
# print("Cache cleared for qa_scan operation")

# --------------------------------------------------------------------------------------------
# Common Use Cases
# --------------------------------------------------------------------------------------------
# This caching utility is particularly useful in scenarios where you need to perform expensive operations on files and want to avoid re-processing unchanged files. Some common use cases include:
# 1. Code analysis tools that scan files for quality assurance or linting purposes.
# 2. Documentation generation systems that need to process files and generate documentation.
# 3. Visualization tools that generate visual representations of data from files.
# 4. Any other scenarios where file content remains relatively stable over time, and re-processing can be avoided.

# --------------------------------------------------------------------------------------------
# Best Practices
# --------------------------------------------------------------------------------------------
# To make the most out of this caching utility, consider the following best practices:
# 1. Choose an appropriate TTL based on your specific use case. If the files change frequently, a shorter TTL may be appropriate. If the files are relatively static, a longer TTL can be used to maximize cache hits.
# 2. Use meaningful operation names when generating cache keys to differentiate between different types of operations.
# 3. Ensure that the cache directory has sufficient permissions for reading and writing cache files.
# 4. Regularly monitor and clean up the cache directory to prevent it from growing too large, especially if the TTL is set to a long duration.
# 5. Consider using the memory cache for frequently accessed entries to improve performance further. The cache automatically stores retrieved results in memory for faster subsequent access.
# 6. Handle potential exceptions gracefully when using the cache methods to ensure the robustness of your application.

# By following these best practices and leveraging the caching utility appropriately, you can significantly improve the performance of your file-processing operations by avoiding unnecessary re-analysis of unchanged files.

## How-To Guide

Objective:
The objective of this code is to provide a simple file-based caching utility using MD5 hashing. It aims to optimize performance by skipping re-analysis of unchanged files, resulting in a 2-3x speedup.

Prerequisites:
- Python 3.x installed
- The provided code saved in a Python file (e.g., `file_cache.py`)

Step-by-step instructions:
1. Import the necessary modules:
   - `hashlib` for generating MD5 hashes
   - `json` for serializing and deserializing data
   - `pathlib` for handling file paths
   - `typing` for type hints
   - `datetime` for handling timestamps

2. Define the `FileCache` class:
   - Initialize the cache with a `cache_dir` (default: ".bob_cache") and `ttl_hours` (default: 24)
   - Create the cache directory if it doesn't exist
   - Set the time-to-live (TTL) for cache entries
   - Initialize an empty memory cache dictionary

3. Implement the `get_file_hash` method:
   - Generate an MD5 hash of the file content
   - Read the file content if not provided
   - Return the MD5 hash string

4. Implement the `get_cache_key` method:
   - Generate a cache key combining the file path, file hash, and operation type
   - Hash the file path to prevent collisions between files with identical content
   - Hash the file content using `get_file_hash`
   - Combine all three components for a unique cache key

5. Implement the `get` method:
   - Retrieve the cached result if it exists and is not expired
   - Check the memory cache first
   - If not found in memory, check the disk cache
   - If found, check if the cache entry is expired based on the TTL
   - If not expired, store the result in the memory cache and return it
   - If expired or not found, return None

6. Implement the `set` method:
   - Store the result in the cache
   - Store the result in memory cache
   - Serialize the result and timestamp to a JSON file on disk
   - Return True if successful, False otherwise

7. Implement the `clear` method:
   - Clear cache entries based on the specified operation (optional)
   - Clear entries from memory cache
   - Clear entries from disk cache based on the operation or all entries if no operation is specified
   - Return the number of entries cleared

8. Implement the `get_stats` method:
   - Get cache statistics
   - Return a dictionary with cache stats including memory entries, disk entries, cache directory, and TTL in hours

9. Define the `get_cache` function:
   - Get or create the global cache instance
   - If the global cache instance is None, create a new `FileCache` instance with the provided `cache_dir` and `ttl_hours`
   - Return the global cache instance

10. Use the caching utility in your code:
    - Import the `get_cache` function from the file where the `FileCache` class is defined
    - Call `get_cache()` to obtain the cache instance
    - Use the cache instance's methods (`get`, `set`, `clear`, `get_stats`) to interact with the cache

Expected outcomes:
- The caching utility will store and retrieve cached results based on file content hashes
- Unchanged files will be skipped, resulting in faster execution
- Cache entries will expire based on the specified TTL
- Cache statistics can be obtained using the `get_stats` method

Tips and warnings:
- Ensure that the `cache_dir` exists and has appropriate write permissions
- Be cautious when clearing the cache, as it will remove all cached entries
- Adjust the `ttl_hours` parameter based on your specific requirements and the frequency of file changes
- Consider handling exceptions appropriately when using the caching utility
- The provided code assumes that the files being cached are text files. If you need to cache binary files, you may need to modify the code accordingly

## Tutorial

Learning Objectives:
1. Understand the concept of caching and its benefits in performance optimization.
2. Learn how to implement a simple file-based cache using MD5 hashing in Python.
3. Gain familiarity with file handling, hashing, JSON serialization, and file system operations.
4. Understand how to manage cache entries, including setting, getting, and clearing cache data.
5. Learn how to design and implement a caching system with time-to-live (TTL) functionality.

Prerequisites:
- Basic understanding of Python programming.
- Familiarity with file handling and JSON in Python.
- Basic knowledge of hashing algorithms, particularly MD5.
- Understanding of the concept of caching and its role in performance optimization.

Step-by-Step Lessons:

Lesson 1: Introduction to Caching
- Understand what caching is and why it's important for performance optimization.
- Learn about different types of caching mechanisms (in-memory, disk-based, etc.).
- Discuss the benefits of caching, such as reducing computation time and minimizing redundant operations.

Lesson 2: Setting Up the Cache Directory
- Learn how to initialize the cache directory using the `Path` class from the `pathlib` module.
- Understand the purpose of the `cache_dir` parameter in the `FileCache` class constructor.
- Explore the `mkdir` method and its `exist_ok` parameter to ensure the cache directory is created if it doesn't exist.

Lesson 3: Generating File Hashes
- Understand the concept of hashing and its role in caching.
- Learn how to generate an MD5 hash of file content using the `hashlib` module.
- Explore the `get_file_hash` method, which reads the file content and returns its MD5 hash.
- Discuss the importance of hashing file content to uniquely identify files and detect changes.

Lesson 4: Creating Cache Keys
- Learn how to create unique cache keys using a combination of file path, file hash, and operation type.
- Understand the purpose of the `get_cache_key` method and its parameters.
- Explore the process of hashing the file path and content to generate a unique cache key.
- Discuss the significance of combining these components to prevent cache key collisions.

Lesson 5: Retrieving Cached Results
- Understand how to retrieve cached results using the `get` method.
- Learn how to check the memory cache first before accessing the disk cache.
- Explore the process of reading cached data from a JSON file on disk.
- Discuss the importance of checking the timestamp of cached entries to determine if they have expired.
- Learn how to store retrieved results in the memory cache for faster subsequent access.

Lesson 6: Storing Cached Results
- Learn how to store results in the cache using the `set` method.
- Understand the process of storing results in both the memory cache and disk cache.
- Explore the JSON serialization of cached data, including the timestamp and result.
- Discuss the importance of persisting cached data to disk for durability and recovery.

Lesson 7: Clearing Cache Entries
- Understand how to clear cache entries using the `clear` method.
- Learn how to clear specific cache entries based on the operation type.
- Explore the process of removing cache files from the disk cache directory.
- Discuss the significance of clearing cache entries to manage disk space and maintain cache freshness.

Lesson 8: Obtaining Cache Statistics
- Learn how to retrieve cache statistics using the `get_stats` method.
- Understand the information provided by the cache statistics, such as memory entries, disk entries, cache directory, and TTL.
- Discuss the importance of monitoring cache statistics for performance analysis and optimization.

Practice Exercises:

Exercise 1: Implementing the `FileCache` Class
- Create a new Python file and implement the `FileCache` class based on the provided code.
- Ensure that all methods and their functionalities are correctly implemented.
- Test the class by creating an instance of `FileCache` and performing various operations like setting and getting cache entries.

Exercise 2: Testing Cache Retrieval and Storage
- Write a script that demonstrates the usage of the `FileCache` class.
- Create a sample file and store its content in the cache using a specific operation type.
- Retrieve the cached result using the corresponding cache key.
- Modify the file content and verify that the cache is updated accordingly.
- Clear the cache for the specific operation type and check if the cache entries are removed.

Exercise 3: Exploring Cache Statistics
- Extend the previous exercise by adding code to retrieve and display cache statistics.
- Print the memory entries, disk entries, cache directory, and TTL of the cache.
- Analyze the cache statistics and discuss their significance in understanding cache performance.

Summary and Next Steps:
In this tutorial, we explored the concept of caching and learned how to implement a simple file-based cache using MD5 hashing in Python. We covered the following key points:

- Caching is a technique used to store frequently accessed or computationally expensive data to improve performance.
- The `FileCache` class provides a simple and efficient way to cache results based on file content hash.
- The cache system uses a combination of file path, file hash, and operation type to generate unique cache keys.
- Cached results are stored in both memory and disk to optimize retrieval speed and durability.
- The cache system supports clearing specific cache entries based on operation type and provides cache statistics for monitoring.

Next Steps:
- Experiment with different cache TTL values to understand the impact on cache freshness and performance.
- Explore advanced caching techniques, such as distributed caching or in-memory caching using Redis or Memcached.
- Integrate the `FileCache` class into your own projects to optimize performance and reduce redundant operations.
- Consider implementing additional features, such as cache expiration based on file modification time or support for multiple cache directories.

## Troubleshooting Guide

Common issues and solutions when using the FileCache module:

**Issue 1: Cache directory permission errors**
- Symptom: Unable to create or write to cache files
- Solution: Ensure the cache directory has appropriate read/write permissions
- Check: Verify the user running the application has permission to create files in the cache directory

**Issue 2: Cache not being used (always re-processing files)**
- Symptom: Performance not improving, files always being re-analyzed
- Solution: Check if TTL is too short or if file content is changing
- Debug: Use `get_stats()` to check cache hit rates and verify cache keys are being generated correctly

**Issue 3: Stale cache entries**
- Symptom: Getting outdated results from cache
- Solution: Reduce TTL value or manually clear cache using `clear()` method
- Prevention: Set appropriate TTL based on how frequently files change

**Issue 4: Cache directory growing too large**
- Symptom: Disk space issues due to large cache directory
- Solution: Implement regular cache cleanup using `clear()` method
- Prevention: Set shorter TTL values or implement automated cleanup scripts

**Issue 5: Memory cache consuming too much RAM**
- Symptom: High memory usage
- Solution: The memory cache is bounded by the number of unique cache keys accessed
- Mitigation: Restart the application periodically or implement cache size limits

## Requirements Specification

Software Requirements Specification (SRS)

1. Introduction
1.1 Purpose
The purpose of this document is to specify the requirements for the FileCache module, a caching utility that uses MD5 hashing to optimize performance by skipping the re-analysis of unchanged files.

1.2 Scope
The FileCache module is designed to be used in various software systems that require caching of file-based results. It can be integrated into any Python-based project to improve performance by avoiding redundant file processing.

1.3 Definitions, Acronyms, and Abbreviations
- MD5: Message-Digest Algorithm 5, a widely used cryptographic hash function
- TTL: Time-to-Live, the duration for which a cache entry is considered valid

2. Overall Description
2.1 Product Perspective
The FileCache module is a standalone Python module that can be integrated into any software system requiring file-based caching. It does not depend on any external systems or services.

2.2 Product Functions
- Generate MD5 hash of file content
- Generate a cache key combining file path, file hash, and operation type
- Retrieve cached results if they exist and are not expired
- Store results in the cache
- Clear cache entries based on operation type
- Retrieve cache statistics

2.3 User Classes and Characteristics
- Developers integrating the FileCache module into their software systems
- End-users who benefit from improved performance due to caching

2.4 Operating Environment
- Python 3.x
- Any operating system supporting Python

2.5 Design and Implementation Constraints
- The cache directory must be writable
- The cache directory should have sufficient storage space
- The TTL value should be set appropriately based on the specific use case

2.6 Assumptions and Dependencies
- The MD5 hash function is collision-resistant enough for the intended use case
- The file system supports the required file operations

3. External Interface Requirements
3.1 User Interfaces
- No user interfaces are provided by the FileCache module

3.2 Hardware Interfaces
- No specific hardware interfaces are required

3.3 Software Interfaces
- The FileCache module depends on the following Python standard library modules:
  - hashlib
  - json
  - pathlib
  - typing
  - datetime

3.4 Communications Interfaces
- No communication interfaces are involved

4. System Features
4.1 get_file_hash
- Description: Generate MD5 hash of file content
- Input: file_path (str), content (Optional[str])
- Output: MD5 hash string (str)

4.2 get_cache_key
- Description: Generate a cache key combining file path, file hash, and operation type
- Input: file_path (str), operation (str), content (Optional[str])
- Output: Cache key string (str)

4.3 get
- Description: Retrieve cached result if it exists and is not expired
- Input: cache_key (str)
- Output: Cached result (Optional[Dict[str, Any]]) or None

4.4 set
- Description: Store result in cache
- Input: cache_key (str), result (Dict[str, Any])
- Output: True if successful, False otherwise

4.5 clear
- Description: Clear cache entries based on operation type
- Input: operation (Optional[str])
- Output: Number of entries cleared (int)

4.6 get_stats
- Description: Get cache statistics
- Input: None
- Output: Dictionary with cache stats (Dict[str, Any])

5. Nonfunctional Requirements
5.1 Performance Requirements
- The FileCache module should provide a 2-3x speedup by skipping unchanged files
- The cache lookup and storage operations should have minimal overhead

5.2 Security Requirements
- The MD5 hash function is used for generating file hashes, which should be sufficient for the intended use case
- No sensitive information is stored in the cache

5.3 Reliability Requirements
- The FileCache module should handle exceptions gracefully and not cause the entire system to fail
- Cache entries should be retrieved and stored reliably

5.4 Maintainability Requirements
- The code should be well-documented and follow best practices
- The module should be easy to integrate and use in other projects

5.5 Portability Requirements
- The FileCache module should be compatible with Python 3.x on any operating system supporting Python

6. System Constraints
6.1 System Constraints
- The cache directory must have sufficient storage space
- The cache directory must be writable
- The TTL value should be set appropriately based on the specific use case

7. Dependencies
7.1 Dependencies
- Python 3.x
- hashlib
- json
- pathlib
- typing
- datetime

8. Acceptance Criteria
8.1 The FileCache module should be able to generate MD5 hashes of file content
8.2 The FileCache module should generate unique cache keys combining file path, file hash, and operation type
8.3 The FileCache module should retrieve cached results if they exist and are not expired
8.4 The FileCache module should store results in the cache efficiently
8.5 The FileCache module should clear cache entries based on operation type
8.6 The FileCache module should provide cache statistics
8.7 The FileCache module should provide a 2-3x speedup by skipping unchanged files
8.8 The FileCache module should handle exceptions gracefully and not cause the entire system to fail
8.9 The FileCache module should be compatible with Python 3.x on any operating system supporting Python

9. Glossary
- MD5: Message-Digest Algorithm 5, a widely used cryptographic hash function
- TTL: Time-to-Live, the duration for which a cache entry is considered valid