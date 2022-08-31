import re
import csv
from pprint import pprint


def regrouping_data_by_template(contacts_list):
    for element in contacts_list[1:]:
        for number, item in enumerate(element[:3]):
            fafa = re.search('[\r\t\f\v  ]', item)
            if fafa is not None:
                var = item.split(' ')
                if len(var) == 3 and number == 0:
                    element[0:3] = var
                elif len(var) == 2 and number == 0:
                    element[0:2] = var
                else:
                    element[1:3] = var
    return contacts_list

def formatting_phones(list):
    pattern = '\+*(7|7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})\s*[(]*\w*\.*\s*(\d+)?\)*'
    for item in list[1:]:
        if item[5] != '':
            mama = re.findall(pattern, item[5])
            if mama[0][5] == '':
                little_pattern = r"+7(\2)\3-\4-\5"
                result = re.sub(pattern, little_pattern, item[5])
                item[5] = result
            elif mama[0][5] != '':
                big_pattern = r"+7(\2)\3 -\4 -\5 доб.\6"
                result = re.sub(pattern, big_pattern, item[5])
                item[5] = result
    return list

def megre_doubled_items(formetted_phones_list):
    pass



if __name__ == '__main__':
    with open('phonebook_raw.csv') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        contact_list_regrupped = regrouping_data_by_template(contacts_list)
        formetted_phones_list = formatting_phones(contact_list_regrupped)
        megre_doubled_items(formetted_phones_list)