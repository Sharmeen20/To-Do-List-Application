import string

x = string.digits
y = string.ascii_lowercase


def missingCharacters(s):
    a = ""
    b = ""
    for i in x:
        if i not in s:
            a += i

    for i in y:
        if i not in s:
            b += i

    return a + b


if __name__ == '__main__':
    n = input()
    print(missingCharacters(n))
