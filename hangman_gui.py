from tkinter import *
import tkinter.font as TkFont
import random
import re

class Hangman:

    def __init__(self):
        # initialize app window
        self.root = Tk()
        self.root.title("Hangman GUI")
        self.root.resizable(False, False)
        self.start()
        self.root.update()
        x_coord = int(self.root.maxsize()[0]/2 - self.root.winfo_width()/2)
        y_coord = int(self.root.maxsize()[1]/2 - self.root.winfo_height()/2)
        self.root.geometry(f"+{x_coord}+{y_coord}")
        self.root.mainloop()

    def reposition(self):
        before_width = self.root.winfo_width()
        before_height = self.root.winfo_height()
        self.root.update()
        after_width = self.root.winfo_width()
        after_height = self.root.winfo_height()
        translation_x = int((before_width-after_width) / 2)
        translation_y = int((before_height-after_height) / 2)
        self.root.geometry(f"+{self.root.winfo_x()+translation_x}+{self.root.winfo_y()+translation_y}")

    def get_word_list(self, file_name):
        word_list_file = open(file_name, "r") # "read"
        word_list_text = word_list_file.read()
        word_list = word_list_text.split(" ")
        word_list_file.close() # an opened file should always be closed
        """ alt:
        with open(file_name, "r") as word_list_file:
            # this way, the file will automatically close when the program exits the block
        """
        return word_list

    def start(self):
        # initialize game variables
        WORD_LIST_FILE_NAME = "words.txt"
        word_list = self.get_word_list(WORD_LIST_FILE_NAME)
        self.secret_word = random.choice(word_list)
        print(self.secret_word)
        self.guessed_letters = []
        # initialize gui elements
        self.game_frame = Frame(self.root)
        self.welcome_label = Label(self.game_frame, text="Welcome to Hangman GUI")
        self.welcome_label.pack()
        self.remaining_guesses = 6
        self.remaining_guesses_label = Label(self.game_frame, text=f"You have {self.remaining_guesses} guesses left.")
        self.remaining_guesses_label.pack()
        self.game_board = list("_"*len(self.secret_word))
        self.game_board_label = Label(self.game_frame, text=" ".join(self.game_board), font=TkFont.Font(size=20))
        self.game_board_label.pack()
        self.user_entry_label = Label(self.game_frame, text="Guess a letter or a word")
        self.user_entry_label.pack()
        self.user_entry = Entry(self.game_frame, justify="center")
        self.user_entry.bind("<Return>", lambda event: self.submit_guess()) # bind Return key to submit_guess in entry field
        self.user_entry.pack()
        self.user_entry.focus_set()
        self.alert_label = Label(self.game_frame, text="", fg="red")
        self.submit_guess_button = Button(self.game_frame, text="Submit My Guess", command=self.submit_guess)
        self.submit_guess_button.pack()

        self.correct_frame = Frame(self.root)
        self.congrats_label = Label(self.correct_frame, text=f"\nIt's {self.secret_word}!\nCongratulations! You guessed the secret word!")
        self.congrats_label.pack()
        self.correct_restart_button = Button(self.correct_frame, text="Start New Game", command=self.restart)
        self.correct_restart_button.bind("<Return>", lambda event: self.restart())
        self.correct_restart_button.pack()

        self.incorrect_frame = Frame(self.root)
        self.ran_out_label = Label(self.incorrect_frame, text=f"\nYou ran out of attempts.\nThe secret word is {self.secret_word}.")
        self.ran_out_label.pack()
        self.incorrect_restart_button = Button(self.incorrect_frame, text="Start New Game", command=self.restart)
        self.incorrect_restart_button.bind("<Return>", lambda event: self.restart())
        self.incorrect_restart_button.pack()
        # pack game_frame
        self.game_frame.pack(padx=50, pady=50)

    def restart(self):
        # remove all gui elements
        self.game_frame.pack_forget()
        self.correct_frame.pack_forget()
        self.incorrect_frame.pack_forget()
        # create new variables and elements
        self.start()
        # remove welcome_label from game_frame
        self.welcome_label.pack_forget()
        self.reposition()

    def congrats(self):
        self.game_frame.pack_forget()
        self.correct_frame.pack(padx=50, pady=50)
        self.correct_restart_button.focus_set()
        self.reposition()

    def failed(self):
        self.game_frame.pack_forget()
        self.incorrect_frame.pack(padx=50, pady=50)
        self.incorrect_restart_button.focus_set()
        self.reposition()

    def get_user_entry(self, error_message="invalid", pattern=".*"):
        try: # convert to string
            user_input = str(self.user_entry.get())
        except:
            self.show_alert_label(error_message)
            return ""
        # match pattern
        if re.search(pattern, user_input):
            return user_input
        else:
            self.show_alert_label(error_message)
            return ""

    def submit_guess(self):
        guess = self.get_user_entry("Your guess is invalid.", "^[a-z]+$")
        self.user_entry.delete(0, END) # empty text in entry widget
        if len(guess) > 1:
            word = guess
            if word == self.secret_word:
                self.congrats()
                return
            else:
                self.show_alert_label(f"{word} is not the correct word.")
        elif len(guess) == 1:
            letter = guess
            if letter in self.guessed_letters:
                self.show_alert_label("You already guessed this letter.")
            elif letter in self.secret_word:
                for m in re.finditer(letter, self.secret_word):
                    self.game_board[m.start()] = letter
                    self.game_board_label.configure(text=" ".join(self.game_board))
                self.hide_alert_label()
                if "_" not in self.game_board:
                    self.congrats()
                    return
            else:
                self.show_alert_label(f'The letter "{letter}" is not in the secret word.')
                self.remaining_guesses -= 1
                self.remaining_guesses_label.configure(text=f"You have {self.remaining_guesses} guesses left.")
            self.guessed_letters.append(letter)
        else:
            pass

        if self.remaining_guesses == 0:
            self.failed()
            return

    def hide_alert_label(self):
        self.alert_label.pack_forget()
        self.reposition()

    def show_alert_label(self, text):
        # insert new text
        self.alert_label.configure(text=text)
        # pack alert_label above submit_guess_button
        self.alert_label.pack()
        self.submit_guess_button.pack_forget()
        self.submit_guess_button.pack()
        self.reposition()

Hangman()
