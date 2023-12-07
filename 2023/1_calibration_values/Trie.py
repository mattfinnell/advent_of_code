class TrieNode:
    def __init__(self):
        self.next = {}
        self.eow = None


class Trie:
    def __init__(self, dictionary):
        self._root = TrieNode()

        for word in dictionary:
            self.insert(word)

    def search(self, word) -> bool:
        current: TrieNode = self._root

        for c in word:
            if c not in current.next:
                return False

            current = current.next[c]

        return current.eow 

    def insert(self, word):
        current = self._root
        for c in word:
            if c not in current.next:
                current.next[c] = TrieNode()

            current = current.next[c]

        current.eow = word

