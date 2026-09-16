class Tokenizer:

    def __init__(self):
        pass

    def _bit_encoder(self, text: str) -> list[int]:
        '''
        Convert characters to 8 bit intergers
        Using .encode
        '''
        return list(text.encode("utf-8"))

    def _bit_decoder(self, ids: list[int]) -> str:
        '''
        Convert the list of 8 bit intergers to a string
        '''
        return(bytes(ids).decode("utf-8"))

tokenizer = Tokenizer()
print(tokenizer._bit_encoder("Hello"))

