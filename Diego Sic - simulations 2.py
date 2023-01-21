#Diego Sic
#This code creates evidence for the project 2

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


def approval(profile, approval_factor):
    '''This function takes a profile (2-D list) and
    integer to delimit the quanity of approvals a 
    voter can give. Then for each ballot in the profile
    takes the approvals of each voter randomly, but inside
    of the domain.
    Argument:
        profile (2-D list) and
        integer to delimit the quanity of approvals a 
        voter can give. 
    Return:
        If there's a tie of 3 candidates at the top will return
        a None. Otherwise, will return a list with the 2 winners'''   
    votes = []
    #This is the num of alternatives
    for i in range(len(profile[0])):
        votes_for_alternatives = 0
        #This is the number of voters
        for ballot in profile:
            if ballot.index(i) <= random.randint(0,approval_factor):
                votes_for_alternatives += 1
        votes.append(votes_for_alternatives)

    if votes.count(max(votes)) > 2:
        return None

    winners = sorted(range(len(votes)), key=lambda i: votes[i])[-2:]
    return winners
    
def main():
    option_for_num_of_voters = [50, 100, 150]
    domain_limitations = [5] 
    x_lists = option_for_num_of_voters

    #Storaging the data collected
    y_list = []                  
    for z in range(len(option_for_num_of_voters)):
        results_for_z_voters = []
        for j in range(len(domain_limitations)):
            #Settings
            num_voters = option_for_num_of_voters[z]
            num_alternatives = 40
            num_simulations = 10000
            #Result for each domain
            approval_winner_quantity = 0
            for i in range(num_simulations):
                profile = make_IC_profile(num_voters, num_alternatives)   
                w_approval = approval(profile, domain_limitations[j])      
                if w_approval  is not None:
                    approval_winner_quantity += 1
            print("done")
            results_for_z_voters.append(approval_winner_quantity/num_simulations)
        y_list.append(results_for_z_voters)

    print(y_list)
    description = [f"Approval limited to : {domain} per voter" for domain in domain_limitations]
    #Plotting the data   
    plt.plot(x_lists, y_list, marker='s')
    plt.xlabel("Number of voters")
    plt.ylabel("Percentage where there's no 3 winners tied at the top")
    plt.title("Resoluteness of using approval voting in the first round")
    plt.legend(description)
    fig = plt.gcf()
    fig.savefig("Resoluteness of using approval voting in the first round.png")
    plt.show()

if __name__ == "__main__":
    main()