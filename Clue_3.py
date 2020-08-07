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
#Deal deck
def shuffle(number_players):
    i = 1
    player_1 = []
    player_2 = []
    player_3 = []
    player_4 = []
    player_5 = []
    player_6 = []
    solution = []
    solution.append(rd.sample(suspects, 1))
    deck.remove(solution[0][0])
    solution.append(rd.sample(weapons, 1))
    deck.remove(solution[1][0])
    solution.append(rd.sample(rooms, 1))
    deck.remove(solution[2][0])

    rd.shuffle(deck)

    if number_players == 3:
        for elem in deck:
            if i == 1:
                player_1.append(elem)
                i+=1
            elif i == 2:
                player_2.append(elem)
                i +=1
            elif i==3:
                player_3.append(elem)
                i = 1
    elif number_players == 4:
        for elem in deck:
            if i == 1:
                player_1.append(elem)
                i+=1
            elif i == 2:
                player_2.append(elem)
                i +=1
            elif i==3:
                player_3.append(elem)
                i +=1
            elif i==4:
                player_4.append(elem)
                i = 1
    elif number_players == 5:
        for elem in deck:
            if i == 1:
                player_1.append(elem)
                i += 1
            elif i == 2:
                player_2.append(elem)
                i += 1
            elif i == 3:
                player_3.append(elem)
                i += 1
            elif i == 4:
                player_4.append(elem)
                i += 1
            elif i == 5:
                player_5.append(elem)
                i = 1
    elif number_players == 6:
        for elem in deck:
            if i == 1:
                player_1.append(elem)
                i += 1
            elif i == 2:
                player_2.append(elem)
                i += 1
            elif i == 3:
                player_3.append(elem)
                i +=1
            elif i == 4:
                player_4.append(elem)
                i += 1
            elif i == 5:
                player_5.append(elem)
                i += 1
            elif i == 6:
                player_6.append(elem)
                i = 1
    return player_1, player_2, player_3, player_4, solution

def calc_init_df(my_cards,rest_cards, playercards, sol):
    probability_matrix = pd.DataFrame(cards, columns = ["Cards"])
    # Chance of cards being available (not in solution)
    susp_chance = 5 / 6
    loc_chance = 9 / 10
    weap_chance = 5 / 6
    i = 1

    while i <= num_players:
        probability_matrix["Player_" + str(i)] = ""
        i += 1
    k = 2
    while k <= num_players:
        column_text = "Player_" + str(k)
        #probability_matrix["Player_" + str(k)] = probability_matrix.loc[0:5,column_text].replace(to_replace = "", value = len(playercards["Player " + str(k)])/rest_cards, regex = True)
        probability_matrix.loc[0:5, column_text]= susp_chance*(len(playercards["Player " + str(k)]) / rest_cards)
        probability_matrix.loc[6:15, column_text]= loc_chance*(len(playercards["Player " + str(k)]) / rest_cards)
        probability_matrix.loc[16:21, column_text]= weap_chance*(len(playercards["Player " + str(k)]) / rest_cards)

        k += 1

    for elem in my_cards:
        j = probability_matrix.index[probability_matrix['Cards'] == elem]
        probability_matrix["Player_1"][j]=1
        k = 2
        while k <= num_players:
            probability_matrix["Player_"+ str(k)][j]=0
            k+=1
    probability_matrix["Player_1"]=probability_matrix["Player_1"].replace(to_replace = "", value = 0, regex = True)

    value1 = [1/6]*6
    value2 = [1/10]*10
    value3 = [1/6]*6
    solution_column = value1 + value2 + value3

    probability_matrix["Solution"] = solution_column
    for elem in my_cards:
        j = probability_matrix.index[probability_matrix['Cards'] == elem]
        probability_matrix["Solution"][j]=0
    return probability_matrix

def new_guess(cards_guess,guessing_player,number_of_players,all_cards):
    cards_guess = cards_guess
    number_of_players = number_of_players
    all_cards = all_cards
    guessing_player = guessing_player
    z=1
    intersect = []
    while z <= number_of_players-1 and intersect ==[]:
        if guessing_player == number_of_players:
            guessing_player =1
        else:
            guessing_player += 1
        intersect = list(set(cards_guess) & set(all_cards["Player " + str(guessing_player)]))

        z+=1
    return intersect, guessing_player

def update_guess_matrix(list_guesses, shown_cards,solution_matrix, player_number,player_showing):
    #Matrix of guesses
    list_of_guesses = list_guesses
    if len(shown_cards) >=1:
        shown_cards = rd.sample(shown_cards,1)
    else:
        pass
    if player_showing == player_number+1 or (player_showing == 1 and player_number ==4):
        list_of_guesses.at[guess_number, "next_player_shows"] = shown_cards
    elif player_showing == player_number+2 or player_showing == player_number -2:
        list_of_guesses.at[guess_number, "next+1_player_shows"] = shown_cards
        list_of_guesses.iloc[guess_number-1:guess_number,2:3] = list_of_guesses.iloc[guess_number-1:guess_number,2:3].replace(np.nan, 0)
    elif player_showing == player_number+3 or player_showing == player_number -1:
        list_of_guesses.at[guess_number, "next+2_player_shows"] = shown_cards
        list_of_guesses.iloc[guess_number-1:guess_number,2:4] = list_of_guesses.iloc[guess_number-1:guess_number,2:4].replace(np.nan, 0)
    list_of_guesses = list_of_guesses.fillna(value = "NA")
    #print(list_of_guesses,"\n",solution_matrix)
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
me,you, them, other, solution = shuffle(num_players)
rest_cards = len(cards)-len(me)-3

print("My cards: ",me)

player_cards = {'Player 1': me, 'Player 2': you, 'Player 3': them, 'Player 4': other}
solution_cards = {'Solution': solution}
print(solution)
print(type(player_cards))
prob_matrix = calc_init_df(me, rest_cards, player_cards, solution_cards)
print(prob_matrix)
game = TRUE
k = 1
gp = 1
guess_number = 1
guess_list = pd.DataFrame(columns = ["Player_guessing","Guess","next_player_shows","next+1_player_shows","next+2_player_shows"])
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
        intersect, player_guessing = new_guess(guess,gp,num_players,player_cards)
        guess_column = "Player_" + str(k) + "_Guess"
        print(intersect)
        guess_list.at[guess_number,"Player_guessing"] = "Player_" + str(k)
        guess_list.at[guess_number,"Guess"] = guess
        guesslist2 = update_guess_matrix(guess_list,intersect,prob_matrix,k,player_guessing)
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

