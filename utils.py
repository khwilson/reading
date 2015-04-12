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
