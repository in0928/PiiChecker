class TextChecker:

    @staticmethod
    def target_ends_at(tokens, target):
        """

        :param tokens: a list of words which can be indexed
        :param target: tag_ of the word in tokens
        :return: the index where the last match with target tag_ occurs
        """
        count = 0
        while count < len(tokens)-1:
            if tokens[count].tag_ == target:
                count += 1
                continue
            else:
                return count
        return count


    def checkName(self):
        pass

    def checkAddress(self):
        pass