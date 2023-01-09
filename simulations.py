import copy
import random
from matplotlib import pyplot as plt
import numpy as np

def make_IC_profile(num_voters: int, num_alternatives:int):
    '''This part will create an Impartial Culture election
    using a fixed amount of voters and alternatives
    Argument:
        This will recieve a integer describing the number of voters
        and integer descrbing the number of alternatives to choose
    Return:
        will return a 2-D with the len of the list will be the
        number of voters, and the length of each list will be
        the number of alternatives'''
    alternatives = list(range(num_alternatives))
    profile = []
    for i in range(num_voters):
        random.shuffle(alternatives)
        profile.append(copy.copy(alternatives))
    return profile

def matrix(profile):
    '''This function will create a Matrix using the number of 
    alternatives we have, the function storage in each position 
    if the alternative is in the loop won or lost against all the
    other alternatives
    Argument:
        A list with the ballots (profile)
    Return:
        A 2-D with the results of each alternative
        against all the rest of alternatives'''
    data_base_matrix = []
    for i in range(len(profile[0])):
        results = []
        for j in range(len(profile[0])):
            i_votes = 0
            j_votes = 0
            if i == j:
                results.append(0)
                continue
            for ballot in profile:
                if ballot.index(i) < ballot.index(j):
                    i_votes += 1
                else:
                    j_votes += 1

            if i_votes > j_votes:
                results.append(1)
            else:
                results.append(-1)
        data_base_matrix.append(results)

    return data_base_matrix

def condercet(matrix_1):
    '''This function will receive a matrix where each
    row of it, is the number of time it won against each
    alternative if there's a winner against all the other
    alternatives will return that winner if there's not winner
    will return None
    Argument:
        A 2-D list in form of a Matrix
    Return:
        A winner or a None'''
    for i in range(len(matrix_1)):
        if sum(matrix_1[i]) == len(matrix_1)-1:
            return i
    return None

def copeland(matrix_1):
    '''This function will receive a Matrix and will sum
    how many times each alternative won and storage that sum in a list
    and the end of the loop, will return the alternative with the highest
    sum
    Argument:
        Matrix
    Return:
        A winner'''
    results_alternatives = []
    for i in range(len(matrix_1)):
        results_alternatives.append(sum(matrix_1[i]))

    index_max = max(results_alternatives)
    if results_alternatives.count(index_max) > 1:
    # There are two or more maximum numbers in the list, so return None
        winner = None
    else:
    # There is only one maximum number in the list, so return it
        winner = index_max
    winner = results_alternatives.index(index_max)
    return winner

def plurality(profile):
    '''This function will check how many times each option
    is selected as the first option for the voters, and will return
    the one that has been selected the most
    Argument:
        A profile, a list with lists inside describing the order
        of preference of every voter
    Return:
        An alternative (int) as a winner'''
    votes = []
    #This is the num of alternatives
    for i in range(len(profile[0])):
        votes_for_alternatives = 0
        #This is the number of voters
        for j in range(len(profile)):
            if profile[j][0] == i:
                votes_for_alternatives += 1
        votes.append(votes_for_alternatives)
    index_max = max(votes)
    if votes.count(index_max) > 1:
    # There are two or more maximum numbers in the list, so return None
        winner = None
    else:
    # There is only one maximum number in the list, so return it
        winner = index_max
    winner = votes.index(index_max)
    return winner

def borda(profile):
    '''This function will use the Borda method if weight
    to weighted all the alternatives and return the one 
    that has highest sum
    Argument:
        A profile, a list with lists inside describing the order
        of preference of every voter
    Return:
        A integer describing the winner'''
    bordas_results = []
    for i in range(len(profile[0])):
        scores_of_alternative = 0
        for ballot in profile:
            alternatives_index = ballot.index(i)
            value = (len(profile[0]) - (alternatives_index + 1))
            scores_of_alternative += value
        bordas_results.append(scores_of_alternative)
    index_max = max(bordas_results)
    if bordas_results.count(index_max) > 1:
    # There are two or more maximum numbers in the list, so return None
        winner = None
    else:
    # There is only one maximum number in the list, so return it
        winner = index_max
    winner = bordas_results.index(index_max)
    return winner
#The axis-x has to be the voters
#The axis-y has to be the percentage of coincidence
#Each line has to be the number of alternatives

    
def main():
    option_for_num_of_voters = [10, 25, 50]
    option_for_num_of_alternatives = [2,3,10]
    x_lists = option_for_num_of_voters
    y_lists_condorcet_existence = []
    y_lists_condorcet_borda = []
    y_lists_condorcet_plurality = []
    for z in range(len(option_for_num_of_voters)):
        results_for_z_voters = []
        results_for_z_voters_borda = []
        results_for_z_voters_plurality = []
        for j in range(len(option_for_num_of_alternatives)):
            #Settings
            num_voters = option_for_num_of_voters[z]
            num_alternatives = option_for_num_of_alternatives[j]
            num_simulations = 10000
            condorcet_winner_count = 0
            condorcet_plurality = 0
            condorcet_borda = 0
            co_plu_bor_winner = 0
            #Creating profile
            for i in range(num_simulations):
                profile = make_IC_profile(num_voters, num_alternatives)
                matrix_profile = matrix(profile)
                condorcet_winner = condercet(matrix_profile)
                if condorcet_winner is not None:
                    condorcet_winner_count += 1
                    if condorcet_winner == borda(profile):
                        condorcet_borda += 1
                    if condorcet_winner == plurality(profile):
                        condorcet_plurality += 1
                else:
                    copeland_winner = copeland(matrix_profile)
                    plurality_winner = plurality(profile)
                    borda_winner = borda(profile)
                    if copeland_winner == plurality_winner == borda_winner:
                        co_plu_bor_winner += 1
            
            results_for_z_voters.append(condorcet_winner_count/num_simulations)
            results_for_z_voters_borda.append(condorcet_borda/condorcet_winner_count)
            results_for_z_voters_plurality.append(condorcet_plurality/condorcet_winner_count)

        y_lists_condorcet_existence.append(results_for_z_voters)
        y_lists_condorcet_borda.append(results_for_z_voters_borda)
        y_lists_condorcet_plurality.append(results_for_z_voters_plurality)

    description = [f"Alternatives = {option}" for option in option_for_num_of_alternatives]

    #Plotting the graph of condorcet Existence
    print(x_lists)
    print(y_lists_condorcet_existence)
    plt.plot(x_lists, y_lists_condorcet_existence, marker='s')
    plt.xlabel("Number of voters")
    plt.ylabel("Percentage of existence")
    plt.title("Condorcet winner existence")
    plt.legend(description)
    fig = plt.gcf()
    fig.savefig("Condorcet winner existence.png")

    #Plotting the graph of Borda matching with Condorcet
    print(x_lists)
    print(y_lists_condorcet_borda)
    plt.plot(x_lists, y_lists_condorcet_borda, marker='s')
    plt.xlabel("Number of voters")
    plt.ylabel("Percentage of existence")
    plt.title("Condorcet and Borda coincidence")
    plt.legend(description)
    fig = plt.gcf()
    fig.savefig("Condorcet and Borda coincidence.png")

    #Plotting the graph of Borda matching with Condorcet
    print(x_lists)
    print(y_lists_condorcet_borda)
    plt.plot(x_lists, y_lists_condorcet_borda, marker='s')
    plt.xlabel("Number of voters")
    plt.ylabel("Percentage of existence")
    plt.title("Condorcet and Borda coincidence")
    plt.legend(description)
    fig = plt.gcf()
    fig.savefig("Condorcet and Borda coincidence.png")



if __name__ == "__main__":
    main()