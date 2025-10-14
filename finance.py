#with open('data_leak_sample.txt', 'r', encoding='utf-8') as f:
    #main_text = f.read()

import re


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
