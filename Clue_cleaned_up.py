import pandas as pd
import tkinter as tk
from tkinter import font
from tkinter import Scrollbar
from tkinter import *
import random as rd
import pandas as pd
import numpy as np
# Create groups for suspects, rooms and weapons
suspects = ['Colonel Mustard', 'Miss Scarlet', 'Mr. Green', 'Mrs. Peacock',
         'Mrs. White', 'Professor Plum']
rooms = ['The Study','Kitchen','Ballroom','Conservatory','Billiard Room','Library',
         'Hall','Lounge','Dining Room','Cellar']
weapons = ['Revolver','Dagger','Lead Pipe','Rope','Candlestick','Wrench']
pd.set_option('display.max_columns', None)

# combine to deal
deck = suspects + rooms + weapons
cards = deck.copy()

#Function to deal deck
def shuffle(number_players):
    # Create the solution list
    solution = []
    # Append random suspect card to solution
    solution.append(rd.sample(suspects, 1))
    # Remove that card from the deck
    deck.remove(solution[0][0])
    # Append random weapon card to solution
    solution.append(rd.sample(weapons, 1))
    # Remove that card from the deck
    deck.remove(solution[1][0])
    # Append random room card to solution
    solution.append(rd.sample(rooms, 1))
    # Remove that cacrd from the deck
    deck.remove(solution[2][0])

    # initialize a dictionary for the player cards
    p_cards = {}
    rd.shuffle(deck)

    # Create key for each player
    for num in range(number_players):
        p_cards["Player " + str(num+1)] = []
    j=1

    # Deal cards to each player
    for elem in deck:
        p_cards["Player " + str(j)].append(elem)
        if j==number_players:
            j=1
        else:
            j+=1
    return p_cards, solution

def calc_init_df(my_cards,rest_cards, playercards, sol):
    # Initialize the probability matrix with a column that includes all the cards in the game
    probability_matrix = pd.DataFrame(cards, columns = ["Cards"])

    # Chance of cards of card not being in the solution for each category
    susp_chance = 5 / 6
    loc_chance = 9 / 10
    weap_chance = 5 / 6

    # Create columns in the probability matrix dataframe for each player
    i = 1
    while i <= num_players:
        probability_matrix["Player_" + str(i)] = ""
        i += 1

    # Create initial probabilities for each card being in each players hand
    # start with k=2 since we won't worry about player 1 (your own hand), until below
    k = 2
    while k <= num_players:
        # create text to apply to the .loc function to place the probabilities in the right location
        column_text = "Player_" + str(k)

        # apply probabilities
        # the chance of the card not being in the solution (5/6,9/10,5/6), multiplied by the # of cards in the player's hand
        # and divide by the rest of the cards that are left after the # of cards in your hand and the solution (rest_cards)
        probability_matrix.loc[0:5, column_text]= susp_chance*(len(playercards["Player " + str(k)]) / rest_cards)
        probability_matrix.loc[6:15, column_text]= loc_chance*(len(playercards["Player " + str(k)]) / rest_cards)
        probability_matrix.loc[16:21, column_text]= weap_chance*(len(playercards["Player " + str(k)]) / rest_cards)
        k += 1

    # Create initial values for the solution
    value1 = [1 / 6] * 6
    value2 = [1 / 10] * 10
    value3 = [1 / 6] * 6
    solution_column = value1 + value2 + value3

    # Create solution column
    probability_matrix["Solution"] = solution_column

    # apply probabilities to the cards that I have in my hand (Player_1)
    for elem in my_cards:
        # find the row in the probability matrix dataframe where the card in your hand is
        j = probability_matrix.index[probability_matrix['Cards'] == elem]
        # Adjust the probability of that card being in your hand to 1
        probability_matrix["Player_1"][j]=1

        # adjust the other player's probabilities for that card to 0
        k = 2
        while k <= num_players:
            probability_matrix["Player_"+ str(k)][j]=0
            k+=1

        # Adjust solution to 0 for that card
        probability_matrix["Solution"][j] = 0

    # Replace all of player 1 open spots to 0 since the others have been filled with one
    probability_matrix["Player_1"]=probability_matrix["Player_1"].replace(to_replace = "", value = 0, regex = True)
    return probability_matrix

def new_guess(cards_guess,guessing_player,number_of_players,all_cards):
    z=1
    # Initialize intersect list
    intersect = []
    # Create a while loop that loops through players and stops when there is an intersect found
    while z <= number_of_players-1 and intersect ==[]:
        if guessing_player == number_of_players:
            guessing_player =1
        else:
            guessing_player += 1
        intersect = list(set(cards_guess) & set(all_cards["Player " + str(guessing_player)]))

        z+=1
        # Returns the intersect (all cards) and the player that guessing player(player who showed!)
    return intersect, guessing_player

def update_guess_matrix(list_guesses, shown_cards, player_number,player_showing,number_of_players):
    #Matrix of guesses
    list_of_guesses = list_guesses
    # If the player showing has more than 1 card, then they will show a random selection
    if len(shown_cards) >=1:
        shown_cards = rd.sample(shown_cards,1)
    else:
        pass

    list_of_guesses.at[guess_number,"Player_"+str(player_showing)] = shown_cards
    for player in range(number_of_players+1)[player_number+1:]:

        if pd.isna(list_of_guesses.at[guess_number,"Player_" + str(player)]):
            list_of_guesses.at[guess_number, "Player_" + str(player)] = 0
        else:
            break

    for player2 in range(number_of_players + 1)[1:player_showing]:
        if player_number > player_showing and pd.isna(list_of_guesses.at[guess_number,"Player_" + str(player2)]):
            list_of_guesses.at[guess_number, "Player_" + str(player2)] = 0
        else:
            break
    list_of_guesses = list_of_guesses.fillna(value = "NA")
    return list_of_guesses

def update_prob_matrix(sol_matrix, guesslist,which_guess,intersect_card):
    print(guesslist)
    length_of_guesslist = len(guesslist.columns)
    if guesslist.iloc[which_guess-1][0] == "Player_1":
        #search items 2,3,4
        col_index = 2
        while col_index <= length_of_guesslist-1:
            if guesslist.iloc[which_guess-1][col_index]==0:
                #needs to be fore all cards
                index_value1 = sol_matrix[sol_matrix['Cards'] == guesslist.iloc[which_guess - 1]["Guess"][0]].index[0]
                index_value2 = sol_matrix[sol_matrix['Cards'] == guesslist.iloc[which_guess - 1]["Guess"][1]].index[0]
                index_value3 = sol_matrix[sol_matrix['Cards'] == guesslist.iloc[which_guess - 1]["Guess"][2]].index[0]

                print("Index value is: ",index_value1)
                col_value = "Player_" + str(col_index)
                sol_matrix.at[index_value1,col_value]=0
                sol_matrix.at[index_value2,col_value]=0
                sol_matrix.at[index_value3,col_value]=0

                #sol_matrix.set_value(index, col_number, 10)

            elif guesslist.iloc[which_guess-1][col_index]=="NA":
                pass
            else:
                #need to get shown card
                index_value = sol_matrix[sol_matrix['Cards'] == guesslist.iloc[which_guess - 1][col_index][0]].index[0]
                print(index_value)
                col_value = "Player_" + str(col_index)
                sol_matrix.at[index_value, 1:] = 0
                sol_matrix.at[index_value,col_value]=1

            col_index+=1
    else:
        col_index = 2
        while col_index <= length_of_guesslist-1:
            index_value1 = sol_matrix[sol_matrix['Cards'] == guesslist.iloc[which_guess - 1]["Guess"][0]].index[0]
            print(index_value1)
            index_value2 = sol_matrix[sol_matrix['Cards'] == guesslist.iloc[which_guess - 1]["Guess"][1]].index[0]
            index_value3 = sol_matrix[sol_matrix['Cards'] == guesslist.iloc[which_guess - 1]["Guess"][2]].index[0]

            if guesslist.iloc[which_guess - 1][col_index] == 0:
                col_number = which_guess%num_players+col_index-1
                if col_number == 5:
                    col_number = 1
                elif col_number ==6:
                    col_number = 2
                elif col_number == 7:
                    col_number = 3
                else:
                    pass
                col_value = "Player_" + str(col_number)
                sol_matrix.at[index_value1, col_value] = 0
                sol_matrix.at[index_value2, col_value] = 0
                sol_matrix.at[index_value3, col_value] = 0
            else:
                pass
            col_index+=1
    for row_value, col_value in sol_matrix.iterrows():
        sum = 0
        for prob_value in col_value:
            if isinstance(prob_value,float)==TRUE or isinstance(prob_value,int) == TRUE:
                sum = sum+ prob_value
                print("the prob value is: ",prob_value)
                print("The sum is: ",sum)
            else:
                pass
         
        if sum < 0.99:

            #sum other solution values
            print("column index: ",len(sol_matrix.columns)-1)
            print("row_value: ", row_value)
            print("Suspects are: ", suspects)
            temp_sum = sol_matrix[0:6][sol_matrix.columns[len(sol_matrix.columns)-1]].sum()


            temp_sum = temp_sum-sol_matrix.at[row_value, sol_matrix.columns[len(sol_matrix.columns)-1]]
            print(temp_sum)
            # recalculate odds
            # (1-sum)*player_prob/sum(probs)
            column_index = 1
            for prob_value in col_value:
                if isinstance(prob_value, float) == TRUE or isinstance(prob_value, int) == TRUE:
                    new_prob = prob_value/sum
                    sol_matrix.at[row_value, sol_matrix.columns[column_index]] = new_prob
                    column_index = column_index +1

            # if row_value ==0:
            solution_row = 0
            while solution_row < row_value:
                sol_matrix.loc[solution_row,sol_matrix.columns[len(sol_matrix.columns)-1]] = (1-new_prob)*sol_matrix.loc[solution_row,sol_matrix.columns[len(sol_matrix.columns)-1]] /temp_sum
                solution_row=solution_row+1
            solution_row = solution_row + 1

            #elif row_value == 5:
            while solution_row > row_value and solution_row < 6:
                sol_matrix.loc[solution_row, sol_matrix.columns[len(sol_matrix.columns) - 1]] = (1-new_prob)*sol_matrix.loc[solution_row,sol_matrix.columns[len(sol_matrix.columns)-1]] /temp_sum
                solution_row = solution_row + 1
            # elif row_value > 0 and row_value < 5:
            #     sol_matrix.loc[0:row_value,sol_matrix.columns[len(sol_matrix.columns)-1]] = (1-sum)/5
            #     sol_matrix.loc[row_value+1:5,sol_matrix.columns[len(sol_matrix.columns)-1]] = (1-sum)/5

        else:
            pass
        #print("col val1: ",col_value[0])
        #print("col val2: ",col_value[1])
        #print("col val3: ",col_value[2])
        #print("col val4: ",col_value[3])
        #print("col val5: ",col_value[4])
        #print("col val6: ",col_value[5])

    return sol_matrix

num_players = int(input("How many players are playing?"))

# Call shuffle function to shuffle and deal cards
player_cards, solution = shuffle(num_players)

# get list of your own cards
me = list(player_cards.get("Player 1"))

# Obtain the number of cards outside of the solution and your hand
rest_cards = len(cards)-len(me)-3

# Create a solution dictionary
solution_cards = {'Solution': solution}
print(solution)
print(player_cards)

# Call the calc_init_df function to create and calculate an initial probability matrix
prob_matrix = calc_init_df(me, rest_cards, player_cards, solution_cards)
print(prob_matrix)
game = TRUE
k = 1
# guessing player
gp = 1
guess_number = 1

#Create initial guest list with player guessing and guess columns
guess_list = pd.DataFrame(columns = ["Player_guessing","Guess"])
# Create columns for each player
for col in range(num_players):
    guess_list["Player_" + str(col+1)] = ""

num_turn = 0
while game == TRUE:
    while k <= num_players:
        solve = input("Would you like to solve?")
        if solve == "Y" or solve == "y" or solve == "Yes" or solve == "yes":
            solution_guess = input("Enter your guess in the following format (suspect,weapon,room)\n").split(',')
            if solution_guess[0] == solution[0][0] and solution_guess[1] == solution[1][0] and solution_guess[2] == solution[2][0]:
                print("wow!")
                exit()
            else:
                print(solution)
        else:
            pass
        guess = input("Player " + str(k) + ", Enter guess in the following format (suspect,weapon,room)\n").split(',')
        intersect, showing_player = new_guess(guess,gp,num_players,player_cards)

        guess_list.at[guess_number,"Player_guessing"] = "Player_" + str(k)
        guess_list.at[guess_number,"Guess"] = guess

        guesslist2 = update_guess_matrix(guess_list,intersect,k,showing_player,num_players)
        prob_matrix = update_prob_matrix(prob_matrix,guesslist2,guess_number, intersect)
        print(prob_matrix)
        intersect = []

        guess_number+=1
        k+=1
        if gp == num_players:
            gp = 1
            num_turn +=1
        else:
            gp +=1

        if k ==num_players+1:
            k = 1
        else:
            pass
    game = FALSE

