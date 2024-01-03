import re

import opusfilter


class CountSentensesFilter(opusfilter.FilterABC):
    """Сравнение предложений в строке"""
    score_direction = opusfilter.CLEAN_LOW

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def count_sentenses(self, sentence: str) -> int:
        """Количество предложений в строке"""
        length = len(re.split('[!.?]+', sentence))
        return length

    def score(self, pairs: list) -> list:
        for pair in pairs:
            yield [self.count_sentenses(sentence) for sentence in pair]

    def accept(self, score: list) -> bool:
        if score[0] == score[1]:
            return True
        else:
            return False


class CountWordsFilter(opusfilter.FilterABC):
    """Проверка на превышение слов в переводе более чем на 20"""
    score_direction = opusfilter.CLEAN_LOW

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

    def count_words(self, sentence: str) -> int:
        """Количество слов в строке"""
        length = len(sentence.split(' '))
        return length

    def score(self, pairs: list) -> list:
        for pair in pairs:
            yield [self.count_words(sentence) for sentence in pair]

    def accept(self, score: list) -> bool:
        if abs(score[0] - score[1]) < 20:
            return True
        else:
            return False


class QuotationMarkFilter(opusfilter.FilterABC):
    """Проверка на закрытие кавычек в переводе"""
    score_direction = opusfilter.CLEAN_LOW

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

    def quotation_mark(self, sentence: str) -> int:
        """Количество кавычек в строке"""
        count_mark = len(re.findall('["\']+', sentence))
        return count_mark

    def score(self, pairs: list) -> list:
        for pair in pairs:
            yield [self.quotation_mark(sentence) for sentence in pair]

    def accept(self, score: list) -> bool:
        return all(amount % 2 == 0 for amount in score)


class AngularQuotesFilter(opusfilter.FilterABC):
    """Проверка угловых кавычек в переводе"""
    score_direction = opusfilter.CLEAN_LOW

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

    def angular_quotes_mark(self, sentence: str) -> bool:
        """Наличие открывающих закрывающих угловых кавычек"""
        close_angular_quotes = sentence.count('»')
        open_angular_quotes = sentence.count('«')
        return True if close_angular_quotes == open_angular_quotes else False

    def score(self, pairs: list) -> list:
        for pair in pairs:
            yield [self.angular_quotes_mark(sentence) for sentence in pair]

    def accept(self, score: list) -> bool:
        return all(value == True for value in score)


class NoTranslationFilter(opusfilter.FilterABC):
    """Проверка осуществления перевода"""
    score_direction = opusfilter.CLEAN_LOW

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

    def translate(self, sentence: str) -> str:
        """Наличие перевода в строке"""
        translation = re.sub('[^a-zA-Z0-9а-яА-Я]', '', sentence)
        return translation

    def score(self, pairs: list) -> list:
        for pair in pairs:
            yield [self.translate(sentence) for sentence in pair]

    def accept(self, score: list) -> bool:
        if score[0].lower() != score[1].lower():
            return True
        else:
            return False