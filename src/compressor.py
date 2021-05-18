from utils.compressor.encode_data import encode_data
from utils.compressor.concat_symbols import concat_symbols
from utils.compressor.symbol_to_latin_encode import symbol_to_latin_encode
import struct


class Compressor():
    def __init__(self, data, dictionary):
        self.data = data.decode('ISO-8859-1')
        self.dictionary = dictionary

    def run(self):
        current_dictionary_value, idx, encoded_message = 256, 0, []

        while idx < len(self.data) - 1:
            symbol = encode_data(self.data, idx)
            next_symbol = encode_data(self.data, idx + 1)
            concatenated_symbols = concat_symbols(symbol, next_symbol)

            while concatenated_symbols in self.dictionary:
                idx += 1
                symbol = concatenated_symbols
                if idx < len(self.data) - 1:
                    if concatenated_symbols not in self.dictionary:
                        self.dictionary[concatenated_symbols] = current_dictionary_value
                        encoded_message.append(
                            symbol_to_latin_encode(symbol, self.dictionary))
                    concatenated_symbols = concat_symbols(
                        symbol, encode_data(self.data, idx + 1))
                else:
                    encoded_message.append(
                        symbol_to_latin_encode(symbol, self.dictionary))
                    break

            if concatenated_symbols not in self.dictionary:
                self.dictionary[concatenated_symbols] = current_dictionary_value
                current_dictionary_value += 1
                encoded_message.append(
                    symbol_to_latin_encode(symbol, self.dictionary))

                if idx == len(self.data) - 2:
                    encoded_message.append(
                        symbol_to_latin_encode(next_symbol, self.dictionary))

            idx += 1

        return encoded_message
