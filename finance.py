#with open('data_leak_sample.txt', 'r', encoding='utf-8') as f:
    #main_text = f.read()

import re
from datetime import datetime

def num_card(text) -> str:
  return re.sub(r'\D', '', text)


def check_luhn(text) -> bool:
  total_sum = 0
  card=num_card(text)
  for i in range(len(card)):
      num_text = int(card[i])
      if i % 2 ==0 :
          if num_text * 2 > 9:
              total_sum+= (2 * num_text) - 9
          else:
              total_sum += 2 * num_text
      else:
          total_sum += num_text
  return total_sum % 10 == 0


def find_and_validate_credit_cards(text) -> dict:
   pattern_1 = r'(?:\d ?[ -]? ?){13,19}'
   card_in_text = re.findall(pattern_1, text)
   pattern_2 = r'\b(?:\d{4} ?[- ]? ?){3}\d{4}\b'
   potential_cards = re.findall(pattern_2, text)
   result = {'valid': [], 'invalid': []}
   for num in card_in_text:
       if num in potential_cards and check_luhn(num):
        result['valid'].append(num)
   else:
       result['invalid'].append(num)
   return result


with open('data_leak_sample.txt', 'r', encoding='utf-8') as f:
    main_text = f.read()
    print(find_and_validate_credit_cards(main_text))

def leap_year(year: int) -> bool:
    """
    Determine whether a given year is a leap year.

    Args:
        year (int): The year to check.

    Returns:
        bool: True if the year is a leap year, False otherwise.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def days_check(month: int, year: int, day: int) -> bool:
    """
    Check if the given day is valid for the specified month and year.

    Args:
        month (int): Month number (1-12).
        year (int): Year number.
        day (int): Day number.

    Returns:
        bool: True if the day is valid for the month, False otherwise.
    """
    if month in [4, 6, 9, 11] and day > 30:
        return False
    if month == 2:
        if leap_year(year) and day > 29:
            return False
        elif not leap_year(year) and day > 28:
            return False
    return True


def add_spase(text):
    text_list = []
    text = str(text)
    for i in range(16):
        if (i+1) %4 != 0:
            text_list.append(text[i])
        else:
            text_list.append(text[i])
            text_list.append(" ")
    return "".join(text_list)

def parse_date(date_str):
    formats = ['%d.%m.%Y', '%Y/%m/%d', '%d-%b-%Y', '%d-%m-%Y','%d/%m/%Y','%d-%m-%Y',
                    '%Y.%m.%d', '%Y-%m-%d', '%d/%b/%Y', '%d.%b.%Y' ,'%Y-%b-%d',
                    '%Y.%b.%d', '%d-%B-%Y', '%d/%B/%Y', '%d.%B.%Y', '%Y-%B-%d','%Y.%B.%d']
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime('%d.%m.%Y')
        except ValueError:
            continue
    return None

def find_and_validate_credit_cards(text) -> dict:
   pattern_1 = r'(?:\d ?[ -]? ?){13,19}'
   card_in_text = re.findall(pattern_1, text)
   pattern_2 = r'\b(?:\d{4} ?[- ]? ?){3}\d{4}\b'
   potential_cards = re.findall(pattern_2, text)
   for num in card_in_text:
       if num in potential_cards and check_luhn(num):
         return True
   else:
         return False


def phones(data1):
    result = {
        'phones': {'valid': [], 'invalid': []},
        'dates': {'normalized': [], 'invalid': []},
        'inn': {'valid': [], 'invalid': []},
        'cards': {'valid': [], 'invalid': []}
             }
    data_num = data1.get('phones', [])
    pattern = (r"(\+7|8|007)[ ]?[\-*.(]?\d{3}[)\-*.]?[ ]?"
               r"\d{3}[ \-\.]?\d{2}[ \-\.]?\d{2}")
    for phone in data_num:
        number_match = re.match(pattern, phone)
        if number_match:
            first_num = number_match.group(0)
            number_digits = re.sub(r'\D', '', phone)
            if first_num.startswith("+7") or first_num.startswith("7"):
                if first_num.startswith("+7"):
                    normal_phone = "+7" + number_digits[1:]
                else:
                    normal_phone = "+7" + number_digits[1:]
                result['phones']['valid'].append(normal_phone)
            elif first_num.startswith("8"):
                normal_phone = "+7" + number_digits[1:]
                result['phones']['valid'].append(normal_phone)
            elif first_num.startswith("007"):
                normal_phone = "+7" + number_digits[3:]
                result['phones']['valid'].append(normal_phone)
            else:
                normal_phone = "+7" + number_digits
                result['phones']['valid'].append(normal_phone)
        else:
            result['phones']['invalid'].append(phone)

    for date_str in data.get('dates', []):
        date_str = date_str.strip()
        normalized = parse_date(date_str)
        dt = datetime.strptime(normalized, '%d.%m.%Y')
        year = dt.year
        month = dt.month
        day = dt.day
        if normalized and days_check(month, year, day):
            result['dates']['normalized'].append(normalized)
        else:
            result['dates']['invalid'].append(date_str)

    for inn in data.get('inn', []):
        if not re.fullmatch(r'\d+', inn):
            result['inn']['invalid'].append(inn)
        else:
            inn_digits = inn
            if len(inn_digits) in (10, 12):
                result['inn']['valid'].append(inn_digits)
            else:
                result['inn']['invalid'].append(inn)
    for card in data.get('cards', []):
        pattern_2 = r'\b(?:\d{4} ?[- ]? ?){3}\d{4}\b'
        potential_cards = re.match(pattern_2, card)
        if potential_cards:
            if check_luhn(num_card(card)):
                card_digits = num_card(card)
                result['cards']['valid'].append(add_spase(card_digits))
            else:
                card_digits = num_card(card)
                result['cards']['invalid'].append(add_spase(card_digits))
        else:
            card_digits = num_card(card)
            result['cards']['invalid'].append(add_spase(card_digits))
    return result




def read_and_parse(filepath):
    data = {
        'phones': [],
        'dates': [],
        'inn': [],
        'cards': []
    }

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue


            parts = line.split(':', 1)
            if len(parts) != 2:
                continue

            category = parts[0].strip().lower()
            values_str = parts[1].strip()

            values = re.split(r'[;,]', values_str)
            values = [vl.strip() for vl in values if vl.strip()]

            if category == 'телефоны':
                for vl in values:
                    data['phones'].append(vl)
            elif category == 'даты':
                for vl in values:
                    data['dates'].append(vl)
            elif category == 'инн':
                for vl in values:
                    data['inn'].append(vl)
            elif category == 'карты':
                for vl in values:
                    data['cards'].append(vl)
    return data
