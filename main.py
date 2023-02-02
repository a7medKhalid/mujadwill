#create section class

class Section:
    def __init__(self, id, course_symbol, course_id, section, is_theory, course_title, start_time, end_time, days_type):
        self.id = id
        self.course_symbol = course_symbol
        self.course_id = course_id
        self.section = section
        self.is_theory = is_theory
        self.course_title = course_title
        self.start_time = start_time
        self.end_time = end_time
        self.days_type = days_type
        self.instructor = None

    def __str__(self):
        return self.course_symbol + ' ' + self.course_id + ' ' + self.section + ' ' + self.course_title + ' ' + str(self.start_time) + ' ' + str(self.end_time) + ' ' + self.days_type

class Instructor:
    def __init__(self, id, name, max_hours):
        self.id = id
        self.name = name
        self.max_hours = max_hours
    
    def __str__(self):
        return self.name

        
        

# import csv file
import pandas as pd
def importSections():
    # import arabic xlsx file
    data = pd.read_excel('mujadwill.xlsx')

    # create list of sections
    sections = []

    # loop through each row
    for index, row in data.iterrows():

        # get the days type
        # concatenate the days type

        days_type = str(row['الاحد']) + str(row['الاثنين']) + str(row['الثلاثاء']) + str(row['الأربعاء']) + str(row['الخميس'])
        # remove n letter from the days type
        days_type = days_type.replace('nan', '')
        
        # check if the section is theory or lab
        if row['رمز الجدولة'] == 'L':
            is_theory = True
        else:
            is_theory = False
        
        # create section object
        section = Section(row['م'], row['المقرر'], row['رقمه'], row['الشعبة'], is_theory, row['عنوان المقرر'], row['البداية'], row['النهاية'], days_type)

        # append the section to the list
        sections.append(section)

    return sections


# enum for fitness 

from enum import Enum
class Fitness(Enum):
    CONFLICT = 3
    FULL_LOAD = 2
    FOUR_DAYS = 1

       
class Helpers:

    def calculateConflict(self, section, instructorSections):
        conflict = False
        for sec in instructorSections:
            conflict = False
            days_type = sec.days_type
            startTime = sec.start_time
            endTime = sec.end_time
            if section.days_type == days_type and section.start_time == startTime and section.end_time == endTime:
                conflict = True
                break
                
        if conflict:
            return 0
        else:
            return Fitness.CONFLICT.value

    def calculateFullLoad(self, section, instructorSections):
        instructorSections.append(section)
        instructor = section.instructor
        instructorHours = 0
        for sec in instructorSections:
            instructorHours += sec.end_time - sec.start_time

        if instructorHours > instructor.max_hours:
            return 0
        else:
            return Fitness.FULL_LOAD.value
    
    def calculateFourDays(self, section, instructorSections):
        instructorSections.append(section)
        instructorDays = []
        for sec in instructorSections:
            days_type = sec.days_type
            # remove spaces from the days type
            days_type = days_type.replace(' ', '')
            for day in days_type:
                if day not in instructorDays:
                    instructorDays.append(day)

        if len(instructorDays) > 4:
            return 0
        else:
            return Fitness.FOUR_DAYS.value


import random

class GeneticAlgorithm:
    
    def generatePopulation(self, sections_list, instructors_list):
        # create list of sections with instructors
        population = []

        for s in sections_list:
            # select random instructor
            random_instructor = random.choice(instructors_list)
            s.instructor = random_instructor
            
            population.append(s)

        return population

    def calculateFitness(self,population):

        
        fitness = 0
        ranked_population = []
        conflict_fitness = 0
        fullLoad_fitness = 0
        fourDays_fitness = 0

        counter = 0

        # remove last item from the list
        
        for section in population:

            if section == None:
                break
            
            instructor = section.instructor
            
            # without the current section
            instructorSections = [x for x in population if x.instructor == instructor and x != section]

            section_fitness = 0

            # constraints
            # 1. instructor has no conflicts
            conflict = Helpers.calculateConflict(self, section, instructorSections)
            fitness += conflict
            section_fitness += conflict
            conflict_fitness += conflict

            # 2. instructor has full load
            fullLoad = Helpers.calculateFullLoad(self, section, instructorSections)
            fitness += fullLoad
            section_fitness += fullLoad
            fullLoad_fitness += fullLoad

            # 3. instructor has no more than 4 days
            fourDays = Helpers.calculateFourDays(self, section, instructorSections)
            fitness += fourDays
            section_fitness += fourDays
            fourDays_fitness += fourDays

            # 4. 

            







            ranked_population.append((section, section_fitness))
            
            counter += 1
            
        return ranked_population, fitness, conflict_fitness, fullLoad_fitness, fourDays_fitness

    def crossover(self, ranked_population, instructors_list):

        # sort the ranked population by the rank
        ranked_population.sort(key=lambda x: x[1], reverse=True)

        # get the best 50% of the population
        best_population = ranked_population[:int(len(ranked_population)/2)]

        # get the worst 50% of the population
        worst_population = ranked_population[int(len(ranked_population)/2):]

        # loop on worst population and swap instructors randmoly
        for section in worst_population:
            # select random instructor
            random_instructor = random.choice(instructors_list)
            section[0].instructor = random_instructor

        # remove the section rank from the list
        best_population = [x[0] for x in best_population]
        worst_population = [x[0] for x in worst_population]
        
        # add the best population to the worst population
        new_population = best_population + worst_population

        return new_population


class Application:

    def main():


        # create list of instructors
        instructors_list = []
        # add instructors to the list
        instructors_list.append(Instructor(1, 'محمد', 10))
        instructors_list.append(Instructor(2, 'عبدالله', 10))
        instructors_list.append(Instructor(3, 'علي', 10))
        instructors_list.append(Instructor(4, 'حسن', 10))
        instructors_list.append(Instructor(5, 'زيد', 10))
        instructors_list.append(Instructor(6, 'باسل', 10))
        instructors_list.append(Instructor(7, 'ياسر', 10))
        instructors_list.append(Instructor(8, 'محمود', 10))
        instructors_list.append(Instructor(10, 'وليد', 10))
        instructors_list.append(Instructor(11, 'معاذ', 10))
        instructors_list.append(Instructor(12, 'برقان', 10))
        instructors_list.append(Instructor(13, 'فيصل', 10))
        instructors_list.append(Instructor(14, 'مشاري', 10))
        instructors_list.append(Instructor(15, 'عمر', 10))
        instructors_list.append(Instructor(16, 'عبيد', 10))
        instructors_list.append(Instructor(17, 'حسنين', 10))
        instructors_list.append(Instructor(18, 'مؤيد', 10))
        instructors_list.append(Instructor(19, 'احمد', 10))
        instructors_list.append(Instructor(20, 'فارس', 10))
        instructors_list.append(Instructor(21, 'فراس', 10))

        instructors_list.append(Instructor(22, 'محمد', 10))
        instructors_list.append(Instructor(23, 'عبدالله', 10))
        instructors_list.append(Instructor(24, 'علي', 10))
        instructors_list.append(Instructor(25, 'حسن', 10))
        instructors_list.append(Instructor(26, 'زيد', 10))
        instructors_list.append(Instructor(27, 'باسل', 10))
        instructors_list.append(Instructor(28, 'ياسر', 10))
        instructors_list.append(Instructor(29, 'محمود', 10))
        instructors_list.append(Instructor(30, 'وليد', 10))
        instructors_list.append(Instructor(31, 'معاذ', 10))
        instructors_list.append(Instructor(32, 'برقان', 10))
        instructors_list.append(Instructor(33, 'فيصل', 10))
        instructors_list.append(Instructor(34, 'مشاري', 10))
        instructors_list.append(Instructor(35, 'عمر', 10))
        instructors_list.append(Instructor(36, 'عبيد', 10))
        instructors_list.append(Instructor(37, 'حسنين', 10))
        instructors_list.append(Instructor(38, 'مؤيد', 10))
        instructors_list.append(Instructor(39, 'احمد', 10))
        instructors_list.append(Instructor(40, 'فارس', 10))
        instructors_list.append(Instructor(41, 'فراس', 10))
        instructors_list.append(Instructor(42, 'محمد', 10))
        instructors_list.append(Instructor(43, 'عبدالله', 10))
        instructors_list.append(Instructor(44, 'علي', 10))
        instructors_list.append(Instructor(45, 'حسن', 10))
        instructors_list.append(Instructor(46, 'زيد', 10))
        instructors_list.append(Instructor(47, 'باسل', 10))
        instructors_list.append(Instructor(48, 'ياسر', 10))
        instructors_list.append(Instructor(49, 'محمود', 10))
        instructors_list.append(Instructor(50, 'وليد', 10))
        instructors_list.append(Instructor(51, 'معاذ', 10))
        instructors_list.append(Instructor(52, 'برقان', 10))
        instructors_list.append(Instructor(53, 'فيصل', 10))
        instructors_list.append(Instructor(54, 'مشاري', 10))
        instructors_list.append(Instructor(55, 'عمر', 10))
        instructors_list.append(Instructor(56, 'عبيد', 10))
        instructors_list.append(Instructor(57, 'حسنين', 10))
        instructors_list.append(Instructor(58, 'مؤيد', 10))
        instructors_list.append(Instructor(59, 'احمد', 10))
        instructors_list.append(Instructor(60, 'فارس', 10))
        instructors_list.append(Instructor(61, 'فراس', 10))
        instructors_list.append(Instructor(62, 'محمد', 10))
        instructors_list.append(Instructor(63, 'عبدالله', 10))
        instructors_list.append(Instructor(64, 'علي', 10))
        instructors_list.append(Instructor(65, 'حسن', 10))
        instructors_list.append(Instructor(66, 'زيد', 10))
        instructors_list.append(Instructor(67, 'باسل', 10))
        instructors_list.append(Instructor(68, 'ياسر', 10))
        instructors_list.append(Instructor(69, 'محمود', 10))
        instructors_list.append(Instructor(70, 'وليد', 10))
        instructors_list.append(Instructor(71, 'معاذ', 10))
        instructors_list.append(Instructor(72, 'برقان', 10))
        instructors_list.append(Instructor(73, 'فيصل', 10))
        instructors_list.append(Instructor(74, 'مشاري', 10))
        instructors_list.append(Instructor(75, 'عمر', 10))
        instructors_list.append(Instructor(76, 'عبيد', 10))
        instructors_list.append(Instructor(77, 'حسنين', 10))
        instructors_list.append(Instructor(78, 'مؤيد', 10))
        instructors_list.append(Instructor(79, 'احمد', 10))
        instructors_list.append(Instructor(80, 'فارس', 10))




        




        # create list of sections
        sections_list = importSections()

        # add sections to the list
        # sections_list.append(Section(1, 'CS', '101', 'A', True, 'Introduction to Computer Science', 8, 10, ' MTW'))
        # sections_list.append(Section(2, 'CS', '101', 'B', True, 'Introduction to Computer Science', 8, 10, 'MTW'))
        # sections_list.append(Section(3, 'CS', '101', 'C', True, 'Introduction to Computer Science', 8, 10, 'MTW'))
        # sections_list.append(Section(4, 'CS', '101', 'D', True, 'Introduction to Computer Science', 8, 10, 'MTW'))
        # sections_list.append(Section(5, 'CS', '101', 'E', True, 'Introduction to Computer Science', 8, 10, 'MTW'))
        # sections_list.append(Section(6, 'CS', '101', 'F', True, 'Introduction to Computer Science', 8, 10, 'MTW'))
        # sections_list.append(Section(7, 'CS', '101', 'G', True, 'Introduction to Computer Science', 8, 10, 'MTW'))



        best_fitness = 0
        best_chromosome = None

        G = GeneticAlgorithm()

        # generate population 
        population = G.generatePopulation(sections_list, instructors_list)

        counter = 0
        while True:
            # count fitness
            ranked_population, fitness, conflict_fitness, fulload_fitness, fourDays_fitness = G.calculateFitness(population)

            # check if the fitness is better than the best fitness
            if fitness > best_fitness:
                best_fitness = fitness
                best_chromosome = population
                best_conflict_fitness = conflict_fitness
                best_fullLoad_fitness = fulload_fitness 
                best_fourDays_fitness = fourDays_fitness
                
            # check if the fitness is 100%
            if fitness == (3 * len(sections_list)):
                break

            # crossover
            population = G.crossover(ranked_population, instructors_list)

            if population == None:
                break

            counter += 1

            if counter == 1000:
                break

        best_fitness = best_fitness / ((Fitness.CONFLICT.value + Fitness.FULL_LOAD.value + Fitness.FOUR_DAYS.value) * len(sections_list))
        best_conflict_fitness = best_conflict_fitness / (Fitness.CONFLICT.value * len(sections_list))
        best_fullLoad_fitness = best_fullLoad_fitness / (Fitness.FULL_LOAD.value * len( sections_list))
        best_fourDays_fitness = best_fourDays_fitness / (Fitness.FOUR_DAYS.value * len(sections_list))

        return best_chromosome, best_fitness, best_conflict_fitness, best_fullLoad_fitness, best_fourDays_fitness
    




s,f,c,fl,fd = Application.main()

# print table of the best chromosome


for i in s:

    print('course' , i.course_id, 'course_symbol' , i.course_symbol , 'instructor' , i.instructor.name)
    print('-----------------')


print('-----------------')
print('best fitness' , f, '%')
print('conflict fitness' , c, '%')
print('full load fitness' , fl, '%')
print('four days fitness' , fd, '%')
print('-----------------')