from Trie import Trie, TrieNode

def get_calibration_values(filename):
    with open(filename) as f:
        lines = [line[:-1] for line in f.readlines()]

    replacements = {
        "one" : "1",
        "two" : "2",
        "three" : "3",
        "four" : "4",
        "five" : "5",
        "six" : "6",
        "seven" : "7",
        "eight" : "8",
        "nine" : "9",
        "zero" : "0",
    }

    trie = Trie(replacements.keys())

    def get_decimals(string: str):
        return [c for c in string if c.isdigit()]

    def get_word(string, start, trie: Trie):
        current :TrieNode = trie._root

        for i in range(start, len(string)):
            c = string[i]

            if c in current.next:
                current = current.next[c]

                if current.eow:
                    return current.eow, i 
            else:
                return None, -1

        return None, -1

    def convert(string: str, trie: Trie):
        result, word_end = [], -1

        for i, c in enumerate(string):
            if i < word_end:
                continue

            word, word_end = get_word(string, i, trie)
            result.append(replacements[word] if word else c)

        return ''.join(result)

    calibration_values = []
    for line in lines:
        converted = convert(line, trie)

        decimals = get_decimals(converted)

        pair = int(f"{decimals[0]}{decimals[-1]}")

        print(f"{line}\n{converted} --> {pair}\n")

        calibration_values.append(pair)

    return sum(calibration_values)

main_file = "calibration_document.txt"
test_file = "test2.txt"
another_one = "test3.txt"

print(get_calibration_values(main_file))