





"""
DESCRIPTION:
    This program attempts to implement huffman coding to compress text. The program takes in a .txt file
address, implements the algorithms necessary to compress it vai huffman coding, prints out a dictionary to show how
the characters would be translated in binary post compression, and prints out how much of the file can be theoretically
compressed using this technique.

NOTE:
    The original intention with the program was to generate a whole new file to store the compressed version of the
text, and be able to decompress it. However, I, Aritra Roy Mazumder solemnly acknowledge that I don't know how to do
that and could not finish the program due to fast approaching AP exams(Pray for me, I'm scared)

INSTRUCTIONS:
    Scroll down, kindly ignore my lack of formal coding conventions, locate line 235,
replace ""replace_with_file_name.txt"" in  ==> the_string = get_string_from_file("replace_with_file_name.txt") with
the name of the file which you must have in the same folder. Ofcourse you guys know how to do it with a path too.


"""
# Class to create nodes that will go into the huffman tree


class Node(object):
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.binary_signature = None
        self.head = None
        self.left = None
        self.right = None

    def __str__(self):
        ch = "None"
        bin_sig = "None"
        if self.char:
            ch = self.char
        if self.binary_signature:
            bin_sig = self.binary_signature

        return "(" + ch + ", " + str(self.freq) + ", " + bin_sig + ")"

# the class to make individual huffman trees


class HuffTree(object):
    def __init__(self, node_list):
        self.node_list = node_list
        self.root = Node(None, self.sum_of_freq())
        self.original_node_list = node_list.copy()
        self.build_heap()
        self.binary_assignment()
        self.binary_translation_dictionary = self.build_translation_dictionary()

    # builds the huffman tree
    def build_heap(self):
        while len(self.node_list) > 2:
            first_node_holder = self.node_list[self.lowest_freq_index()]
            self.node_list.remove(first_node_holder)
            second_node_holder = self.node_list[self.lowest_freq_index()]
            self.node_list.remove(second_node_holder)

            third_node_holder = Node(None, first_node_holder.freq + second_node_holder.freq)
            first_node_holder.head = third_node_holder
            second_node_holder.head = third_node_holder
            third_node_holder.left = first_node_holder
            third_node_holder.right = second_node_holder
            self.node_list.append(third_node_holder)

        self.node_list[0].head = self.root
        self.node_list[1].head = self.root
        self.root.left = self.node_list[0]
        self.root.right = self.node_list[1]

    # creates the dictionary to translate the characters into binary
    def build_translation_dictionary(self):
        dict_bin = {}
        for x in self.original_node_list:
            dict_bin[x.char] = x.binary_signature
        return dict_bin
        
    # returns index of node with lowest freq in node_list
    
    def lowest_freq_index(self):
        lowest_frequency_index = 0
        for x in range(len(self.node_list)):
            if self.node_list[x].freq < self.node_list[lowest_frequency_index].freq:
                lowest_frequency_index = x
        return lowest_frequency_index

    # returns the sum of the frequencies of the nodes in the node_list
    
    def sum_of_freq(self):
        counter = 0
        for x in self.node_list:
            counter += x.freq
        return counter

    def __str__(self):
        return self.pre_order_print(self.root, "")

    # got this from the internet for testing purposes
    def pre_order_print(self, start, traversal):
        if start:
            traversal += (str(start) + "||")
            traversal = self.pre_order_print(start.left, traversal)
            traversal = self.pre_order_print(start.right, traversal)
        return traversal

    # assigns the "binary signature" for all nodes (IDK what its actually called)
    def binary_assignment(self):
        self.pre_order_binary_assignment(self.root, "")

    # recursively goes through the nodes in the tree and assigns them a "binary signature"
    def pre_order_binary_assignment(self, current_node, binary_signature):
        if not (current_node.left and current_node.right):
            current_node.binary_signature = binary_signature
        else:
            self.pre_order_binary_assignment(current_node.left, binary_signature + "0")
            self.pre_order_binary_assignment(current_node.right, binary_signature + "1")


# merge sort algorithm that takes a list of ints and returns list sorted in ascending order using a merge sort algorithm

def merge_sort(working_list):

    if len(working_list) > 1:
        mid_section = len(working_list)//2
        sublist_left = working_list[:mid_section]
        sublist_right = working_list[mid_section:]

        merge_sort(sublist_left)
        merge_sort(sublist_right)

        index_left = 0
        index_right = 0
        index = 0

        while index_left < len(sublist_left) and index_right < len(sublist_right):

            if sublist_left[index_left] <= sublist_right[index_right]:
                working_list[index] = sublist_left[index_left]

                index_left += 1
                index += 1

            else:
                working_list[index] = sublist_right[index_right]
                index_right += 1
                index += 1

        while index_left < len(sublist_left):
                working_list[index] = sublist_left[index_left]
                index_left += 1
                index += 1

        while index_right < len(sublist_right):
                working_list[index] = sublist_right[index_right]
                index_right += 1
                index += 1

    return working_list


# Takes a string and returns a frequency dictionary

def create_frequency_dictionary(text):
    freq_dict = {}
    for i in text:
        if i not in freq_dict.keys():
            freq_dict[i] = 1
        else:
            freq_dict[i] += 1
    return freq_dict


# takes a dictionary and returns a list containing all the values
# needed this cuz dictionary.values() returns an non iterable data type

def get_list_of_values(dictionary):
    lst = []
    for i in dictionary.values():
        lst.append(i)
    return lst


# takes the sorted list of frequencies and makes a sorted list of values that line up in index with the freq list

def get_sorted_list_of_conjugate_chars(freq, dictionary):
    value_lst = []
    for i in freq:
        for j in dictionary.keys():
            if dictionary[j] == i:
                value_lst.append(j)
                del dictionary[j]
                break
    return value_lst


# creates a list of nodes from a list of characters and a list of their conjugate frequencies
def create_list_of_nodes(freq_list, char_list):
    lst_of_nodes = []
    for i in range(len(freq_list)):
        lst_of_nodes.append(Node(char_list[i], freq_list[i]))
    return lst_of_nodes


# takes a string and produces the list of nodes from it
def produce_node_lists(sample_str):
    frequency_dictionary = create_frequency_dictionary(sample_str)
    list_of_frequencies = get_list_of_values(frequency_dictionary)
    sorted_list_of_frequencies = merge_sort(list_of_frequencies.copy())
    sorted_list_of_conjugate_chars = get_sorted_list_of_conjugate_chars(sorted_list_of_frequencies.copy(),
                                                                        frequency_dictionary)
    list_of_nodes = create_list_of_nodes(sorted_list_of_frequencies, sorted_list_of_conjugate_chars)
    return list_of_nodes


# takes the name of a .txt file in form "sample_file.txt" and returns the contents of the file in a string
def get_string_from_file(name_of_file):
    some_string = ""
    with open(name_of_file, "r") as f:
        some_string += f.read()
    return some_string


"""
replace "replace_with_file_name.txt" with name of your file
"""
the_string = get_string_from_file("replace_with_file_name.txt")
huffman_tree = HuffTree(produce_node_lists(the_string))

print("Binary Translation Dictionary:")
print(huffman_tree.binary_translation_dictionary)

# assumes negligible space is required to store whatever .txt files need to store outside of its contents
org_bin_len = len(the_string) * 8
print("Original bits: " + str(org_bin_len))

translation_dict = huffman_tree.binary_translation_dictionary

binary_string = ""
for unique_global_x in the_string:
    binary_string += str(translation_dict[unique_global_x])
com_bin_len = len(binary_string)
print("New number of bits: " + str(com_bin_len))

# assumes negligible space required to store the dictionary and whatever .txt files need to store outside of the content
print("Percentage theoretically compressible: " + str(round(((org_bin_len - com_bin_len) / org_bin_len) * 100, 1)) +
      " %")
