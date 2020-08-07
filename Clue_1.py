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
    i = 1
    while i <= num_players:
        probability_matrix["Player_" + str(i)] = ""
        i += 1
    for elem in my_cards:
        j = probability_matrix.index[probability_matrix['Cards'] == elem]
        probability_matrix["Player_1"][j]=1
        k = 2
        while k <= num_players:
            probability_matrix["Player_"+ str(k)][j]=0
            k+=1
    probability_matrix["Player_1"]=probability_matrix["Player_1"].replace(to_replace = "", value = 0, regex = True)
    k = 2
    while k <= num_players:
        probability_matrix["Player_" + str(k)] = probability_matrix["Player_" + str(k)].replace(to_replace = "", value = len(playercards["Player " + str(k)])/rest_cards, regex = True)
        k += 1
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

    #print(list_of_guesses,"\n",solution_matrix)
    return list_of_guesses

num_players = int(input("How many players are playing?"))
me,you, them, other, solution = shuffle(num_players)
rest_cards = len(cards)-len(me)

print("My cards: ",me)

player_cards = {'Player 1': me, 'Player 2': you, 'Player 3': them, 'Player 4': other}
solution_cards = {'Solution': solution}
print(solution)
print(player_cards)
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

