class Contact:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self) -> str:
        return f"{self.name}: {self.number}"

class Node:
    def __init__(self, key, value):
        self.key = key          
        self.value = value      
        self.next = None        


class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.data = [None] * size 

    def hash_function(self, key):
        total = 0
        for i, ch in enumerate(key):
            total += (i + 1) * ord(ch)
        return total % self.size

    def insert(self, key, number):
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
        idx = self.hash_function(key)
        cur = self.data[idx]
        while cur is not None:
            if cur.key == key:
                return cur.value
            cur = cur.next
        return None

    def print_table(self):
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


# Test
if __name__ == "__main__":
    table = HashTable(10)

    print("Initial table:")
    table.print_table()

    # contacts
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
feel slow as data gets bigger. Balanced trees offer O(log n) operations and keep order,
which is great for range queries or ordered output, but they’re more complex. For a
contact manager focused on quick “find by name,” a hash table is a very good fit.
"""
