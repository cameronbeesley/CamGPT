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

tokenizer = Tokenizer()

text = "Once upon a time, long      long ago... There was a man. This man's name was Bob!"

chunks = tokenizer._seperator(text)
print(chunks)

ids = tokenizer._chunk_encoder("Hello")
print(ids)
s = tokenizer._chunk_decoder(ids)
print(s)

