def get_num_words(text: str) -> int:
    list_of_words = text.split()

    return len(list_of_words)

def get_char_freq(text: str) -> dict[str, int]:
    char_counts = {}

    for character in text.lower():
        if character in char_counts:
            char_counts[character] += 1
        else:
            char_counts[character] = 1

    return char_counts

def sort_dict(dictionary):
    sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse = True))

    return sorted_dict
