
import hashlib
import sqlite3
import os


CACHE_LIMIT = 10


def init_cache_db(cache_db_path: str):
    """
    Initializes the cache database by creating a table if it doesn't exist.

    Args:
        cache_db_path (str): The path to the cache database file.

    Returns:
        None
    """
    conn = sqlite3.connect(cache_db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cache (
            hash TEXT PRIMARY KEY,
            file_path TEXT,
            file_size INTEGER,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()



# Function to get the file path from the cache database
import sqlite3

def get_file_path_from_cache(cache_db_path: str, hash: str):
    """
    Retrieves the file path associated with the given hash from the cache database.

    Args:
        cache_db_path (str): The path to the cache database.
        hash (str): The hash value to search for in the cache.

    Returns:
        str: The file path associated with the given hash, or None if no matching hash is found.
    """
    conn = sqlite3.connect(cache_db_path)
    c = conn.cursor()
    c.execute('''
        SELECT file_path FROM cache WHERE hash = ?
    ''', (hash,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

import hashlib

def generate_sha256(file: str) -> str:
    """
    Generate the SHA256 hash value of a file.

    Args:
        file (str): The file to generate the hash value for.

    Returns:
        str: The SHA256 hash value of the file.
    """
    sha = hashlib.sha256()
    sha.update(file.encode('utf-8'))
    return sha.hexdigest()

# add the file path to the cache database queue
def add_file_path_to_cache(cache_db_path: str, hash: str, file_path: str):
    file_size = os.path.getsize(file_path)
    conn = sqlite3.connect(cache_db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO cache (hash, file_path, file_size) VALUES (?, ?, ?)
    ''', (hash, file_path, file_size))
    conn.commit()
    conn.close()
    size = get_cache_size(cache_db_path) 
    if size > CACHE_LIMIT:
        delete_oldest_entry(cache_db_path)

# get cache
def get_cache(cache_db_path: str):
    """
    Retrieves all the data from the cache table in the specified SQLite database.

    Args:
        cache_db_path (str): The path to the SQLite database file.

    Returns:
        list: A list of tuples representing the rows retrieved from the cache table.
    """
    conn = sqlite3.connect(cache_db_path)
    c = conn.cursor()
    c.execute('''
        SELECT * FROM cache
    ''')
    result = c.fetchall()
    conn.close()
    return result

# check database size
import sqlite3

def get_cache_size(cache_db_path: str) -> int:
    """
    Retrieves the number of records in the cache table of the specified database.

    Args:
        cache_db_path (str): The path to the cache database.

    Returns:
        int: The number of records in the cache table.
    """
    conn = sqlite3.connect(cache_db_path)
    c = conn.cursor()
    c.execute('''
        SELECT COUNT(*) FROM cache
    ''')
    result = c.fetchone()
    conn.close()
    return result[0]

# delete the oldest entry in the cache database
import sqlite3

def delete_oldest_entry(cache_db_path: str):
    """
    Deletes the oldest entry from the cache table in the specified SQLite database.

    Args:
        cache_db_path (str): The path to the SQLite database file.

    Returns:
        None
    """
    conn = sqlite3.connect(cache_db_path)
    c = conn.cursor()
    c.execute('''
        SELECT * FROM cache WHERE updated_at = (SELECT MIN(updated_at) FROM cache)
    ''')
    one = c.fetchone()
    c.execute('''
        DELETE FROM cache WHERE hash = ?
              ''', (one[0],))
              
    conn.commit()
    conn.close()

    file_path = one[1]
    os.remove(file_path)
    
# update the file path in the cache database
import sqlite3

def update_file_path_in_cache(cache_db_path: str, hash: str, file_path: str):
    """
    Updates the file path in the cache database for a given hash.

    Args:
        cache_db_path (str): The path to the cache database.
        hash (str): The hash value to identify the record in the cache.
        file_path (str): The new file path to be updated in the cache.

    Returns:
        None
    """
    conn = sqlite3.connect(cache_db_path)
    c = conn.cursor()
    c.execute('''
        UPDATE cache SET file_path = ?, updated_at = CURRENT_TIMESTAMP WHERE hash = ?
    ''', (file_path, hash))
    conn.commit()
    conn.close()

# Function to get the file path from the cache database
def get_file_path_from_cache(cache_db_path: str, hash: str):
    """
    Retrieves the file path associated with the given hash from the cache database.

    Args:
        cache_db_path (str): The path to the cache database.
        hash (str): The hash value to search for in the cache.

    Returns:
        str: The file path associated with the given hash, or None if no matching hash is found.
    """
    conn = sqlite3.connect(cache_db_path)
    c = conn.cursor()
    c.execute('''
        SELECT file_path FROM cache WHERE hash = ?
    ''', (hash,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# Function to get the file size from the cache database
import sqlite3

def get_file_size_from_cache(cache_db_path: str, hash: str):
    """
    Retrieves the file size from the cache database based on the given hash.

    Args:
        cache_db_path (str): The path to the cache database.
        hash (str): The hash value used to retrieve the file size.

    Returns:
        int or None: The file size if found, None otherwise.
    """
    conn = sqlite3.connect(cache_db_path)
    c = conn.cursor()
    c.execute('''
        SELECT file_size FROM cache WHERE hash = ?
    ''', (hash,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None