import sys
from stats import get_num_words, get_char_freq, sort_dict

def get_book_test(file_path: str) -> str:
    with open(file_path) as f:
        file_contents = f.read()

    return file_contents

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <path_to_book>")
        sys.exit(1)

    corpus_path = sys.argv[1]

    text = get_book_test(corpus_path)

    num_words = get_num_words(text)

    char_dict = get_char_freq(text)

    char_dict = sort_dict(char_dict)
    print("============ BOOKBOT ============")
    print(f"Analyzing book found at {corpus_path}...")
    print("----------- Word Count ----------")
    print(f"Found {num_words} total words")
    print("--------- Character Count -------")

    for char in char_dict:
        count = char_dict[char]
        if char.isalpha():
            print(f"{char}: {count}")

    print("============= END ===============")

main()
