import sys
import pathlib


class LZW:
    def __init__(self, dictionary_size: int):
        self.dictionary_size = dictionary_size
        self.dictionary: dict
        self.reversed_dictionary: dict
        self.compressed_message: list = []

    def init_dictionary(self):
        return {(i.to_bytes(1, 'big')): i for i in range(256)}

    def init_reversed_dictiionary(self):
        return {i: (i.to_bytes(1, 'big')) for i in range(256)}

    def compress(self, data: str):
        compressed_file = open('compressed_file.txt.lzw', 'w')

        if isinstance(data, str):
            data = data.encode()

        self.dictionary: dict = self.init_dictionary()

        key, index, message_size = 256, 0, len(data)-1
        first_byte: bytes = data[0].to_bytes(1, 'big')
        next_byte: bytes

        dictionary_overflow = index + 1 > message_size

        while not dictionary_overflow:
            next_byte = data[index + 1].to_bytes(1, 'big')
            concatenated_words: bytes = data[index].to_bytes(
                1, 'big') + next_byte

            if concatenated_words in self.dictionary:
                next_index = 1

                while concatenated_words in self.dictionary:
                    next_index += 1
                    first_byte = concatenated_words
                    if index + next_index > message_size:
                        break

                    concatenated_words += data[index +
                                               next_index].to_bytes(1, 'big')

                self.compressed_message.append(
                    str(self.dictionary[first_byte]))
                index += len(first_byte)

            else:
                self.compressed_message.append(
                    str(self.dictionary[first_byte]))
                first_byte = next_byte
                index += len(first_byte)

            if key <= self.dictionary_size:
                key += 1
                self.dictionary[concatenated_words] = key

            dictionary_overflow = index + 1 > message_size

        separator: str = ','
        compressed_file.write(separator.join(self.compressed_message))
        compressed_file.close()

        return self.compressed_message

    def decompress(self, data):
        self.reversed_dictionary = self.init_reversed_dictiionary()
        return data

    def calculate_cr(self):
        return 'compression ratio value'


''' 
  Run lzw using the following comand for compressing:
  $ python lwz.py file_name.extension -c k_size 
  or for decompressing
  use: $ python lwz.py file_name.extension -d k_size 
'''
if __name__ == '__main__':

    root_path: str = pathlib.Path().absolute()
    _, file_name, command, dictionary_size = sys.argv
    try:
        dictionary_size = 2**int(dictionary_size)
    except:
        dictionary_size = 2**9

    file_path: str = f'{root_path}/data/{file_name}'
    lzw = LZW(dictionary_size)

    if command == '-c':
        with open(file_path, 'rb') as input_file:
            lzw.compress(input_file.read())
    elif command == '-d':
        with open(file_name, 'rb') as input_file:
            lzw.decompress(input_file.read())
