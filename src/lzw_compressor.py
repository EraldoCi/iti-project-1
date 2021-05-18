def lzw_compressor(data):
    current_dictionary_value, idx, encoded_message = 256, 0, []
    encode_dictionary = {(i.to_bytes(1, 'big')): i for i in range(256)}

    while idx < len(data) - 1:
        symbol = encode_data(data, idx)
        next_symbol = encode_data(data, idx + 1)
        concatenated_symbols = concat_symbols(symbol, next_symbol)

        while concatenated_symbols in encode_dictionary:
            idx += 1
            symbol = concatenated_symbols
            if idx < len(data) - 1:
                if concatenated_symbols not in encode_dictionary:
                    encode_dictionary[concatenated_symbols] = current_dictionary_value
                    encoded_message.append(
                        symbol_to_latin_encode(symbol, encode_dictionary))
                concatenated_symbols = concat_symbols(
                    symbol, encode_data(data, idx + 1))
            else:
                encoded_message.append(
                    symbol_to_latin_encode(symbol, encode_dictionary))
                break

        if concatenated_symbols not in encode_dictionary:
            encode_dictionary[concatenated_symbols] = current_dictionary_value
            current_dictionary_value += 1
            encoded_message.append(
                symbol_to_latin_encode(symbol, encode_dictionary))
        idx += 1

    return encoded_message


def encode_data(data, idx):
    return data[idx].encode('latin-1')


def symbol_to_latin_encode(symbol, dictionary):
    return dictionary[symbol]


def concat_symbols(symbol, next_symbol):
    print(symbol, next_symbol, symbol + next_symbol)
    return symbol + next_symbol


lzw_compressor('Eu não gosto do Gusvãozão')
