import re


class RemoveAccent():

    translateChars = {
        'a': r'[àáâãäå]',
        'e': r'[èéêë]',
        'i': r'[ìíîï]',
        'o': r'[òóôõö]',
        'u': r'[ùúûü]',
        'A': r'[ÂÀ]',
        'E': r'[ÊÈ]',
        'I': r'[ÎÌ]',
        'O': r'[ÔÒ]',
        'U': r'[ÙÒ]',
    }

    @staticmethod
    def normalize(old: str) -> str:
        """
        Removes common accent characters, lower form.
        Uses: regex.
        """
        if old == '':
            return ''

        new = str(old)

        for key, value in RemoveAccent.translateChars.items():
            new = re.sub(value, key, new)

        return new
