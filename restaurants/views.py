from django.shortcuts import render


# Restaurant Section

def restaurant_filter_view(request):
    """
    Restaurant filtering view - bu yerda Restaurantlarni royxati kerak bolsa shu view ga murojat qilinadi.

    Diqqat: Ma'lum bir paremetrlar qabul qilinadi filterlash uchun, xech qanday parametr qabul qilinmasa toliq royxat
    pagination bilan qaytariladi.
    """
    pass


def restaturant_add_view(request):
    """
    Yangi restaurant qoshish uchun ishlatiladi.

    Talab qilinadi: Bunig uchun faqat Ma'lum toifadagi royxatdan otgan va shu api
    ga dostupi bor login qilgan user bolishi shart.
    """
    pass


def restaturant_actions_view(request):
    """
    Bu yerda restaurant ga tegishli amallarni request type ga qarab delete, get detail, edit, qilish amallarini bajarish
    uchun ishlatiladi.

    Diqqat: {id} - restaurant id sini parametr sifatida user tarafidan jonatilishi kerak.
    Talab qilinadi: Edit yoki delete qilish uchun user Super admin yoki, Restaurant egasi, Tzim manageri bolishi kerak
    """
    pass


# Room section


def restaurant_room_view(request):
    """
    Restaurantlarni room lari ni royxat korinishda olish uchun

    Diqqat: {id} - restaurant id si jonatilish shart
    Talab qilinmaydi: User ixtiyoriy bolishi kerak, royxatdan otgan otmagan, admin admin emas ...
    """

    pass


def restaurant_room_add_view(request):
    """
    Restaurant uchun yangi room qoshish uchun ishlatiladi.

    Diqqat: {id} - restaurant id si jonatilish shart
    Talab qilinadi: User restaurant egasi, yoki tizim adminstratori bolishi kerak
    """
    pass


def restaurant_room_actions_view(request):
    pass


# Menu section

def restaurant_menu_view(request):
    pass


def restaurant_menu_add_view(request):
    pass


def restaurant_menu_actions_view(request):
    pass


# Comments and Reviews

def restaurant_comment_view(request):
    pass


def restaurant_rate_view(request):
    pass
