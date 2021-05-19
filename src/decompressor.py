from tqdm import tqdm


class Decompressor():
    def __init__(self, data, dictionary):
        self.data = data
        self.dictionary = dictionary

    def run(self):
        decoded_message, current_index = [], "256"
        first_letter = self.dictionary[str(self.data[0])]
        decoded_message.append(first_letter.decode('latin_1'))
        self.dictionary[current_index] = first_letter

        progress_bar = tqdm(total=len(self.data)-1, iterable=self.data,
                            desc='Decompression iterations and timing ⌚️')

        for i in range(1, len(self.data)):
            code = str(self.data[i])
            decoded_symbol = self.dictionary[code].decode(
                'latin_1')
            symbol = decoded_symbol[0] if len(
                decoded_symbol) else decoded_symbol

            self.dictionary[current_index] = self.dictionary[current_index] + \
                symbol.encode('latin_1')

            current_index = str(int(current_index) + 1)
            self.dictionary[current_index] = self.dictionary[code]

            decoded_message.append(
                self.dictionary[code].decode('latin_1'))

            progress_bar.update(1)

        progress_bar.close()
        return "".join(decoded_message)
