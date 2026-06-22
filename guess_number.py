import random
Easy_Level=10
Hard_Level=5
def set_difficulty(level_chosen):
    if level_chosen=='hard':
        return Hard_Level
    elif level_chosen=='easy':
        return Easy_Level
    else:
        return

def check_answer(guessed_number,answer,attempts):
    if guessed_number<answer:
        print("Your Guess is too low")
        return attempts-1
    elif guessed_number>answer:
        print("Your Guess is too high")
        return attempts-1
    else:
        print(f"Your Guess is right. The answer is {answer}")
def game():
    print("Let me think of number between 1 to 50")
    answer= random.randint(1,50)
    level=input("choose level of difficulty type 'easy' or 'hard'")
    attempts=set_difficulty(level)
    if attempts != Easy_Level and Hard_Level:
        print("You have entered wrong difficulty level... Play Again!")
        return
    guessed_number=0
    while guessed_number!=answer:
         print(f"You have{attempts} attempts remaining to guess the number")
         guessed_number=int(input("Guess number"))
         attempts=check_answer(guessed_number,answer,attempts)
         if attempts==0:
             print("You are out of guesses..You lose")
             return
         elif guessed_number!=answer:
             print("Guess number")

game()