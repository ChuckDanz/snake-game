import pygame
import neat 
import random
import os
import time
import sys
import math



SW, SH = 800, 800 #Screen Width and Height

BLOCK_SIZE = 50



generation = 0

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

pygame.init()

#FONT = pygame.font.SysFont("Arial", 50)

directions = [0, 1, 2, 3]


        

class Snake:
    

    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.consecutive_turns = 0
        self.xdir = 1
        self.ydir = 0
        self.direction = -1
        self.past_direction = -1
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
        self.last_move_time = time.time()
        self.still_time_threshold = 3
        self.apples_eaten = 0
        self.turns = []
    
    def spawn_food(self):
        while True:
            # Generate random coordinates for the food
            self.ax = random.randint(0, (SW - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            self.ay = random.randint(0, (SH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE

            # Check if the food overlaps with any part of the snake's body
            food_collides_with_snake = any((self.ax, self.ay) == (segment.x, segment.y) for segment in self.body)
            
            # If food doesn't overlap with the snake's body, break the loop
            if not food_collides_with_snake:
                break
        
        #self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        #pygame.draw.rect(screen, "red", self.rect)

    

    
    
    def update_timer(self):
        if not self.dead:
            self.last_move_time = time.time()
    
    def reset_timer(self):
        if not self.dead:
            self.last_move_time = time.time()
       

    def time_since_last_food(self):
        if not self.dead:
            return time.time() - self.last_move_time
        return 0
        #return time.time() - self.last_move_time > self.still_time_threshold



    def update(self):
        global food

        
        
        #if self.time_since_last_food() > 30:
            #self.dead = True
            

        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y: # Checks for Collision
                #print("Snake collided with itself and died")
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH): # This Too
                #print("Snake collided with the wall")
                self.dead = True

        #if self.is_still_for_threshold():
            #self.dead = True
        

       # if self.dead:
            #self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            #self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            #self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            #self.xdir = 1
            #self.ydir = 0 
            #self.dead = False
            #food = Food()


        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

        
    

    
    def check_food_row(self):
        #return (self.ax - self.head.x) / SW
        return (self.head.y // BLOCK_SIZE) - (self.ay // BLOCK_SIZE)

    def check_food_column(self):
        #return (self.ay - self.head.y) / SH
        return (self.head.x // BLOCK_SIZE) - (self.ax // BLOCK_SIZE)

    def distance_food(self):
        return ((self.head.x - self.ax) ** 2 + (self.head.y - self.ay) ** 2) ** 0.5 / (SW + SH)
    
    def distance_to_wall_horizontal(self):
        min_horizontal_distance = min(self.head.x, 799 - self.head.x)
        max_horizontal_distance = max(self.head.x, 799 - self.head.x)
        if max_horizontal_distance == 0:
            return 0  # Avoid division by zero
        return (self.head.x - min_horizontal_distance) / max_horizontal_distance

    def distance_to_wall_vertical(self):
        min_vertical_distance = min(self.head.y, 799 - self.head.y)
        max_vertical_distance = max(self.head.y, 799 - self.head.y)
        if max_vertical_distance == 0:
            return 0  # Avoid division by zero
        return (self.head.y - min_vertical_distance) / max_vertical_distance
    
    def distance_to_tail(self):#fix this, dont use distance
        if len(self.body) > 0:
            last_segment = self.body[-1]
            return (abs(self.head.x - last_segment.x), abs(self.head.y - last_segment.y)) 
        else:
            # If the snake has no body segments, return a default value (e.g., 1.0)
            return 1.0
    def get_snake_length(self):
        return len(self.body)
    
    


    
    def get_data(self):
        self.left_adjacent = 0
        self.right_adjacent = 0
        self.up_adjacent = 0
        self.down_adjacent = 0
        if any((self.x - BLOCK_SIZE, self.y) == (segment.x, segment.y) for segment in self.body):
            self.left_adjacent += 1
        if any((self.x + BLOCK_SIZE, self.y) == (segment.x, segment.y) for segment in self.body):
            self.right_adjacent += 1
        if any((self.x, self.y - BLOCK_SIZE) == (segment.x, segment.y) for segment in self.body):
            self.up_adjacent += 1
        if any((self.x, self.y + BLOCK_SIZE) == (segment.x, segment.y) for segment in self.body):
            self.down_adjacent += 1
        if len(self.body) > 0:
            last_segment = self.body[-1]
            dist_from_tail =  (abs(self.head.x - last_segment.x), abs(self.head.y - last_segment.y)) 
        else:
            # If the snake has no body segments, return a default value (e.g., 1.0)
            dist_from_tail = (SW, SH)
        
        

        data = [
            #self.check_food_column(),
            #self.check_food_row(),
            self.head.x - self.ax,
            self.head.y - self.ay, #now find inputs to get snake to see itself
            #dist_from_tail[0],
            #dist_from_tail[1],
            #abs(self.x - SW),
            #abs(self.y - SH)
            self.distance_to_wall_horizontal(), #need to fix
            self.distance_to_wall_vertical(),
            #self.direction,
            #self.head.x,
           # self.head.y
            #self.distance_to_tail()
            #self.get_snake_length(),
            #self.down_adjacent,
            #self.up_adjacent,
            #self.right_adjacent,
            #self.left_adjacent,
            #self.past_direction,
            #self.consecutive_turns
        ]

        return data
    
    def is_dead(self):
        return self.dead 
    
    #def add_fitness_food(self):
        #self.add_fit_food += 1

    
    def get_reward(self):
       reward_apple_eaten = self.apples_eaten #* 2
       self.apples_eaten = 0

       #reward_time_survived = 0.1

       #total_reward = self.apples_eaten * reward_apple_eaten# + self.time_since_last_food() * reward_time_survived

       return reward_apple_eaten

        #put a counter of moves left so the snake dies if it does not get an apple in time

        

    def get_food_eaten(self):
        if (self.head.x, self.head.y) == (self.ax, self.ay):
            self.apples_eaten += 1
            self.spawn_food()
            self.reset_timer()
            new_segment = pygame.Rect(self.body[-1].x, self.body[-1].y, BLOCK_SIZE, BLOCK_SIZE)
            self.body.append(new_segment)
    
    
    
    #integrate the food object into the snake object





def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)

#score = FONT.render("1", True, "white")
#score_rect = score.get_rect(topright = (SW-20, SH/20))
            

#drawGrid()

snake = Snake()

#food = Food()

#print(food.x, food.y)



def run_snake(genomes, config):
    #global food
    #INIT NEAT
    nets = []
    snakes = []

    

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        #Initialize the Snakes
        snakes.append(Snake())

    #Initalize the Game
    #pygame.init()
    #FONT = pygame.font.SysFont("Arial", 50)
    
    #drawGrid()
    for snake in snakes:
        snake.spawn_food()

    global generation
    generation += 1

    #food = Food()

    #foods = [Food() for _ in range(len(snakes))]
    start_time = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        
        #snake.update()

        screen.fill('black')
        drawGrid()
        
        

        
        

            #input my data and get result from network
        for index, snake in enumerate(snakes):
            output = nets[index].activate(snake.get_data())
            #print(output)
            i = output.index(max(output))
            #print(snake.is_still_for_threshold())
            #print(i)
            #print(snake.is_dead())
            #print(f"Snake {index} - Output: {output}, Decision: {i}, Data: {snake.get_data()}")
            #check logic here to make snake go to food
            #snake.update_timer()
            #snake.always_move_forward()
            if i == 0 and snake.past_direction != 2:
                snake.direction = 0
            elif i == 1 and snake.past_direction != 3:
                snake.direction = 1
            elif i == 2 and snake.past_direction != 0:
                snake.direction = 2
            elif i == 3 and snake.past_direction != 1:
                snake.direction = 3

            #snake.update()
            snake.get_food_eaten()
            
            
        # find a new way to make the snake continously move forward, this will resolve a lot of issues so it cannot go back and forward
        # number of input is not relative to how many outputs, make outputs 4
                
        #update car and fitness
        remain_snakes = 0
        for i, snake in enumerate(snakes):
            if snake.is_dead() == False:
                remain_snakes += 1
                snake.update()
                #snake.get_food_eaten()
                genomes[i][1].fitness += snake.get_reward()

                #print(f"Generation: {generation}, Snake {i + 1} - Fitness: {genomes[i][1].fitness}, Apples Eaten: {snake.apples_eaten}")


                if i == 0:
                    pygame.draw.rect(screen, "red", (snake.ax, snake.ay, BLOCK_SIZE, BLOCK_SIZE))
            
    

       
        
        #print(f"Generation Fitness: {[g.fitness for _, g in genomes]}")
                    
        
        
        
        pygame.draw.rect(screen, "blue", snakes[0].head)

        for square in snakes[0].body:
            pygame.draw.rect(screen, "blue", square)

        for snake in snakes:
            if snake.direction == 0 and snake.past_direction != 2: 
                snake.ydir = -1
                snake.xdir = 0
            if snake.direction == 2 and snake.past_direction != 0: 
                snake.ydir = 1
                snake.xdir = 0
            if snake.direction == 3 and snake.past_direction != 1:
                snake.xdir = -1
                snake.ydir = 0
            if snake.direction == 1 and snake.past_direction != 3: 
                snake.xdir = 1
                snake.ydir = 0

            if snake.direction == directions[snake.past_direction - 1]: 
                snake.turns.append("Left")
            elif snake.past_direction == 3 and snake.direction == 0: 
                snake.turns.append("Right")
            elif snake.direction == snake.past_direction + 1: 
                snake.turns.append("Right")
            if "Right" and  "Left" in snake.turns: snake.turns.clear()

            snake.consecutive_turns = len(snake.turns)
            snake.past_direction = snake.direction

            #print("Snake X:", snakes[0].head.x, "Snake Y:", snakes[0].head.y)
            #print("Apple X:", snakes[0].ax, "Apple Y:", snakes[0].ay)
            
                #snake.xdir = -1 if food.x < snake.head.x else 1
                #snake.ydir = 0
        
        #snake.update()

        
        for snake in snakes:
            if snake.time_since_last_food() > 15:
                snake.dead = True

        if remain_snakes == 0:#fix this i do not think this applies to each of the snakes
            break
        
        #now print the best fitness snake to the screen
        
        #add more inputs to make snake not run into itself

        

        for snake in snakes:
            snake.apple_eaten = 0


        #print(f"Remaining Snakes: {remain_snakes}")
            #print(snake.time_since_last_food())

        #print(snakes[0].time_since_last_food())

        #food.update()

        
        pygame.display.update()
        clock.tick(10)


        
        
        #if remain_snakes >= len(snakes):
        #    break

       

            

        

        #score = FONT.render(f"{(len(snake.body) - 2) + 1}", True, "white")

        # screen.blit(score, score_rect)

            

        
if __name__ == "__main__":
    #set config file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    #Core algortihm class
    p = neat.Population(config)

    #Reporter for stats
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    #Run Neat
    p.run(run_snake, 1000)







