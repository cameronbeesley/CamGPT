import regex

class Tokenizer:

    def __init__(self):
        pass

    def _chunk_encoder(self, text: str) -> list[int]:
        '''
        Convert characters to 8 bit intergers
        Using .encode
        '''
        return list(text.encode("utf-8"))

    def _chunk_decoder(self, ids: list[int]) -> str:
        '''
        Convert the list of 8 bit intergers to a string
        '''
        return(bytes(ids).decode("utf-8"))

    def _seperator(self, text: str) -> list[str]:
        '''
        Seperates the text into "chuncks" - list of smaller strings
        Will regex with the GPT-2 pattern
        '''
        pattern = regex.compile(r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""")
        chunks = regex.findall(pattern, text)
        return chunks

    def _text_encoder(self, raw_chunks: list[str]) -> list[list[int]]:
        '''
        Takes the raw chunks and encodes them
        Returns a list of encoded chucks
        '''
        encoded_chunks: list[list[int]] = []
        for chunk in raw_chunks:
            encoded_chunks.append(self._chunk_encoder(chunk))
        return encoded_chunks

    def _text_dencoder(self, encoded_chunks: list[list[int]]) -> list[str]:
            '''
            Takes the encoded chunks and dencodes them
            Returns a list of dencoded chucks
            '''
            dencoded_chunks: list[str] = []
            for chunk in encoded_chunks:
                dencoded_chunks.append(self._chunk_decoder(chunk))
            return dencoded_chunks

tokenizer = Tokenizer()

text = "Once upon a time, long      long ago... There was a man. This man's name was Bob!"

chunks = tokenizer._seperator(text)
print(chunks)

encoded_chunks = tokenizer._text_encoder(chunks)
print(encoded_chunks)

dencoded_chunks = tokenizer._text_dencoder(encoded_chunks)
print(dencoded_chunks)

