from linkedlist import DoublyLinkedList

# '''
# Linked List hash table key/value pair
# '''
class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''
    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity
        self.load = 0.0
        self.resizing = False


    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key)


    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        spec = 5381
        for char in key:
            spec = (( spec << 5 ) + spec) + ord(char)

        return spec & 0xFFFFFFFF


    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash(key) % self.capacity


    def insert(self, key, value):
        '''
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Fill this in.
        '''
        pos = self._hash_mod(key)

        if self.storage[pos] is None:
            linked = DoublyLinkedList()

            self.storage[pos] = linked
            linked.add_to_tail( (key, value) )

            self.load = self.load + 1
            self.autoResize()
            
        else:
            currentNode = self.storage[pos].head
            found = False

            while currentNode is not None:
                if currentNode.value[0] == key:
                    currentNode.value = (key, value)
                    found = True
                    break

                currentNode = currentNode.next

            if found is False:
                self.storage[pos].add_to_tail( (key, value) )
        

    def autoResize(self):
        if self.resizing is False and self.load > 0:
                if self.capacity / self.load < 0.2:
                    self.resize(self.capacity // 2)
                elif self.capacity / self.load > 0.7:
                    self.resize(self.capacity * 2)

    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        '''
        pos = self._hash_mod(key)

        if self.storage[pos] is not None:
            currentNode = self.storage[pos].head

            while currentNode is not None:
                if currentNode.value[0] == key:
                    self.storage[pos].delete(currentNode)

                    if self.storage[pos].head is None:
                        self.load = self.load - 1

                    self.autoResize()

                    return
                
                currentNode = currentNode.next

        print("Key not found")


    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        pos = self._hash_mod(key)

        if self.storage[pos] is not None:
            currentNode = self.storage[pos].head

            while currentNode is not None:
                if currentNode.value[0] == key:
                    return currentNode.value[1]
                
                currentNode = currentNode.next

        return None

    def resize(self, newCapacity = None):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Fill this in.
        '''

        if newCapacity == None:
            newCapacity = self.capacity * 2

        newTable = HashTable(newCapacity)

        newTable.resizing = True
        self.resizing = True

        for i in self.storage:
            if i is not None:
                currentNode = i.head

                while currentNode is not None:
                    key = currentNode.value[0]
                    value = currentNode.value[1]

                    newTable.insert(key, value)

                    currentNode = currentNode.next

        self.capacity = newTable.capacity
        self.storage = newTable.storage
        self.resizing = False

        del newTable

if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")
