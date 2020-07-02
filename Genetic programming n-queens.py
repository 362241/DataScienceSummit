import random

class Solver:

    
    @staticmethod
    def create(n):
        return Solver(n)

    def __init__(self, n):
        self.nq = n
        self.maxFitness= (nq*(nq-1))/2  # 8*7/2 = 28

    def random_chromosome(self): #making random chromosomes 
        return [ random.randint(1, nq) for _ in range(nq) ]

    def generate_initial_population(self): #generate initial population
        return [self.random_chromosome() for _ in range(100)]

    def fitness(self,chromosome):
        horizontal_collisions = sum([chromosome.count(queen)-1 for queen in chromosome])/2
        diagonal_collisions = 0

        n = len(chromosome)
        left_diagonal = [0] * 2*n
        right_diagonal = [0] * 2*n
        for i in range(n):
            left_diagonal[i + chromosome[i] - 1] += 1
            right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

        diagonal_collisions = 0
        for i in range(2*n-1):
            counter = 0
            if left_diagonal[i] > 1:
                counter += left_diagonal[i]-1
            if right_diagonal[i] > 1:
                counter += right_diagonal[i]-1
            diagonal_collisions += counter / (n-abs(i-n+1))
        
        return int(self.maxFitness - (horizontal_collisions + diagonal_collisions)) #28-(2+3)=23

    def probability(self,chromosome, fitness):
        return self.fitness(chromosome) / self.maxFitness

    def random_pick(self,population, probabilities):
        populationWithProbabilty = zip(population, probabilities)
        total = sum(w for c, w in populationWithProbabilty)
        r = random.uniform(0, total)
        upto = 0
        for c, w in zip(population, probabilities):
            if upto + w >= r:
                return c
            upto += w
        assert False, "Shouldn't get here"
            
    def reproduce(self,x, y): #doing cross_over between two chromosomes
        n = len(x)
        c = random.randint(0, n - 1)
        return x[0:c] + y[c:n]

    def mutate(self,x):  #randomly changing the value of a random index of a chromosome
        n = len(x)
        c = random.randint(0, n - 1)
        m = random.randint(1, n)
        x[c] = m
        return x

    def genetic_queen(self,population, fitness):
        mutation_probability = 0.03
        new_population = []
        probabilities = [self.probability(n, self.fitness) for n in population]
        for i in range(len(population)):
            x = self.random_pick(population, probabilities) #best chromosome 1
            y = self.random_pick(population, probabilities) #best chromosome 2
            child = self.reproduce(x, y) #creating two new chromosomes from the best 2 chromosomes
            if random.random() < mutation_probability:
                child = self.mutate(child)
            # print_chromosome(child)
            new_population.append(child)
            if self.fitness(child) == self.maxFitness: break
        return new_population

    def print_chromosome(self,chrom):
        print("Chromosome = {},  Fitness = {}"
            .format(str(chrom), self.fitness(chrom)))

    def solve(self):
       
        population = self.generate_initial_population()
        
        generation = 1

        while not self.maxFitness in [self.fitness(chrom) for chrom in population]:
            print("=== Generation {} ===".format(generation))
            population = self.genetic_queen(population, self.fitness)
            print("")
            print("Maximum Fitness = {}".format(max([self.fitness(n) for n in population])))
            generation += 1
        chrom_out = []
        print("Solved in Generation {}!".format(generation-1))
        for chrom in population:
            if self.fitness(chrom) == self.maxFitness:
                print("");
                print("One of the solutions: ")
                chrom_out = [8-item for item in chrom]
                self.print_chromosome(chrom_out)


    

if __name__ == '__main__':
    nq = int(input("Enter Number of Queens: ")) #say N = 8
    solver = Solver.create(nq)
    solver.solve()
