import random


preview_lines = 4 # minimum 3
seperator = ' '
max_line_char = 30
spacing_between_words = "10px"


class TextCheck:
    def __init__(self):

        self.word_list = [word.strip() for word in open("words.txt").readlines()]
        self.current_line_index = None
        self.current_word_index = None
        self.formatted_lines = None
        self.clean_lines = None
        self.formatted_word = None
        self.correct_words = None
        self.total_words = None
        self.correct_characters = None
        self.incorrect_words = None
        self.restart()

    def restart(self):
        self.correct_words = 0
        self.incorrect_words = 0
        self.total_words = 0
        self.correct_characters = 0
        self.current_line_index = 0
        self.current_word_index = 0
        self.formatted_lines = [[]]
        self.clean_lines = [[]]
        self.formatted_word = ''

        line = 0

        random.shuffle(self.word_list)

        for word in self.word_list:
            if self.clean_lines[line] == []:
                self.clean_lines[line].append(word)
            elif len(seperator.join(self.clean_lines[line]) + seperator + word) < max_line_char:
                self.clean_lines[line].append(word)
            else:
                line += 1
                self.clean_lines.append([word])

    def no_words_left(self):
        if (self.current_line_index == len(self.clean_lines) - 1 and
                self.current_word_index == len(self.clean_lines[self.current_line_index]) ):
            return True
        return False

    def next_word(self, current_input: str):
        try:
            current_word = self.clean_lines[self.current_line_index][self.current_word_index]
        except IndexError:
            print("next_word index error")
            return

        self.total_words += 1
        if current_word == current_input:
            color = "DodgerBlue "
            self.correct_words += 1
            self.correct_characters += len(current_word) + 1
        else:
            self.incorrect_words += 1
            color = "Red"
        self.formatted_lines[self.current_line_index].append(
            f'<span style="color: {color}">{current_word}</span>')

        if self.current_word_index == len(self.clean_lines[self.current_line_index]) - 1:
            self.current_word_index = 0
            self.current_line_index += 1
            self.formatted_lines.append([])
        else:
            self.current_word_index += 1

    def get_formatted_text(self, current_input: str):
        # try to get current word which needs checking ---------------------------
        try:
            current_word = self.clean_lines[self.current_line_index][self.current_word_index]
        except IndexError:
            print("get_formatted_text index error")
            return "No more words"

        # format in rich text current word which is checked -----------------------
        self.formatted_word = '<span style="background-color: #b8e069;">'
        for i in range(0, len(current_word)):
            try:
                if current_word[i] == current_input[i]:
                    self.formatted_word += f'<span style="color: white;">{current_word[i]}</span>'
                else:
                    self.formatted_word += f'<span style="color: red;">{current_word[i]}</span>'
            except IndexError:
                self.formatted_word += current_word[i]
        self.formatted_word += '</span>'

        # format all lines in rich text which needs to be displayed --------------------
        # adding formatted lines before current word
        formatted_text = f'<span style="word-spacing: {spacing_between_words}">'
        if self.current_line_index == 0:
            # if very first line of word list
            formatted_text += seperator.join(self.formatted_lines[0])
        else:
            # if not ...
            formatted_text += seperator.join(self.formatted_lines[self.current_line_index - 1])
            formatted_text += "<br>" + seperator.join(
                self.formatted_lines[self.current_line_index])

        # if current word is not first in line we add seperator
        if self.current_word_index != 0:
            formatted_text += seperator
        formatted_text += self.formatted_word

        # adding current word
        if self.current_word_index < len(self.clean_lines[self.current_line_index]) - 1:
            formatted_text += seperator + seperator.join(
                self.clean_lines[self.current_line_index][self.current_word_index + 1:])

        # adding clean unformatted words after current words
        if self.current_line_index == 0:
            last_line_index = preview_lines - 1
        else:
            last_line_index = self.current_line_index + preview_lines - 2

        for line_index in range(self.current_line_index + 1, last_line_index + 1):
            if line_index < len(self.clean_lines):
                formatted_text += "<br>" + seperator.join(self.clean_lines[line_index])

        formatted_text += "</span>"

        return formatted_text

