def split_numbers(str_of_nums):
    """
    Given a nicely formatted set of phone numbers in a string,
    return them as a list.

    :param str str_of_nums: The string of numbers which for now must be comma separated
    :return: A list of numbers
    :rtype: list[str]
    """
    return str_of_nums.split(',')
