"""
Some utility functions

@author Kevin Wilson - khwilson@gmail.com
"""
import random


LETTERS_AND_DIGITS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'


def random_string(length):
    """
    Return a random string of the given length consisting of letters and numbers

    :param int length: The length of the random string
    :return: A random string
    :rtype: str
    """
    return ''.join(random.choice(LETTERS_AND_DIGITS) for _ in xrange(length))


def split_numbers(str_of_nums):
    """
    Given a nicely formatted set of phone numbers in a string,
    return them as a list.

    :param str str_of_nums: The string of numbers which for now must be comma separated
    :return: A list of numbers
    :rtype: list[str]
    """
    return str_of_nums.split(',')
