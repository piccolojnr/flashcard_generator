import unittest
import time
import os
import scripts.caching as caching  # assuming the functions are in a file named testing.py
import datetime


class TestCacheFunctions(unittest.TestCase):

    def setUp(self):
        self.cache_db_path = 'test_cache.db'  # path to your test database
        caching.init_cache_db(self.cache_db_path)
        self.test_data = None
        with open('extracted_data/output_0.txt') as f:
            self.test_data = f.read().strip()
        
        with open("test_path", "w") as f:
            f.write("test")
            
    def tearDown(self):
        os.remove(self.cache_db_path)
        os.remove("test_path")
    

    
    def print_db(self):
        result = caching.get_cache(self.cache_db_path)
        
        # print the contents of the cache database and beautify it
        print("Cache database contents:")
        print("Hash\t\t\tFile Path\tFile Size\tUpdated At")
        print("-" * 40)
        for row in result:
            print(f"{row[0][0:17]}...\t{row[1]}\t{row[2]}\t{row[3]}")
        print("-" * 40)
        
        
    def test_init_cache_db(self):
        self.assertTrue(os.path.exists(self.cache_db_path))
    
    def test_get_cache(self):
        result = caching.get_cache(self.cache_db_path)
        self.assertEqual(len(result), 0)
    
    def test_add_file_path_to_cache(self):
        hash = caching.generate_sha256(self.test_data)
        caching.add_file_path_to_cache(self.cache_db_path, hash, 'test_path')
        
        result = caching.get_cache(self.cache_db_path)

        self.assertIsNotNone(result)
        self.assertEqual(result[0][1], 'test_path')
        
    def test_cache_size(self):
        # Add 10 entries to the cache
        for i in range(10):
            caching.add_file_path_to_cache(self.cache_db_path, caching.generate_sha256(f'test_hash_{i}'), 'test_path')
        
        size = caching.get_cache_size(self.cache_db_path)
        self.assertEqual(size, 10)
    
    def test_cache_size_limit(self):
        # Add entries until the cache size limit is reached
        for i in range(10):
            caching.add_file_path_to_cache(self.cache_db_path, caching.generate_sha256(f'test_hash_{i}'), 'test_path')
        
        # Check that the cache size is 10
        result = caching.get_cache(self.cache_db_path)
        self.assertEqual(len(result), 10)
        
        # Add another entry
        caching.add_file_path_to_cache(self.cache_db_path, caching.generate_sha256('test_hash_10'), 'test_path')
        
        # Check that the cache size is still 10
        result = caching.get_cache(self.cache_db_path)
        self.assertEqual(len(result), 10)

    
    def test_delete_oldest_entry(self):
        # Add an entry with a known timestamp
        
        for i in range(10):
            caching.add_file_path_to_cache(self.cache_db_path, caching.generate_sha256(f'test_hash_{i}'), 'test_path')
        
        size = caching.get_cache_size(self.cache_db_path)
        
        caching.delete_oldest_entry(self.cache_db_path)
        
        size_after = caching.get_cache_size(self.cache_db_path)
        
        self.assertEqual(size - 1, size_after)
        
        
        
    def test_update_file_path_in_cache(self):
        # Add an entry with a known hash
        hash = caching.generate_sha256(self.test_data)
        caching.add_file_path_to_cache(self.cache_db_path, hash, 'test_path')
        cache = caching.get_cache(self.cache_db_path)
        before =  datetime.datetime.strptime(cache[0][3], '%Y-%m-%d %H:%M:%S')
        time.sleep(1)
        caching.update_file_path_in_cache(self.cache_db_path, hash, 'new_path')
        cache = caching.get_cache(self.cache_db_path)
        after = datetime.datetime.strptime(cache[0][3], '%Y-%m-%d %H:%M:%S')
        self.assertEqual(cache[0][1], 'new_path')
        
        self.assertGreater(after, before)
        

    def test_get_file_path_from_cache(self):
        # Add an entry with a known hash and file path
        caching.add_file_path_to_cache(self.cache_db_path, 'test_hash', 'test_path')

        result = caching.get_file_path_from_cache(self.cache_db_path, 'test_hash')

        self.assertEqual(result, 'test_path')

    def test_get_file_size_from_cache(self):
        # Add an entry with a known hash and file size
        caching.add_file_path_to_cache(self.cache_db_path, 'test_hash', 'test_path')

        result = caching.get_file_size_from_cache(self.cache_db_path, 'test_hash')

        self.assertEqual(result, 4)

if __name__ == '__main__':
    unittest.main()