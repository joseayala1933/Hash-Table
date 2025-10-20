class Contact:
    '''
    Contact class to represent a contact with a name and number.
    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    '''
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self) -> str:
        return f"{self.name}: {self.number}"


class Node:
    '''
    Node class to represent a single entry in the hash table.
    Attributes:
        key (str): The key (name) of the contact.
        value (Contact): The value (Contact object) associated with the key.
        next (Node): Pointer to the next node in case of a collision.
    '''
    def __init__(self, key, value):
        self.key = key          
        self.value = value      
        self.next = None        


class HashTable:
    '''
    HashTable class to represent a hash table for storing contacts.
    Attributes:
        size (int): The size of the hash table.
        data (list): The underlying array to store linked lists for collision handling.
    Methods:
        hash_function(key): Converts a string key into an array index.
        insert(key, value): Inserts a new contact into the hash table (or updates number).
        search(key): Searches for a contact by name (returns Contact or None).
        print_table(): Prints the structure of the hash table.
    '''
    def __init__(self, size=10):
        self.size = size
        self.data = [None] * size 

    def hash_function(self, key):
        """
        Very simple string hash: weighted sum of character codes.
        Not perfect, but easy to understand.
        """
        total = 0
        for i, ch in enumerate(key):
            total += (i + 1) * ord(ch)
        return total % self.size

    def insert(self, key, number):
        """
        Add or update a contact. Uses separate chaining.
        If key already exists, update its number.
        """
        idx = self.hash_function(key)
        head = self.data[idx]
        if head is None:
            self.data[idx] = Node(key, Contact(key, number))
            return

        cur = head
        prev = None
        while cur is not None:
            if cur.key == key:
                cur.value.number = number
                return
            prev = cur
            cur = cur.next

        prev.next = Node(key, Contact(key, number))

    def search(self, key):
        """
        Return the Contact with matching name, or None if not found.
        """
        idx = self.hash_function(key)
        cur = self.data[idx]
        while cur is not None:
            if cur.key == key:
                return cur.value
            cur = cur.next
        return None

    def print_table(self):
        """
        Print each bucket and its chain (if any).
        Format tries to match the assignment examples.
        """
        for i in range(self.size):
            chain = self.data[i]
            if chain is None:
                print(f"Index {i}: Empty")
            else:
                parts = []
                cur = chain
                while cur is not None:
                    parts.append(f"- {cur.value}")
                    cur = cur.next 
                print(f"Index {i}: {' '.join(parts)}")


# ====== Simple Tests / Demo ======
if __name__ == "__main__":
    table = HashTable(10)

    print("Initial table:")
    table.print_table()

    # Add your five contacts
    table.insert("Juan", "505-123-1111")
    table.insert("Jose", "505-123-2222")
    table.insert("Maria", "505-123-3333")
    table.insert("Nataly", "505-123-4444")
    table.insert("Gabriel", "505-123-5555")

    print("\nAfter inserting contacts:")
    table.print_table()

    found = table.search("Nataly")
    print("\nSearch result:", found)  # should show Nataly’s info

    #collison test
    table.insert("Naty", "505-999-0000")  # may collide with Nataly
    print("\nAfter inserting possible collision (Naty):")
    table.print_table()

    table.insert("Jose", "505-777-7777")
    print("\nAfter updating Jose's number:")
    table.print_table()

    print("\nSearch for Diego (should be None):", table.search("Diego"))


"""
Design memo
Why a hash table for fast lookups?
A hash table gives  O(1) time for inserts and searches by converting a key
( a contacts name) into an array index using a hash function. Instead of scanning
through every contact like a list would, the program jumps directly to a small bucket,
which is much faster once the table grows.

I used separate chaining with a tiny linked list in each bucket. If two names hash to the
same index, the new contact is appended to the chain at that index. When inserting, the
code first walks the chain to check if the exact key already exists; if it does, we simply
update the stored phone number. This keeps behavior predictable and avoids duplicate
entries for the same name. The hash function itself is intentionally simple (a weighted
sum of character codes). It’s not industrial-strength, but it’s easy to read and works
well enough for a class project with hundreds of entries.

When to choose a hash table over a list or tree
Choose a hash table when you care most about average O(1) lookups/updates by key and you
don’t need ordered traversal of keys. A list is simpler but gives O(n) search, which can
feel slow as data grows. Balanced trees offer O(log n) operations and keep sorted order,
which is great for range queries or ordered output, but they’re more complex. For a
contact manager focused on quick “find by name,” a hash table is a very practical fit.
"""
