from octopus.nlp import is_word, tokenize_text, get_frequent_tokens


class TestIsWord:
    def test_is_word(self):
        words = ["Sparta", "ok", "R2D2" "beagels", "Jackie Chan", "I"]
        assert all(is_word(word) for word in words)

    def test_is_not_word(self):
        not_words = ["&", "9000", "?"]
        assert all(not is_word(elem) for elem in not_words)


class TestTokenizeText:
    cases = [
        {"text": "This is Sparta!", "tokens": ["sparta"]},
        {
            "text": "Hold my 2 beers please",
            "tokens": ["hold", "beers", "please"],
        },
    ]

    def test_tokenize_text(self):
        for case in self.cases:
            tokenized = list(tokenize_text(case["text"]))
            tokenized.sort()
            case["tokens"].sort()
            assert tokenized == case["tokens"]


class TestGetFrequenTokens:
    cases = [
        {
            "text": "This this this is Sparta Sparta",
            "counts": [{"token": "sparta", "frequency": 2}],
        },
        {
            "text": "Sentences sentences I need more more sentences",
            "counts": [
                {"token": "sentences", "frequency": 3},
                {"token": "need", "frequency": 1},
            ],
        },
    ]

    def test_get_frequent_tokens(self):
        for case in self.cases:
            counts = get_frequent_tokens(case["text"], 50)
            assert case["counts"] == counts

    def test_ntop(self):
        for case in self.cases:
            counts = get_frequent_tokens(case["text"], 1)
            assert len(counts) == 1
