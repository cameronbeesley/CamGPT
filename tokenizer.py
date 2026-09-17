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

    def _find_mcp(self, text: list[list[int]]) -> tuple[int, int] | None:
        '''
        Loops through all the words and characters and stores the count of each pair
        Uses a dictionary for the storing
        Returns most common pair or none if no more pairs
        '''
        # counting the pairs
        pairs: dict[tuple[int,int],int] = {}
        for chunk in text:
            for i in range(len(chunk)-1):
                pair = (chunk[i], chunk[i+1])
                pairs[pair] = pairs.get(pair, 0) + 1

        # finding most common pair
        mcp: tuple[int,int] | None = None
        mcp_count = 0
        for pair, count in pairs.items():
            if count >= mcp_count:
                mcp = pair
                mcp_count = count

        return mcp

    def _merge(self, text: list[list[int]], pair: tuple[int, int], id: int):
        '''
        Loops through the words and merges the pair when found
        id is the id of the new token
        '''
        i = 0
        while i < len(text):
            chunk = text[i]
            new_chunk: list[int] = []
            j = 0
            length = len(chunk)
            while j < length:
                if j < length - 1 and (chunk[j],chunk[j+1]) == pair: # pair is a match
                    new_chunk.append(id)
                    j += 2 # skips the second token in the pair
                else:
                    new_chunk.append(chunk[j])
                    j += 1
            text[i] = new_chunk
            i += 1

        

tokenizer = Tokenizer()

text = "Once upon a time, long      long ago... There was a man. This man's name was Bob!"
text = "ah ah ab"

chunks = tokenizer._seperator(text)
print("Seperated chuncks")
print(chunks)

encoded_chunks = tokenizer._text_encoder(chunks)
print("Encoded chunks")
print(encoded_chunks)

mcp = tokenizer._find_mcp(encoded_chunks)
print("mcp")
print(mcp)

if mcp:
    print("merging")
    tokenizer._merge(encoded_chunks, mcp, 1000)

print("encoded chunks after merge")
print(encoded_chunks)

# decoded_chunks = tokenizer._text_dencoder(encoded_chunks)
# print("decoded chunks after merge")
# print(decoded_chunks)



