import re
import csv


def regrouping_data_by_template(contacts_list: list):
    """Places the last name, first name and middle name in the correct columns.

    :param contacts_list: list
    :return: formatted contacts_list
    """
    for element in contacts_list[1:]:
        for number, item in enumerate(element[:3]):
            names_for_regrouping = re.search("[\r\t\f\v ]", item)
            if names_for_regrouping is not None:
                var = item.split(' ')
                if len(var) == 3 and number == 0:
                    element[0:3] = var
                elif len(var) == 2 and number == 0:
                    element[0:2] = var
                else:
                    element[1:3] = var
    return contacts_list


def formatting_phones(phone_list: list):
    """Formats the number mask according to the scheme +7(999)999-99-99 ext.9999

    :param phone_list: list
    :return: phone_list with correct number mask
    """
    pattern = r"\+*(7|7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})\s*[(]*\w*\.*\s*(\d+)?\)*"
    for item in phone_list[1:]:
        if item[5] != '':
            mama = re.findall(pattern, item[5])
            if mama[0][5] == '':
                little_pattern = r"+7(\2)\3-\4-\5"
                result = re.sub(pattern, little_pattern, item[5])
                item[5] = result
            elif mama[0][5] != '':
                big_pattern = r"+7(\2)\3-\4-\5 доб.\6"
                result = re.sub(pattern, big_pattern, item[5])
                item[5] = result
    return phone_list


def merge_doubled_items(formatted_phones_list: list):
    """Merges repeating contact data

    :param formatted_phones_list: list
    :return: formatted_phones_list with merged repeating data
    """
    last_list = []
    for count, element in enumerate(formatted_phones_list):
        for count_2, second_element in enumerate(formatted_phones_list):
            if element[:2] == second_element[0:2] and count < count_2 and len(element) != 0:
                list_template = ['', '', '', '', '', '', '']
                for count_3, item in enumerate(element):
                    if item != '':
                        list_template[count_3] = item
                for count_4, item in enumerate(second_element):
                    if item != '':
                        list_template[count_4] = item
                last_list.append(list_template)
                formatted_phones_list[count].clear()
                formatted_phones_list[count_2].clear()
        else:
            if len(element) != 0:
                last_list.append(element)
    return last_list


if __name__ == '__main__':
    with open('phonebook_raw.csv') as file_raw:
        rows = csv.reader(file_raw, delimiter=",")
        contacts_list = list(rows)
        contact_list_regrupped = regrouping_data_by_template(contacts_list)
        contact_list_formatted = formatting_phones(contact_list_regrupped)
        contact_list_merged = merge_doubled_items(contact_list_formatted)
        with open("phonebook.csv", "w") as file_done:
            data_writer = csv.writer(file_done, delimiter=',')
            data_writer.writerows(contact_list_merged)
