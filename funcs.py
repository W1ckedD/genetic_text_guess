import random
import string

from chromosome import Chromosome


class GeneticFunction(object):
    def __init__(self, text, crossover_chance=0.8, mutation_chance=0.1, mutation_ri=0.1, population_count=20, generation_count=1000):
        self.charset = string.ascii_letters.join([' ', ',', '.', '!', '?'])
        self.text = text
        self.text_length = len(self.text)
        self.crossover_chance = crossover_chance
        self.mutation_chance = mutation_chance
        self.mutation_ri = mutation_ri
        self.population_count = population_count
        self.generation_count = generation_count
        self.guess_number = 0
        self.found_target_text = False
        self.population = self.generate_initial_population(self.population_count, self.text_length)
        pass
    
    def generate_initial_population(self, population_count, length):
        return [Chromosome(length) for _ in range(population_count)]


    def check_for_goal_state(self):
        self.guess_number += 1
        self.evaluate_popualtion()
        best_match = sorted(self.population, key=lambda chrom: chrom.heuristic_value, reverse=True)[0]
        report_str = f'Guess No: {self.guess_number}, Best Heuristic: {best_match.heuristic_value}, Best Match: {best_match.string}'
        print(report_str)
        if best_match.string == self.text:
            print('Found it!')
            self.found_target_text = True
    
    def evaluate_popualtion(self):
        for chrom in self.population:
            chrom.heuristic_value = self.heuristic_function(chrom)

    def heuristic_function(self, chrom):
        count = 0
        for i in range(self.text_length):
            if chrom.string[i] == self.text[i]:
                count += 1
        return count

    def selection(self):
        self.population = sorted(self.population, key=lambda chrom: chrom.heuristic_value, reverse=True)
        self.population = self.population[:int(0.5*self.population_count)]
        pass

    def crossover(self):
        children = []
        for _ in range((self.population_count - len(self.population)) // 2):
            chance = random.uniform(0, 1)
            if chance > self.crossover_chance:
                continue
            parent1 = random.choice(self.population)
            parent2 = random.choice(self.population)
            index1 = random.randint(2, len(parent1.string))
            index2 = random.randint(2, len(parent2.string))
            if index1 > index2:
                index1, index2 = index2, index1
            child1 = Chromosome(self.text_length)
            child2 = Chromosome(self.text_length)

            child1.string = parent1.string[:index1] + parent2.string[index1:index2] + parent1.string[index2:]
            child2.string = parent2.string[:index1] + parent1.string[index1:index2] + parent2.string[index2:]
            children.append(child1)
            children.append(child2)
        self.population.extend(children)
        
    def mutation(self):
        for chrom in self.population:
            chance = random.uniform(0, 1)
            if chance > self.mutation_chance:
                continue
            si = random.choice([-1, 1])
            ri = self.mutation_ri
            index = -2
            for i in range(len(chrom.string)):
                if chrom.string[i] != self.text[i]:
                    index = i
            mutated_letter = random.choice(self.charset)
            chrom.string = chrom.string[:index] + mutated_letter + chrom.string[index + 1:]