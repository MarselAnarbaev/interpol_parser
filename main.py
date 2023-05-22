# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import webparse
import person


def test():
    yellow = "https://www.interpol.int/How-we-work/Notices/View-Yellow-Notices#"
    red = "https://www.interpol.int/How-we-work/Notices/View-Red-Notices#"
    page = input("Enter page (yellow, red): ")
    name = input("Enter name (or empty): ")
    forename = input("Enter forename (or empty): ")
    parse = person.Person()
    if page.lower() == 'red':
        parse.get_persons_data(red, name, forename)
    elif page.lower() == 'yellow':
        parse.get_persons_data(yellow, name, forename)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
