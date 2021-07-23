# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from covidhelp.vaccinhelp.views import *


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    districts_ids =  (307,301,306,297,295,298,304,305,302,308,300,296,303,299)
    pincodes = (683556,)
    for x in districts_ids:
        dist_fetch_data_from_cowin(x)
    for y in pincodes:
        fetch_data_from_cowin(y)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
