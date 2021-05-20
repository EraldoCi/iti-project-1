import os
import sys
import struct
import pathlib
from typing import List, Dict
from compressor import Compressor
from decompressor import Decompressor
from utils.compressor.generate_graphs import generate_graphs
from utils.convert_time_to_seconds import convert_time_to_seconds
from utils.get_number_of_bytes_necessary_for_number import get_number_of_bytes_necessary_for_number


class LZW:
    def __init__(self):
        self.dictionary: dict
        self.reversed_dictionary: dict
        self.compressed_message: list = []

    def init_code_dictionary(self, k, file_type) -> Dict:
        dictionary_size = pow(2, k)
        dictionary = {}
        for i in range(dictionary_size):
            dictionary[i.to_bytes(
                get_number_of_bytes_necessary_for_number(i, file_type), 'big')] = i

        return dictionary

    def init_decode_dictionary(self, k, file_type) -> Dict:
        dictionary_size = pow(2, k)
        dictionary = {}

        for i in range(dictionary_size):
            dictionary[f'{i}'] = i.to_bytes(
                get_number_of_bytes_necessary_for_number(i, file_type), 'big')
        return dictionary

    def compress(self, data, file_name, k):
        compressed_file = open(
            f'./data/large_inputs/compression/{file_name}.bin', 'wb')

        compressor = Compressor(
            data=data, dictionary=self.init_code_dictionary(k=k, file_type=file_name.split(".")[-1]), k=k)
        compressor_response = compressor.run()

        elapsed_time = compressor_response["time"]
        self.compressed_message = compressor_response["message"]

        compressed_file.write(struct.pack(
            f">{'I'*len(self.compressed_message)}", *self.compressed_message))
        compressed_file.close()
        print(
            f"\nSIZE AFTER COMPRESSION: {os.path.getsize(f'./data/large_inputs/compression/{file_name}.bin')}")

        return {
            "Compression file size": os.path.getsize(f'./data/large_inputs/compression/{file_name}.bin'),
            "Elapsed Time": elapsed_time,
            "Indices": len(self.compressed_message)
        }

    def decompress(self, data, file_name, k):
        decompressor = Decompressor(
            data=data, dictionary=self.init_decode_dictionary(k=k, file_type=file_name.split(".")[-1]))
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
    _, file_name, command = sys.argv
    print(_, file_name, command)

    file_path: str = f'{root_path}/data/large_inputs/'

    lzw = LZW()

    if command == '-c':
        compressed_ratio_values, time_values, indices_used_values = [], [], []
        for dictionary_size in range(16, 17):
            with open(f"{file_path}/{file_name}", 'rb') as input_file:
                input_file_size = os.path.getsize(f"{file_path}/{file_name}")
                print(
                    f"SIZE BEFORE COMPRESSION: {input_file_size} | K = {dictionary_size}")
                compressed_data = lzw.compress(
                    input_file.read(), file_name, int(dictionary_size))
                print("INDICES ", compressed_data["Indices"])
                compressed_ratio = (
                    input_file_size * 8) / (compressed_data["Compression file size"] * dictionary_size)

                compressed_ratio_values.append(compressed_ratio)
                time_values.append(convert_time_to_seconds(
                    compressed_data["Elapsed Time"]))
                indices_used_values.append(compressed_data["Indices"])

        generate_graphs(compressed_ratio_values,
                        time_values, indices_used_values, file_name.split(".")[-1] == 'txt')

    elif command == '-d':
        with open(file=f"{file_path}/compression/{file_name}.bin", mode='rb') as input_file:
            file_bytes = input_file.read()
            print(len(file_bytes))
            bytes_to_string_list = struct.unpack(
                f">{'I'*(round(len(file_bytes)/4))}", file_bytes)
            decoded_message = lzw.decompress(
                data=bytes_to_string_list, k=int(16), file_name=file_name)

            print("ORIGINAL DECODED MESSAGE -> ", len(decoded_message))
            print("DECODED MESSAGE SLIGHTLY SMALLER -> ",
                  len(decoded_message[:-8]))
            file_for_decoded_message = open(
                file=f'./data/large_inputs/decompression/{file_name}',
                mode='wb'
            )
            file_for_decoded_message.write(
                decoded_message.encode('latin_1'))
            file_for_decoded_message.close()
