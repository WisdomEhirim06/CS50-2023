import math


def main():
    # prompt user for text
    text = str(input("Text: "))

    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # using an algoritm to find the index
    L = (letters / float(words)) * 100
    S = (sentences / float(words)) * 100
    index = (0.0588 * L) - (0.296 * S) - 15.8

    # to find index with certain conditions
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {round(index)}")


def count_letters(text):
    letters = 0
    # find if each char is a letter
    for i in range(len(text)):
        if text[i].isalpha():
            letters += 1
    return letters


def count_words(text):
    spaces = 0
    # words are just spaces in between each text
    # keep adding to it
    for i in range(len(text)):
        if text[i].isspace():
            spaces += 1
            words = spaces + 1
    return words


def count_sentences(text):
    sentences = 0
    # search for punctuations that will determine if a sentence
    # return each of this
    for i in range(len(text)):
        if text[i] == "?" or text[i] == "!" or text[i] == ".":
            sentences += 1
    return sentences


main()