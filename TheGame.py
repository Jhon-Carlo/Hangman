from hangman import HangmanGame
import random
import unittest
from io import StringIO
from unittest.mock import patch

class HangmanGame:
    def __init__(self, word, lives=5):
        self.word = word.lower()
        self.display_word = ['_' if c.isalpha() else c for c in self.word]
        self.lives = lives
        self.guessed_letters = set()

    def get_display_word(self):
        return ''.join(self.display_word)

    def guess(self, letter):
        letter = letter.lower()
        if not letter.isalpha() or letter in self.guessed_letters:
            return False
        self.guessed_letters.add(letter)

        if letter in self.word:
            for idx, char in enumerate(self.word):
                if char == letter:
                    self.display_word[idx] = letter
            return True
        else:
            self.lives -= 1
            return False

    def has_won(self):
        return '_' not in self.display_word

    def is_game_over(self):
        return self.lives <= 0 or self.has_won()


words = ['potato', 'tomato', 'cat', 'hangman']
phrases = ['individual assessment', 'python programmer', 'hangman test']

def choose_word(level='basic'):
    return random.choice(words if level == 'basic' else phrases)

def run_game(level='basic'):
    word = choose_word(level)
    game = HangmanGame(word=word, lives=6)

    print("Hangman")
    print(f"Level: {level.capitalize()}")
    print(f"You have {game.lives} lives. Let's begin!")

    while not game.is_game_over():
        print("\nWord: " + game.get_display_word())
        print(f"Lives remaining: {game.lives}")

        user_input = input("Guess a letter: ").strip().lower()

        if len(user_input) != 1 or not user_input.isalpha():
            print("Enter a single letter.")
            continue

        if game.guess(user_input):
            print("Correct")
        else:
            print("Incorrect")

    if game.has_won():
        print("\nYay! You guessed the word:", game.word)
    else:
        print("\nYou lost! The word was:", game.word)

class TestHangmanGame(unittest.TestCase):
    
    #Test for Basic
    @patch('main.random.choice', return_value='potato')  #Word for testing: potato
    def test_basic_level_word(self, mock_choice):
        level = 'basic'
        word = choose_word(level)
        self.assertEqual(word, 'potato')

    #Test for Intermediate
    @patch('main.random.choice', return_value='individual assessment')  #Phrase for testing: individual assessment
    def test_intermediate_level_phrase(self, mock_choice):
        level = 'intermediate'
        phrase = choose_word(level)
        self.assertEqual(phrase, 'individual assessment')

    #Test if underscores are correctly displayed for a word
    @patch('main.random.choice', return_value='potato')  #Word for testing: potato
    def test_underscores_display(self, mock_choice):
        game = HangmanGame('potato')
        display_word = game.get_display_word()
        self.assertEqual(display_word, '______')  #Potato is represented as ______

    #Test that correct guesses reveal the correct letters in the word
    @patch('main.random.choice', return_value='potato')  #Word for testing: potato
    def test_correct_guess_reveal(self, mock_choice):
        game = HangmanGame('potato')
        game.guess('p')
        display_word = game.get_display_word()
        self.assertEqual(display_word, 'p_____')  #The p is revealed, others are still underscores

    #Test that lives are deducted when guessing wrong letters
    @patch('main.random.choice', return_value='potato')  #Word for testing: potato
    def test_incorrect_guess_deduct_life(self, mock_choice):
        game = HangmanGame('potato')
        game.guess('x')
        self.assertEqual(game.lives, 5)  #Life should go from 6 to 5

    #Test that hangman ends when the player runs out of lives
    @patch('main.random.choice', return_value='potato')  #Word for testing: potato
    def test_game_over_when_lives_zero(self, mock_choice):
        game = HangmanGame('potato', lives=1)  #Lives changed to 1 for testing
        game.guess('x')
        self.assertTrue(game.is_game_over())  #The game should end
        self.assertFalse(game.has_won())

    #Test that the game ends when the player guesses the word correctly
    @patch('main.random.choice', return_value='potato')  #Word for testing: potato
    def test_game_over_when_word_guessed(self, mock_choice):
        game = HangmanGame('potato')
        game.guess('p')
        game.guess('o')
        game.guess('t')
        game.guess('a')
        game.guess('t')
        game.guess('o')
        self.assertTrue(game.is_game_over())  # Game should be over when word is guessed correctly
        self.assertTrue(game.has_won())  # Player won by guessing the word correctly

if __name__ == '__main__':
    #Comment the lines below, and uncomment the last line for testing
    level = input("Choose level (basic/intermediate): ").strip().lower()
    if level not in ['basic', 'intermediate']:
        level = 'basic'
    run_game(level)
    
    #unittest.main()
