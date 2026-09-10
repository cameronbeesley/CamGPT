class Token:

    def __init__(self, value):
        self.value: str = value

    def __str__(self):
        return f"[{self.value}]"

class Word:

    def __init__(self, s: str, token_map: dict[str, Token]):
        self.tokens: list[Token] = []
        self.count: int = 1
        self.s: str = s
        self.token_map = token_map

        # tokenizing the original str
        for c in self.s:

            # the char already has a token
            if c in token_map:
                self.tokens.append(token_map[c])

            # the char doesn't have a token
            else:
                token = Token(c)
                self.tokens.append(token)
                token_map[c] = token

    @property
    def weight(self):
        return self.count**2

    def duplicate(self):
        '''
        Returns itself and increases the weight
        '''
        self.count += 1
        return self

    def get_pairs(self) -> list[tuple[Token, Token]]:
        '''
        Gets a list of the pairs
        '''
        pairs: list[tuple[Token, Token]] = []

        for i in range(len(self.tokens) - 1):
            pairs.append((self.tokens[i], self.tokens[i+1]))

        return pairs

    def merge_pair(self, pair: tuple[Token, Token], token_map: dict[str, Token]):
        '''
        Iterates through the tokens
        If pair is found
            - Create new token or find in token_map
            - Replace pair with new token
        '''
        length = len(self.tokens)
        token1, token2 = pair

        if length <= 1:
            return

        # iterating throught the tokens, excluding the last
        i = 0
        while i < length -1:

            # comparing the token to the first in the pair
            if self.tokens[i] == token1:

                # if succesful comparing it to the second in the pair
                if self.tokens[i+1] == token2:

                    # getting the new token
                    new_token = self.get_create_new_token(token1, token2, token_map)

                    # creating the new token list
                    try:
                        beginnning = self.tokens[:i]
                    except:
                        beginnning = []
                    try:
                        ending = self.tokens[i+2:]
                    except:
                        ending = []

                    self.tokens = beginnning + [new_token] + ending # this is the problem
                    length -= 1

            i += 1


    def get_create_new_token(self, token1: Token, token2: Token, token_map: dict[str, Token]) -> Token:
        '''
        Attempts to get the new token from map
        If not it will create the token and add to map
        '''
        new_token_str = token1.value + token2.value
        new_token = token_map.get(new_token_str, Token(new_token_str))
        return new_token


    def __str__(self):
        s = ""
        for token in self.tokens:
            s += str(token)
        return s


class Tokenizer:

    def __init__(self, max_merges: int):
        self.MAX_MERGES: int = max_merges
        self.word_map: dict[str, Word] = {}
        self.token_map: dict[str, Token] = {}

    def tokinize(self, text: str) -> list[Word]:
        words: list[Word] = self._seperate_text(text)
        self._merge(words)
        return words

    def _seperate_text(self, text: str) -> list[Word]:
        '''
        Seperates the text into a list of words - lists of tokens
        Tokens start off as letters
        Punctuation and new lines get their own word
        Does not handle numbers yet
        Weighting is done automatically - using .duplicate()
        '''
        words = []

        word = ""
        for c in text:

            # c is alphabetical
            if c.isalpha():
                word += c

            # c is a special character
            else:
                words.append(word)
                words.append(c)
                word = ""

        # ensure final word is added
        if word:
            words.append(word)

        word_objects = []
        for word in words:

            # word object already exists
            if word in self.word_map:
                word_object = self.word_map[word].duplicate()

            # word object does not already exist
            else:
                word_object = Word(word, self.token_map)
                self.word_map[word] = word_object

            word_objects.append(word_object)

        return word_objects

    def _merge(self, words: list[Word]):
        '''
        Merges common pairs
        Stops when reaches max merges or when no more merges can be made - no more common pairs
        '''
        # more efficient to use set for words now
        word_set = set(words)

        i = 0
        while i < self.MAX_MERGES:

            pair = self._get_pair(word_set)

            # if no more pairs - break
            if not pair:
                return

            self._merge_pair(word_set, pair)
            i += 1

    def _get_pair(self, words: set[Word]) -> tuple[Token, Token] | None:
        '''
        Finds the pairs in each word
        Stores the pairs in a dictionary
        Keeps track of most common pair and returns
        '''
        pair_weight_map: dict[tuple[Token, Token], int] = {}
        max_pair: tuple[Token, Token] | None = None
        max_weight: int = 0

        # iterating through the words
        for word in words:
            pairs = word.get_pairs()

            # iterating throught the pairs for the word
            for pair in pairs:

                # adding the pairs to the map. Adding the weight of the word
                pair_weight_map[pair] = pair_weight_map.get(pair, 0) + word.weight
                weight = pair_weight_map[pair]

                # storing the max pair
                if weight > max_weight:
                    max_pair = pair
                    max_weight = weight

        return max_pair

    def _merge_pair(self, words: set[Word], pair: tuple[Token, Token]):
        '''
        Iterates through the pairs and merges the token pair
        '''
        # iterating through the words
        for word in words:
            word.merge_pair(pair, self.token_map)
            


sentence = "Although Doctor Elena Vasquez-Chen had painstakingly reviewed nearly every line of Python code in the sprawling, labyrinthine codebase before dawn broke over the office, she still couldn't figure out why the API's rate-limiter—implemented using a sliding-window algorithm renowned for its elegance—kept throwing RateLimitExceeded errors whenever concurrent requests overwhelmed the fragile, underprovisioned server cluster, especially since her meticulously written unit tests (crafted in pytest, complete with mocked timestamps and painstakingly isolated edge cases) had sailed through the CI/CD pipeline running on AWS's notoriously finicky us-east-1 region, leaving her equal parts bewildered, exasperated, and quietly impressed by the sheer, almost mischievous unpredictability of distributed systems!"
tokenizer = Tokenizer(1000)
words = tokenizer.tokinize(sentence)
tokens = []
for word in words:
    tokens += word.tokens
for token in tokens:
    print(token, end='')
print()
print(f"Orginal length: {len(sentence)}, Compressed length: {len(tokens)}")


        

            

            


        

