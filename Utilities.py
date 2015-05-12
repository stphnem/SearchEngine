import string


class Utilities():


    def tokenize_file(file):
        """
        :param file: takes in a path to a file
        :return: list of string tokens of words in file

        Use python map translates to replace all punctuation and strip white space and lower the type-case and return the words in a list
        """
        remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
        lines = [line.strip().lower().translate(remove_punctuation_map) for line in open(file)]
        words = []
        for line in lines:
            words.extend(line.split())
        return words


    def print_frequencies(frequencies):
        """
        :param frequencies: takes in a list of frequency objects
        :return: Nothing
        Prints the frequency objects and their counts using string formatting
        """
        output = "\nTotal {} count: {}\nUnique {} count: {}\n"
        if not frequencies:
            print(output.format("items",0,"items",0))
        else:
            is_2_gram = len(frequencies[0].get_text().split()) > 2
            if is_2_gram:
                print(output.format("2-gram", (sum(f.get_frequency() for f in frequencies)), "2-gram", len(frequencies)))
            else:
                print(output.format("item", (sum(f.get_frequency() for f in frequencies)), "item", len(frequencies)))
            for f in frequencies:
                print("{0:30s} {1:<3d}".format(f.get_text(), f.get_frequency()))

  
