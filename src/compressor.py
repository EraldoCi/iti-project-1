from utils.compressor.encode_data import encode_data
from utils.compressor.concat_symbols import concat_symbols
from utils.compressor.symbol_to_latin_encode import symbol_to_latin_encode
from tqdm import tqdm


class Compressor():
    def __init__(self, data, dictionary):
        self.data = data.decode('ISO-8859-1')
        self.dictionary = dictionary

    def run(self):
        message_size = len(self.data)-1
        if message_size < 1:
            return "There is no content to compress!"
        current_dictionary_value, idx, encoded_message = 256, 0, []

        progress_bar = tqdm(total=message_size, iterable=self.data,
                            desc='Compression iterations and timing ⏰')

        while idx < message_size:
            symbol = encode_data(self.data, idx)
            next_symbol = encode_data(self.data, idx + 1)
            concatenated_symbols = concat_symbols(symbol, next_symbol)

            while concatenated_symbols in self.dictionary:
                idx += 1
                progress_bar.update(1)
                symbol = concatenated_symbols
                if idx < message_size:
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
                if idx == message_size - 1:
                    encoded_message.append(
                        symbol_to_latin_encode(encode_data(self.data, idx + 1), self.dictionary))

            idx += 1

            progress_bar.update(1)

        progress_bar.close()

        return encoded_message
