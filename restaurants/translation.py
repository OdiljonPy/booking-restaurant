from .models import RoomType
from modeltranslation.translator import translator, TranslationOptions


class RoomTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(RoomType, RoomTypeTranslationOptions)
