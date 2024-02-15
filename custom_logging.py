import time
from inspect import (
    currentframe,
    stack
)


def custom_logging_base(text: str, _time: bool, _location: bool, _path: bool):
    """

    :param _path:
    :param text:
    :param _time:
    :param _location:
    :return:
    """
    details = []
    if _time:
        details.append(str(time.ctime(time.time())))
    if _location and _path:
        details.append(f"{stack()[1][1]}:{currentframe().f_back.f_lineno}")
    elif _location:
        double_backslash = "\\"
        details.append(f"{stack()[1][1].split('/')[-1].split(double_backslash)[-1]}:{currentframe().f_back.f_lineno}")
    if details:
        print(f"[{' '.join(details)}] {text}")


def cwarn(text: ..., _time: bool = True, _location: bool = True, _path: bool = False):
    """
    custom warning message function
    :param _path:
    :param _location:
    :param _time:
    :param text:
    :return:
    """
    custom_logging_base(str(text), _time, _location, _path)


def clog(text: ..., _time: bool = True):
    """
    custom log function
    :param _time:
    :param text:
    :return:
    """
    print(f"[{str(time.ctime(time.time()))}] {str(text)}")


def cout(text: ..., _time: bool = True):
    """
    custom output function
    :param _time:
    :param text:
    :return:
    """
    print(str(text))
