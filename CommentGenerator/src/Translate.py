from googletrans import Translator

class Translate:
    def __init__(self, language:str):
        self.__lang = language
        self.__translate = Translator()

    def get_translation(self, comment:str)->str:
        if self.__lang != "en":
            return self.__translate.translate(comment, dest=self.__lang).text
        else:
            return comment