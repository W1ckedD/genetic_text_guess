from funcs import GeneticFunction


if __name__ == '__main__':
    example = GeneticFunction("To be or not to be...")
    while not example.found_target_text:
        example.check_for_goal_state()
        example.selection()
        example.crossover()
        example.mutation()
