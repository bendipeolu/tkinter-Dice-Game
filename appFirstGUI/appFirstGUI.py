import tkinter as tk
import random

#################################################################################################################################################

class Player:
    
    def __init__(self, root):
        self.root = root
        self.balance = 0
        self.betting_amount = 0
        self.playstyle = None
        
        # LABELS AND BUTTONS
        self.account_label = tk.Label(self.root, text=f"Account Balance: {self.balance}")
        self.account_label.pack(anchor=tk.NW)

        self.withdraw_button = tk.Button(self.root, text="Withdraw", padx="20", pady="15", command=lambda :self.transaction_amount('Withdraw'))
        self.withdraw_button.pack(anchor=tk.NW)
        
        self.deposit_button = tk.Button(self.root, text="Deposit", padx="20", pady="15", command=lambda : self.transaction_amount('Deposit'))
        self.deposit_button.pack(anchor=tk.NW)
        
        self.fun_money_label = tk.Label(self.root, text=f'Would you like to play for money or for fun?')
        self.fun_money_label.pack(anchor=tk.NE)
        
        self.play_fun_button = tk.Button(self.root, text='For Fun!', padx='20', pady='15', command=self.create_playstyle)
        self.play_fun_button.pack(anchor=tk.NE)
        
        self.play_money_button = tk.Button(self.root, text='For Money!', padx='20', pady='15', command=self.place_bet)
        self.play_money_button.pack(anchor=tk.NE)

        self.playstyle_label = tk.Label(self.root)
        self.playstyle_label.pack()
        
        self.betting_amount_label = tk.Label(self.root)
        self.betting_amount_label.pack()
        
    
    # HANDLES WITHDRAWALS AND DEPOSITS
    def transaction_amount(self, type):
        if type == 'Withdraw' and self.balance <= 0:
            tk.Label(self.root, text='You have no money to withdraw').pack(anchor=tk.NW)
            return
        self.deposit_amount_label = tk.Label(self.root, text=f"How much would you like to {type}")
        self.deposit_amount_label.pack(anchor=tk.NW)

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(anchor=tk.NW)
            
        self.transaction_button = tk.Button(self.root, text="confirm", padx="20", pady="15", command=lambda : self.transaction(int(self.amount_entry.get()), type))
        self.transaction_button.pack(anchor=tk.NW)
                
    def transaction(self, amount, type):
        if type == 'Withdraw' and amount > self.balance:
            self.deposit_amount_label.config(text='Your account balance is too low to make a withdrawl of this size')
            return
        if type == 'Withdraw':
            amount *= -1
        self.balance += amount
        self.transaction_button.destroy()
        self.amount_entry.destroy()
        self.deposit_amount_label.destroy()
        self.account_label.config(text=f"Your balance is {self.balance}")
        

    # SETS PLAYSTYLE TO SHOW WHETHER PLAYER WILL USE MONEY        
    def create_playstyle(self, style = 'Fun'):
        self.playstyle = style
        self.playstyle_label.config(text=f'Playing for {self.playstyle}')
        
        if style == 'Money':
            self.betting_amount_label.config(text=f'Betting Amount: {self.betting_amount}')
        else:
            self.betting_amount = 0
            self.betting_amount_label.config(text='')
        
        
    # PLACING BET WHEN 'PLAYING FOR MONEY'
    def place_bet(self):
        self.enter_amount_label = tk.Label(self.root, text='Please enter your betting amount')
        self.enter_amount_label.pack(anchor=tk.NE)

        self.betting_entry = tk.Entry(self.root)
        self.betting_entry.pack(anchor=tk.NE)

        self.submit_betting_button = tk.Button(self.root, text="confirm", padx="20", pady="15", command=lambda: self.confirm_bet())
        self.submit_betting_button.pack(anchor=tk.NE)

    def confirm_bet(self):
        
        try:
            amount = int(self.betting_entry.get())
        except ValueError:
            self.enter_amount_label.config(text="Invalid betting amount")
            return
        
        self.betting_amount = amount
        self.enter_amount_label.destroy()
        self.betting_entry.destroy()
        self.submit_betting_button.destroy()

        self.create_playstyle('Money')


#################################################################################################################################################

class Dice:
    def __init__(self, root):
        # SAVES IMAGES IN MEMORY
        self.dice_images = {
            1: tk.PhotoImage(file="C:\\Users\\ICTLearner04\\Desktop\\dice\\10826863.png"),
            2: tk.PhotoImage(file="C:\\Users\\ICTLearner04\\Desktop\\dice\\10826864.png"),
            3: tk.PhotoImage(file="C:\\Users\\ICTLearner04\\Desktop\\dice\\10826865.png"),
            4: tk.PhotoImage(file="C:\\Users\\ICTLearner04\\Desktop\\dice\\10826866.png"),
            5: tk.PhotoImage(file="C:\\Users\\ICTLearner04\\Desktop\\dice\\1626822.png"),
            6: tk.PhotoImage(file="C:\\Users\\ICTLearner04\\Desktop\\dice\\10826868.png")
        }
        
        self.root = root
        self.dice_face = tk.Label(self.root)
        self.dice_face.pack()
        
    def roll_dice(self):
        rolled_value = random.randint(1, 6)
        
        self.photo = self.dice_images[rolled_value]

        self.dice_face.config(image=self.photo)
        
        return rolled_value


##############################################################################################################################


class DiceGame:
    def __init__(self, root, player, dice):
        self.root = root
        self.root.title('Dice Game')
        self.root.geometry('600x600')
        self.dice = dice
        self.player = player
        
        # LABELS AND BUTTONS
        self.guess_label = tk.Label(self.root, text="Guess the roll (1-6):")
        self.guess_label.pack()

        self.guess_entry = tk.Entry(self.root)
        self.guess_entry.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

        self.my_button = tk.Button(root, text="Roll Dice", padx="20", pady="15", command=self.check_guess)
        self.my_button.pack()
        
        
    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            self.result_label.config(text="Invalid guess. Please enter a number.")
            return
        
        rolled_value = self.dice.roll_dice()

        if guess == rolled_value:
            self.result_label.config(text="Congratulations! Your guess is correct!")
            
            winnings = self.player.betting_amount * 5
            self.player.balance += winnings
            self.player.account_label.config(text=f"Your balance is {self.player.balance}")
            
            win_screen = tk.Tk()
            tk.Label(win_screen, text=f'Congratulations you won {winnings}!').pack()
            win_screen.mainloop()
            
        else:
            self.result_label.config(text=f"Sorry, your guess ({guess}) is incorrect. The correct roll was {rolled_value}.")
            self.player.balance -= self.player.betting_amount
            self.player.account_label.config(text=f"Your balance is {self.player.balance}")
            

###########################################################################################################################################




def main():
    root = tk.Tk()
    player = Player(root)
    dice = Dice(root)
    game = DiceGame(root, player, dice)
    
    game.root.mainloop()

main()
