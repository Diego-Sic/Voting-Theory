import copy
import random

def make_IC_profile(num_voters: int, num_alternatives:int):
  alternatives = list(range(num_alternatives))
  profile = []
  for i in range(num_voters):
      random.shuffle(alternatives)
      profile.append(copy.copy(alternatives))
  return profile

def matrix(profile):
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
    for i in range(len(matrix_1)):
        if sum(matrix_1[i]) == len(matrix_1)-1:
            return i
    return None

def copeland(matrix_1):
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

    
def main():
    #Settings
    num_voters = 10
    num_alternatives = 4
    num_simulations = 100000
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

            
    print(f"How many condorcet winner we have :{condorcet_winner_count}/{num_simulations}")
    print(f'''How many times condorcet, 
            and borda choose the same winner: {condorcet_borda}/{condorcet_winner_count}''')
    print(f'''How many times condorcet, 
            and plurality choose the same winner: {condorcet_plurality}/{condorcet_winner_count}''')
    print(f'''How many times plurality, borda 
            and copeland choose the same winner: {co_plu_bor_winner}/{num_simulations - condorcet_winner_count}''')


if __name__ == "__main__":
    main()
