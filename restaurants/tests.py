d = {
    'pk': 1,
    'name': 'hh',
    'phone': 998901234567,
    'address': 'Novza'
}


#
# d2 = {}
#
#
# def change(*args, **kwargs):
#     for key in kwargs.keys():
#         for value in args:
#             print(key, value)
#
#
# for key, value in d.items():
#     change(key, value)
#     # print(key)
def table_things(**kwargs):
    print(kwargs['name'])
    for name, value in kwargs.items():
        print(name, '=', value)



table_things(name="hello", pk=2)

