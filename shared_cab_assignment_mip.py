from ortools.linear_solver import pywraplp
from array import *
import numpy as np


def main():
    # calculate the cost of current riders and cabs
    costs = calulate_cost()
    # costs = [
    #     [45, 40, 51, 67],
    #     [55, 40, 61, 53],
    #     [49, 52, 48, 64],
    #     [41, 45, 60, 55]
    # ]

    num_cabs = len(costs)
    num_riders = len(costs[0])

    # Solver
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    # x[i, j] is an array of 0-1 variables, which will be 1
    # if cab i is assigned to rider j.
    x = {}
    for i in range(num_cabs):
        for j in range(num_riders):
            x[i, j] = solver.IntVar(0, 1, '')

    # Constraints
    # Each cab is assigned to at most 1 rider.
    for i in range(num_cabs):
        solver.Add(solver.Sum([x[i, j] for j in range(num_riders)]) <= 1)

    # Each rider is assigned to exactly one cab.
    for j in range(num_riders):
        solver.Add(solver.Sum([x[i, j] for i in range(num_cabs)]) == 1)

    # Objective
    objective_terms = []
    for i in range(num_cabs):
        for j in range(num_riders):
            objective_terms.append(costs[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    # Solve
    status = solver.Solve()

    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f'Total cost = {solver.Objective().Value()}\n')
        for i in range(num_cabs):
            for j in range(num_riders):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if x[i, j].solution_value() > 0.5:
                    print(f'Cab {i} assigned to Rider {j}.' +
                          f' Cost: {costs[i][j]}')
    else:
        print('No solution found.')


def calulate_cost():
    # cab information model with attributes

    # time rate 1 INR for minute
    time_rate = 1

    # traveling cost INR 10 per KM to taxi company
    traveling_cost = 10

    # three weights adjusted as per business context
    w1 = 1
    w2 = 1
    w3 = 1

    #current cabs list with properties
    current_cabs_list = [
        {0: 'cab0', 'properties': {'route': 0, 'rating': 4, 'occupancy': 0}},
        {1: 'cab1', 'properties': {'route': 0, 'rating': 4.4, 'occupancy': 1}},
        {2: 'cab2', 'properties': {'route': 0, 'rating': 3, 'occupancy': 0}},
        {3: 'cab3', 'properties': {'route': 0, 'rating': 5, 'occupancy': 3}},
    ]

    # current riders cab requests with properties
    riders_list = [
        {0: 'rider0', 'properties': {'source': '27.2046,78.01',
                                        'destination': '28.196930, 50.477644', 'distance': 10, 'route': 0}},
        {1: 'rider1', 'properties': {'source': '28.48,77.23',
                                        'destination': '26.196930, 51.5621', 'distance': 11, 'route': 0}},
        {2: 'rider2', 'properties': {'source': '27.67,73.45',
                                        'destination': '26.9873, 52.3267', 'distance': 5, 'route': 0}},
        {3: 'rider3', 'properties': {'source': '24.04,75.43',
                                        'destination': '26.5431, 51.644', 'distance': 6, 'route': 0}},
    ]

    # de-tour distance from cab to rider in KM
    detour_distance = [
        [1, 1, 3, 5],
        [3, 4, 1, 1],
        [1, 4, 6, 2],
        [0, 1, 3, 5]
    ]

    # de-tour time from cab to rider in minutes
    detour_time = [
        [2, 3, 1, 3],
        [5, 4, 7, 3],
        [6, 4, 7, 5],
        [0, 2, 8, 10]
    ]
    # calculate the cost
    cost_array = []
    for i, cab in enumerate(current_cabs_list): 
        cost_array.append([])
        for j, rider in enumerate(riders_list):    
            distance = riders_list[j]['properties']['distance']      
            cost = w1 * (traveling_cost*distance) +  w2*(detour_distance[i][j]) + w3 * (detour_time[i][j])
            cost_array[i].append(cost)
    print("Cost Matrix")        
    print(np.matrix(cost_array))
    return cost_array


if __name__ == '__main__':
    main()
