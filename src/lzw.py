import sys
import pathlib
from typing import List, Dict
from compressor import Compressor
from decompressor import Decompressor
import timeit
import os
import struct
import base64


class LZW:
    def __init__(self, dictionary_size: int):
        self.dictionary_size = dictionary_size
        self.dictionary: dict
        self.reversed_dictionary: dict
        self.compressed_message: list = []

    def init_code_dictionary(self) -> Dict:
        return {(i.to_bytes(1, 'big')): i for i in range(256)}

    def init_decode_dictionary(self) -> Dict:
        return {f'{i}': (i.to_bytes(1, 'big')) for i in range(256)}

    def compress(self, data, file_name):
        compressed_file = open(f'./data/test/{file_name}.bin', 'wb')

        compressor = Compressor(
            data=data, dictionary=self.init_code_dictionary())
        self.compressed_message = compressor.run()

        compressed_file.write(struct.pack(
            f">{'I'*len(self.compressed_message)}", *self.compressed_message))
        compressed_file.close()
        print(
            f"\nSIZE AFTER COMPRESSION: {os.path.getsize(f'./data/test/{file_name}.bin')}")

        return "Finished Compression 🗜"

    def decompress(self, data):
        decompressor = Decompressor(
            data=data, dictionary=self.init_decode_dictionary())
        decoded_message = decompressor.run()

        return decoded_message

    def calculate_ratio_compression(self):
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
    print(_, file_name, command, dictionary_size)
    try:
        dictionary_size = 2**int(dictionary_size)
    except:
        dictionary_size = 2**9

    file_path: str = f'{root_path}/data/large_inputs/{file_name}'

    lzw = LZW(dictionary_size)

    if command == '-c':
        with open(file_path, 'rb') as input_file:
            print(f"SIZE BEFORE COMPRESSION: {os.path.getsize(file_path)}")
            lzw.compress(input_file.read(), file_name)

    elif command == '-d':
        with open(file=file_path, mode='rb') as input_file:
            file_bytes = input_file.read()
            print(len(file_bytes))
            bytes_to_string_list = struct.unpack(
                f">{'I'*(round(len(file_bytes)/4))}", file_bytes)
            decoded_message = lzw.decompress(data=bytes_to_string_list)
            print(decoded_message)
            exit()
            file_for_decoded_message = open(
                f'{root_path}/data/test/decompress-{file_name}', 'wb')
            file_for_decoded_message.write(base64.b64decode(decoded_message))
            file_for_decoded_message.close()
