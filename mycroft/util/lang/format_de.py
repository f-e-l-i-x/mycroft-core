# -*- coding: utf-8 -*-
#
# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from mycroft.util.lang.format_common import convert_to_mixed_fraction

NUM_STRING_DE = {
    0: 'null',
    1: 'ein', #ein Viertel etc., nicht eins Viertel
    2: 'zwei',
    3: 'drei',
    4: 'vier',
    5: u'fünf',
    6: 'sechs',
    7: 'sieben',
    8: 'acht',
    9: 'neun',
    10: 'zehn',
    11: 'elf',
    12: u'zwölf',
    13: 'dreizehn',
    14: 'vierzehn',
    15: u'fünfzehn',
    16: 'sechzehn',
    17: 'siebzehn',
    18: 'achtzehn',
    19: 'neunzehn',
    20: 'zwanzig',
    30: u'dreißg',
    40: 'vierzig',
    50: u'fünfzig',
    60: 'sechzig',
    70: 'siebzig',
    80: 'achtzig',
    90: 'neunzig',
    100: 'hundert'
}

# German uses "long scale" https://en.wikipedia.org/wiki/Long_and_short_scales

NUM_POWERS_OF_TEN = {
    'tausend','Million','Milliarde','Billion','Billiarde','Trillion','Trilliarde'
}

FRACTION_STRING_DE = {
    2: 'halb',
    3: 'drittel',
    4: 'viertel',
    5: u'fünftel',
    6: 'sechstel',
    7: 'siebtel',
    8: 'achtel',
    9: 'neuntel',
    10: 'zehntel',
    11: 'elftel',
    12: u'zwölftel',
    13: 'dreizehntel',
    14: 'vierzehntel',
    15: u'fünfzehntel',
    16: 'sechzehntel',
    17: 'siebzehntel',
    18: 'achtzehntel',
    19: 'neunzehntel',
    20: 'zwanzigstel'
}


def nice_number_de(number, speech, denominators):
    """ German helper for nice_number
    This function formats a float to human understandable functions. Like
    4.5 becomes "4 einhalb" for speech and "4 1/2" for text
    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        # Give up, just represent as a 3 decimal number
        return str(round(number, 3))
    whole, num, den = result
    if not speech:
        if num == 0:
            # TODO: Number grouping?  E.g. "1,000,000"
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)
    if num == 0:
        return str(whole)
    den_str = FRACTION_STRING_DE[den]
    if whole == 0:
        if num == 1:
            if den == 2:
                return_string = ''
            return_string = 'ein {}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1:
        return_string = '{} und ein {}'.format(whole, den_str)
    else:
        return_string = '{} und {} {}'.format(whole, num, den_str)

    return return_string


def pronounce_number_de(num, places=2):
    """
    Convert a number to its spoken equivalent
    For example, '5.2' would return 'five point two'
    Args:
        num(float or int): the number to pronounce (set limit below)
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number

    """





    def pronounce_triplet_de(num):
        result = ""
        num = floor(num)
        if num>99:
            hundreds=floor(num/100)
            if hundreds > 0:
                result += NUM_STRING_DE[hundreds] + EXTRA_SPACE + 'hundert' + EXTRA_SPACE
                num -= hundreds*100
        if num == 0:
                result += '' # do nothing
        elif num == 1:
                result += 'eins' #need the s for the last digit
        elif num <= 20:
                result += NUM_STRING_DE[num]# + EXTRA_SPACE
        elif num > 20:
             ones = num % 10
             tens = num - ones
             if ones > 0:
                 result += NUM_STRING_DE[ones] + EXTRA_SPACE
                 if tens > 0:
                     result += 'und' + EXTRA_SPACE
             if tens > 0:
                     result += NUM_STRING_DE[tens] + EXTRA_SPACE
        return result

    def pronounce_fractional_de(num, places): # fixed number of places even with trailing zeros
        result = ""
        place = 10
        while places > 0:             #doesn't work with 1.0001 and places = 2: int(num*place) % 10 > 0 and places > 0:
            result += " " + NUM_STRING_DE[int(num*place) % 10]
            if int(num*place) % 10 == 1:
                result += 's'  # "1" is pronounced "eins" after the decimal point
            place *= 10
            places -= 1
        return result

    def pronounce_whole_number_de(num, scale_level=0):
        if num == 0:
            return ''

        num = floor(num)
        result = ''
        last_triplet = num % 1000

        if last_triplet == 1:
            if scale_level == 0:
                if result != '':
                    result += '' + 'eins'
                else:
                    result += "eins"
            elif scale_level == 1:
                result += 'ein' + EXTRA_SPACE + 'tausend' + EXTRA_SPACE
            else:
                result += "eine " + NUM_POWERS_OF_TEN[scale_level] + ' '
        elif last_triplet > 1:
            result += pronounce_triplet_de(last_triplet)
            if scale_level == 1:
                #result += EXTRA_SPACE
                result += 'tausend' + EXTRA_SPACE
            if scale_level >= 2:
                #if EXTRA_SPACE == '':
                #    result += " "
                result += " " + NUM_POWERS_OF_TEN[scale_level]
            if scale_level >= 2:
                if scale_level % 2 == 0:
                    result += "e" #MillionE
                result += "n "   #MilliardeN, MillioneN

        num = floor(num/1000)
        scale_level += 1
        return pronounce_whole_number_de(num,scale_level) +  result# + EXTRA_SPACE

    result = ""
    if abs(num) >= 1000000000000000000000000: # cannot do more than this
        return str(num)
    elif num == 0:
        return str(NUM_STRING_DE[0])
    elif num < 0:
         return "minus " + pronounce_number_de(abs(num), places)
    else:
        if num == int(num):
            return pronounce_whole_number_de(num)
        else:
            whole_number_part = floor(num)
            fractional_part = num - whole_number_part
            result += pronounce_whole_number_de(whole_number_part)
            result += " Komma"
            result += pronounce_fractional_de(fractional_part,places)
            return result


def nice_time_en(dt, speech=True, use_24hour=False, use_ampm=False):
    """
    Format a time to a comfortable human format

    For example, generate 'five thirty' for speech or '5:30' for
    text display.

    Args:
        dt (datetime): date to format (assumes already in local timezone)
        speech (bool): format for speech (default/True) or display (False)=Fal
        use_24hour (bool): output in 24-hour/military or 12-hour format
        use_ampm (bool): include the am/pm for 12-hour format
    Returns:
        (str): The formatted time string
    """
    if use_24hour:
        # e.g. "03:01" or "14:22"
        string = dt.strftime("%H:%M")
    else:
        if use_ampm:
            # e.g. "3:01 AM" or "2:22 PM"
            string = dt.strftime("%I:%M %p")
        else:
            # e.g. "3:01" or "2:22"
            string = dt.strftime("%I:%M")
        if string[0] == '0':
            string = string[1:]  # strip leading zeros

    if not speech:
        return string

    # Generate a speakable version of the time
    if use_24hour:
        speak = ""

        # speaking leading 0 not needed in German: 08:00 -> "acht Uhr"
        # 13:00 -> "13 Uhr"
        if string[0] == '0':
        #    speak += pronounce_number_en(int(string[0])) + " "
            speak += pronounce_number_de(int(string[1]))
        else:
            speak = pronounce_number_de(int(string[0:2]))

        speak += " "

        # not needed in German 13:00 -> "dreizehn Uhr"
        if string[3:5] == '00':
            speak += "Uhr"
        else:
            if string[3] == '0':
                #not needed in German, EN 13:05 -> "13 Oh 5" or "13 zero 5", DE 13:05 -> "13 Uhr 5" (leading zero is dropped)
                #speak += pronounce_number_de(0) + " "
                speak += "Uhr" + pronounce_number_de(int(string[4]))
            else:
                speak += "Uhr" + pronounce_number_de(int(string[3:5]))
        return speak
    else:
        if dt.hour == 0 and dt.minute == 0:
            return "Mitternacht"
        if dt.hour == 12 and dt.minute == 0:
            return "Mittag"
        # TODO: "half past 3", "a quarter of 4" and other idiomatic times

        if dt.hour == 0:
            speak = pronounce_number_de(12)
        elif dt.hour < 13:
            speak = pronounce_number_de(dt.hour)
        else:
            speak = pronounce_number_de(dt.hour-12)

        if dt.minute == 0:
            if not use_ampm:
                return speak + " Uhr"
        else:
            speak += " Uhr" + pronounce_number_en(dt.minute)

        if use_ampm:
            if dt.hour > 11:
                speak += " PM"
            else:
                speak += " AM"

        return speak
