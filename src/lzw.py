import sys


class LZW:
    def __init__(self, k_size: int):
        self.k_size = k_size
        self.dictionary: dict = self.init_dictionary()
        self.compressed_message: list = []

    def init_dictionary(self):
        return {(i.to_bytes(1, 'big')): i for i in range(256)}

    def compress(self, data: str):
        if isinstance(data, str):
            data = data.encode()

        key: int = 256
        first_byte: bytes = data[0].to_bytes(1, 'big')
        starting_index: int = 0
        next_byte: bytes

        dictionary_overflow = starting_index + 1 > len(data)-1

        while not dictionary_overflow:
            next_byte = data[starting_index + 1].to_bytes(1, 'big')
            concatenated_words: bytes = data[starting_index].to_bytes(
                1, 'big') + next_byte

            if concatenated_words in self.dictionary:
                next_index = 1

                while concatenated_words in self.dictionary or dictionary_overflow:
                    next_index += 1
                    first_byte = concatenated_words
                    dictionary_overflow = starting_index + \
                        next_index > len(data)-1

                    concatenated_words += data[starting_index +
                                               next_index].to_bytes(1, 'big')

                self.compressed_message.append(self.dictionary[first_byte])
                starting_index += len(first_byte)

            else:
                self.compressed_message.append(self.dictionary[first_byte])
                first_byte = next_byte
                starting_index += len(first_byte)

            if key <= self.k_size:
                key += 1
                self.dictionary[concatenated_words] = key

            dictionary_overflow = starting_index + 1 > len(data)-1

        print(self.compressed_message)
        return self.compressed_message

    def decompress(self, data):
        return data

    def calculate_cr(self):
        return 'compression ratio value'


''' 
  Run lzw using:
  $ python lwz.py file_name.extension -c k_size 
  or 
  use: $ python lwz.py file_name.extension -d k_size 
  by default k_size = 9
'''
if __name__ == '__main__':

    k_size: int
    try:
        k_size = 2**int(sys.argv[2])
    except:
        k_size = 2**9

    lzw = LZW(k_size)

    if sys.argv[2] == '-c':
        with open(sys.argv[1], 'rb') as input_file:
            lzw.compress(input_file.read())
    elif sys.argv[2] == '-d':
        with open(sys.argv[1], 'rb') as input_file:
            lzw.decompress(input_file.read())
