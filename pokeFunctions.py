import os
import csv
import pokepath
import imagehash

def pokeReadHashTable(hashList): 
    # Check for previously written hash table
        if os.path.exists(pokepath.file_HashTable):

            # Open table
            with open(pokepath.file_HashTable, mode='r') as file_csv:
                reader_obj = csv.reader(file_csv)
                for row in reader_obj:

                    if row[1] != "0":
                        hashList.append(imagehash.hex_to_hash(row[1]))
            print(f"hashData uploaded; found {len(hashList)} hashes")
        else:
            print("Hash file not found")