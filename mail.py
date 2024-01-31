import csv
import re
from pprint import pprint

## Читаем адресную книгу в формате CSV в список contacts_list:
with open("phonebook_raw.csv", encoding='utf8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)
# print()


## 1. Выполните пункты 1-3 задания.
# Помещаем Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно
contacts_pattern = r"^(?P<lastname>\w+)[\s,]*(?P<firstname>\w+)[\s,]*(?P<surname>\w*)[\s,]*(?P<organization>[\w]*),(?P<position>[\w\s\-\–]*),(?P<phone>[\w\d\s\(\)\-\+\.]*),(?P<email>[\w\d\.\-\_@]*)"
contacts_pattern_replace = r"\g<lastname>,\g<firstname>,\g<surname>,\g<organization>,\g<position>,\g<phone>,\g<email>"

re_contacts = re.compile(contacts_pattern)

contacts_list_formatted = [re_contacts.sub(contacts_pattern_replace, ','.join(contact)).split(',') for contact in contacts_list]
# pprint(contacts_list_formatted)
# print()


# Приводим все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, то формат: +7(999)999-99-99 доб.9999.
phone_with_ad_pattern = r"(\+7|8)?[\s\(]*(\d{3})[\)\s\-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\sдоб\.\(]+(\d*)\)*"
phone_with_ad_pattern_replace = r"+7(\2)\3-\4-\5 доб.\6"
phone_pattern = r"(\+7|8)?[\s\(]*(\d{3})[\)\s\-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
phone_pattern_replace = r"+7(\2)\3-\4-\5"

re_phone_with_ad = re.compile(phone_with_ad_pattern)
re_phone = re.compile(phone_pattern)

for i, contact in enumerate(contacts_list_formatted):
    phone = contact[5]
    if re_phone_with_ad.match(phone):
        contacts_list_formatted[i][5] = re_phone_with_ad.sub(phone_with_ad_pattern_replace, phone)
    else:
        contacts_list_formatted[i][5] = re_phone.sub(phone_pattern_replace, phone)

# pprint(contacts_list_formatted)


# Объединяем все дублирующиеся записи о человеке в одну
# При этом примем следующие допущения:
# - фамилия в нашем списке уникальные (хотя можно было бы взять уникальным сочетание фамилия+имя (т.к. отчество может быть не указано))
# - если в дублирующихся записях заполнено одно и то же поле, то информацию берем из наибольшего поля (считая, что там более полная информация)
contacts_list_unique = {}
for contact in contacts_list_formatted:
    if contacts_list_unique.get(contact[0]) is None:
        contacts_list_unique[contact[0]] = contact
    else:
        for i, field in enumerate(contact):
            try:
                contacts_list_unique[contact[0]][i] = max(contacts_list_unique[contact[0]][i], field)
            except IndexError as err:
                print(f'При обработке строки {i} возникла ошибка "{err}". Возможно, в дублирующихся записях оказалось разное число полей. '
                    f'Строка обработана, но рекомендуется проверить её корректность.')
                # Если в дублирующейся записи полей больше, чем в первичной - добавить в первичную запись новое поле 
                # (чтобы не потерять дополнительные данные, оказавшиеся в дублирующей записи)
                if i >= len(contacts_list_unique[contact[0]]):
                    contacts_list_unique[contact[0]].append(field)

# pprint(contacts_list_unique)


# 2. Сохраните получившиеся данные в другой файл.
## Код для записи файла в формате CSV:
with open("phonebook.csv", "w", encoding='utf8', newline='') as f:
    datawriter = csv.writer(f, delimiter=',')

## Вместо contacts_list подставьте свой список:
    datawriter.writerows(contacts_list_unique.values())