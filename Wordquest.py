import random
import os
import time

class WordQuest:
    def __init__(self):
        self.words = {
            'easy': ['apple', 'house', 'river', 'music', 'happy', 'light', 'dream', 'smile', 'peace', 'heart',''],
            'medium': ['python', 'garden', 'journey', 'mystery', 'victory', 'courage', 'freedom', 'harmony', 'wisdom', 'silence'],
            'hard': ['adventure', 'challenge', 'beautiful', 'knowledge', 'treasure', 'mountain', 'wonderful', 'brilliant', 'fantastic', 'universe']
        }
        self.score = 0
        self.max_attempts = 6
        self.hints_used = 0
        self.max_hints = 2
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_title(self):
        title = """
        ╔══════════════════════════════════════╗
        ║             WORD QUEST              ║
        ║     Welcome to Word Quess Game      ║
        ╚══════════════════════════════════════╝
        """
        print(title)
    
    def choose_difficulty(self):
        print("\nChoose your difficulty level:")
        print("1. Easy (5-letter words)")
        print("2. Medium (6-7 letter words)")
        print("3. Hard (8+ letter words)")
        
        while True:
            choice = input("\nEnter your choice (1-3): ").strip()
            if choice in ['1', '2', '3']:
                return ['easy', 'medium', 'hard'][int(choice) - 1]
            else:
                print("Please enter a valid option (1, 2, or 3).")
    
    def get_random_word(self, difficulty):
        return random.choice(self.words[difficulty])
    
    def display_word_state(self, word, guessed_letters):
        display = ""
        for letter in word:
            if letter in guessed_letters:
                display += letter + " "
            else:
                display += "_ "
        return display.strip()
    
    def display_hangman(self, attempts_left):
        stages = [
            """
               -----
               |   |
               |   
               |   
               |   
               |   
            -------""",
            """
               -----
               |   |
               |   O
               |   
               |   
               |   
            -------""",
            """
               -----
               |   |
               |   O
               |   |
               |   
               |   
            -------""",
            """
               -----
               |   |
               |   O
               |  /|
               |   
               |   
            -------""",
            """
               -----
               |   |
               |   O
               |  /|\\
               |   
               |   
            -------""",
            """
               -----
               |   |
               |   O
               |  /|\\
               |  / 
               |   
            -------""",
            """
               -----
               |   |
               |   O
               |  /|\\
               |  / \\
               |   
            -------"""
        ]
        return stages[self.max_attempts - attempts_left]
    
    def get_hint(self, word, guessed_letters):
        # Find a letter in the word that hasn't been guessed yet
        unguessed_letters = [letter for letter in word if letter not in guessed_letters]
        if unguessed_letters:
            return random.choice(unguessed_letters)
        return None
    
    def calculate_score(self, word, attempts_left, hints_used, difficulty):
        base_score = len(word) * 10
        attempts_bonus = attempts_left * 5
        hints_penalty = hints_used * 15
        difficulty_bonus = {'easy': 1, 'medium': 1.5, 'hard': 2}[difficulty] * 20
        
        score = base_score + attempts_bonus - hints_penalty + difficulty_bonus
        return max(score, 0)  # Ensure score doesn't go negative
    
    def play_round(self):
        self.clear_screen()
        self.display_title()
        
        difficulty = self.choose_difficulty()
        word = self.get_random_word(difficulty)
        guessed_letters = set()
        attempts_left = self.max_attempts
        self.hints_used = 0
        
        print(f"\nA {difficulty} word has been selected. It has {len(word)} letters.")
        print("You have", attempts_left, "attempts to guess the word.")
        print("Type 'hint' for a hint (you have", self.max_hints, "available).")
        
        while attempts_left > 0:
            print("\n" + "="*50)
            print(self.display_hangman(attempts_left))
            print("\nWord:", self.display_word_state(word, guessed_letters))
            print(f"Attempts left: {attempts_left}")
            print(f"Hints used: {self.hints_used}/{self.max_hints}")
            print(f"Guessed letters: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")
            
            guess = input("\nEnter a letter or 'hint' for a hint: ").lower().strip()
            
            if guess == 'hint':
                if self.hints_used < self.max_hints:
                    hint_letter = self.get_hint(word, guessed_letters)
                    if hint_letter:
                        print(f"\n💡 Hint: The word contains the letter '{hint_letter}'")
                        self.hints_used += 1
                    else:
                        print("\nNo hints available - you've already guessed all letters!")
                else:
                    print("\nYou've used all your hints!")
                continue
            
            if len(guess) != 1 or not guess.isalpha():
                print("Please enter a single letter.")
                continue
            
            if guess in guessed_letters:
                print("You've already guessed that letter.")
                continue
            
            guessed_letters.add(guess)
            
            if guess in word:
                print(f"Good guess! '{guess}' is in the word.")
            else:
                print(f"Sorry, '{guess}' is not in the word.")
                attempts_left -= 1
            
            # Check if player has guessed all letters
            if all(letter in guessed_letters for letter in word):
                round_score = self.calculate_score(word, attempts_left, self.hints_used, difficulty)
                self.score += round_score
                
                print("\n" + "="*50)
                print("🎉 Congratulations! You guessed the word:", word.upper())
                print(f"📊 Round Score: {round_score}")
                print(f"🏆 Total Score: {self.score}")
                print(self.display_hangman(attempts_left))
                return True
        
        # Player ran out of attempts
        print("\n" + "="*50)
        print(self.display_hangman(attempts_left))
        print("💀 Game Over! The word was:", word.upper())
        print(f"🏆 Your total score: {self.score}")
        return False
    
    def play_game(self):
        self.clear_screen()
        self.display_title()
        
        print("Welcome to Word Quest!")
        print("Guess the hidden word one letter at a time.")
        print("Be careful - you only have 6 wrong guesses before the game ends!")
        
        input("\nPress Enter to start your adventure...")
        
        while True:
            if not self.play_round():
                break
            
            play_again = input("\nWould you like to play again? (y/n): ").lower().strip()
            if play_again not in ['y', 'yes']:
                break
        
        print(f"\nThanks for playing Word Quest! Your final score: {self.score}")
        print("Come back soon for more word adventures!")

# Run the game
if __name__ == "__main__":
    game = WordQuest()
    game.play_game()