import numpy as np
import pygame as pg
import argparse

class Environment():
    def __init__(self, waittime, currentMap):
        pg.init()
        pg.mixer.init()

        self.width = 900
        self.height = 600
        self.nRows = 18
        self.nColumns = 18
        self.initSnakeLen = 2

        self.defReward = -0.01
        self.negReward = -5.0
        self.posReward = 2.0
        self.bonusReward = 4.0
        self.toxicReward = -2.5

        self.score = 0
        self.waittime = waittime
        self.currentMap = currentMap

        self.bonusDuration = 500
        self.bonusTimer = 0
        self.toxicDuration = 750
        self.toxicTimer = 0

        self.obstacles = []

        self.stepsSinceLastFood = 0
        self.maxStepsBase = 100
        self.maxStepsPerSegment = 5

        #Set colors
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.DARKGREEN = (10, 50, 10)
        self.DARKRED = (150, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 255, 255)
        self.BROWN = (150, 75, 0)

        #Set fonts
        self.font = pg.font.SysFont("gabriola", 48)

        #Set text
        self.update_score()

        self.gameover_text = self.font.render("Game over !", True, self.RED, self.DARKRED)
        self.gameover_rect = self.gameover_text.get_rect()
        self.gameover_rect.center = (self.width//2, self.height//2)

        #Set pick up sound
        self.pick_up_sound = pg.mixer.Sound("assets/sounds/pick_up_sound.wav")

        #Set bonus pick up sound
        self.bonus_pick_up_sound = pg.mixer.Sound("assets/sounds/ruby_pickup.wav")

        #Set toxic pick up sound
        self.toxic_pick_up_sound = pg.mixer.Sound("assets/sounds/miss_sound.wav")

        if self.initSnakeLen > self.nRows / 2:
            self.initSnakeLen = int(self.nRows /2)
        
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("~~Snake~~")

        #Background
        self.background_image = pg.image.load("assets/background.png").convert()

        #Sprites

        #Apple
        self.apple_image = pg.image.load("assets/collectables/apple/apple.png").convert_alpha()
        self.apple_image = pg.transform.scale(self.apple_image, (int(self.width / self.nColumns), int(self.height / self.nRows)))

        #Bonus
        self.bonus_images = []

        for k in range(7):
            image = pg.image.load(f"assets/collectables/bonus/ruby_{k}.png").convert_alpha()
            image = pg.transform.scale(image, (int(self.width / self.nColumns), int(self.height / self.nRows)))
            self.bonus_images.append(image)
        
        self.bonus_frame = 0
        self.bonus_animation_speed = 3
        self.bonus_animation_counter = 0

        #Toxic
        self.toxic_images = []

        for k in range(7):
            image = pg.image.load(f"assets/collectables/toxic/toxic_{k}.png").convert_alpha()
            image = pg.transform.scale(image, (int(self.width / self.nColumns), int(self.height / self.nRows)))
            self.toxic_images.append(image)
        
        self.toxic_frame = 0
        self.toxic_animation_speed = 8
        self.toxic_animation_counter = 0 

        #Obstacles
        self.obstacle_image = pg.image.load("assets/obstacles/obstacle_3.png").convert_alpha()
        self.obstacle_image = pg.transform.scale(self.obstacle_image, (int(self.width / self.nColumns), int(self.height / self.nRows)))

        #Snake
        self.load_snake_images()

        self.reset()
        self.collected = False


    def update_score(self):
        self.score_text = self.font.render("Score: " + str(self.score), True, self.GREEN, self.DARKGREEN)
        self.score_rect = self.score_text.get_rect()
        self.score_rect.topleft = (0,0)
    
    def load_map(self):
        if self.currentMap == 1:
            self.obstacles = list()
            for y in range(0,18):
                self.obstacles.append((y,0))
                self.obstacles.append((y,17))
            for x in range(0,18):
                self.obstacles.append((0,x))
                self.obstacles.append((17,x))

        elif self.currentMap == 2:
            self.obstacles = list()
            for y in range(2,6):
                for x in range(2,6):
                    self.obstacles.append((y,x))
            
            for y in range(12,16):
                for x in range(12,16):
                    self.obstacles.append((y,x))

        elif self.currentMap == 3:
            self.obstacles = list()
            for y in range(1, 5):
                for x in range(1, 5):
                    self.obstacles.append((y,x))
            
            for y in range(1, 5):
                for x in range(13, 17):
                    self.obstacles.append((y,x))
            
            for y in range(13, 17):
                for x in range(1, 5):
                    self.obstacles.append((y,x))
            
            for y in range(13, 17):
                for x in range(13, 17):
                    self.obstacles.append((y,x))
        
        elif self.currentMap == 4:
            self.obstacles = list()
            for y in range(3, 15):
                if y < 6 or y > 11:
                    self.obstacles.append((y,3))
                    self.obstacles.append((y,4))
                    self.obstacles.append((y,13))
                    self.obstacles.append((y,14))
            
            for x in range(5, 13):
                self.obstacles.append((3,x))
                self.obstacles.append((4,x))
                self.obstacles.append((13,x))
                self.obstacles.append((14,x))
            
        return self.obstacles
    
    def set_map(self, new_map):
        self.currentMap = new_map

    def load_snake_images(self):
        size = (int(self.width / self.nColumns), int(self.height / self.nRows))

        self.snake_images = {
            "head_up": pg.transform.scale(pg.image.load("assets/snake/head/head_up.png").convert_alpha(), size),
            "head_down": pg.transform.scale(pg.image.load("assets/snake/head/head_down.png").convert_alpha(), size),
            "head_left": pg.transform.scale(pg.image.load("assets/snake/head/head_left.png").convert_alpha(), size),
            "head_right": pg.transform.scale(pg.image.load("assets/snake/head/head_right.png").convert_alpha(), size),

            "tail_up": pg.transform.scale(pg.image.load("assets/snake/tail/tail_up.png").convert_alpha(), size),
            "tail_down": pg.transform.scale(pg.image.load("assets/snake/tail/tail_down.png").convert_alpha(), size),
            "tail_left": pg.transform.scale(pg.image.load("assets/snake/tail/tail_left.png").convert_alpha(), size),
            "tail_right": pg.transform.scale(pg.image.load("assets/snake/tail/tail_right.png").convert_alpha(), size),

            "body_horizontal": pg.transform.scale(pg.image.load("assets/snake/body/body_horizontal.png").convert_alpha(), size),
            "body_vertical": pg.transform.scale(pg.image.load("assets/snake/body/body_vertical.png").convert_alpha(), size),

            "body_topleft": pg.transform.scale(pg.image.load("assets/snake/body/body_topleft.png").convert_alpha(), size),
            "body_topright": pg.transform.scale(pg.image.load("assets/snake/body/body_topright.png").convert_alpha(), size),
            "body_bottomleft": pg.transform.scale(pg.image.load("assets/snake/body/body_bottomleft.png").convert_alpha(), size),
            "body_bottomright": pg.transform.scale(pg.image.load("assets/snake/body/body_bottomright.png").convert_alpha(), size),
        }


    def place_fruit(self):
        ocupied = set(self.SnakePos) | set(self.obstacles)
        if self.BonusPos is not None:
            ocupied.add(self.BonusPos)
        if self.ToxicPos is not None:
            ocupied.add(self.ToxicPos)
        free_position = []
        
        for y in range(self.nRows):
            for x in range(self.nColumns):
                if (y, x) not in ocupied:
                    free_position.append((y,x))
        if len(free_position) == 0:
            return None
        
        idx = np.random.randint(0, len(free_position))
        return free_position[idx]
    
    def place_bonus(self):
        if np.random.rand() < 0.3:
            self.BonusPos = self.place_fruit()
            self.bonusTimer = self.bonusDuration
    
    def place_toxic(self):
        if np.random.rand() < 0.35:
            self.ToxicPos = self.place_fruit()
            self.toxicTimer = self.toxicDuration


    def move_snake(self, nextPos, grow):
        self.SnakePos.insert(0, nextPos)
        if not grow:
            self.SnakePos.pop(len(self.SnakePos) -1)
        self.screenMap = np.zeros((self.nRows, self.nColumns))

        for i in range(len(self.SnakePos)):
            self.screenMap[self.SnakePos[i][0], self.SnakePos[i][1]] = 0.5
        
        for y,x in self.obstacles:
            self.screenMap[y, x] = 4
        
        if self.ApplePos is not None:
            self.screenMap[self.ApplePos[0], self.ApplePos[1]] = 1
        if self.BonusPos is not None:
            self.screenMap[self.BonusPos[0], self.BonusPos[1]] = 2
        if self.ToxicPos is not None:
            self.screenMap[self.ToxicPos[0],self.ToxicPos[1]] = 3

    
    def draw_snake(self):
        for index, pos in enumerate(self.SnakePos):
            y, x = pos
            draw_x = x * int(self.width / self.nColumns)
            draw_y = y * int(self.height / self.nRows)

            if index == 0:
                head_y, head_x = self.SnakePos[0]
                neck_y, neck_x = self.SnakePos[1]

                if head_y < neck_y:
                    image = self.snake_images["head_up"]
                elif head_y > neck_y:
                    image = self.snake_images["head_down"]
                elif head_x < neck_x:
                    image = self.snake_images["head_left"]
                elif head_x > neck_x:
                    image = self.snake_images["head_right"]
            
            elif index == len(self.SnakePos) - 1:
                tail_y, tail_x = self.SnakePos[-1]
                before_tail_y, before_tail_x = self.SnakePos[-2]

                if before_tail_y < tail_y:
                    image = self.snake_images["tail_down"]
                elif before_tail_y > tail_y:
                    image = self.snake_images["tail_up"]
                elif before_tail_x < tail_x:
                    image = self.snake_images["tail_right"]
                elif before_tail_x > tail_x:
                    image = self.snake_images["tail_left"]
            
            else:
                prev_y, prev_x = self.SnakePos[index -1]
                curr_y, curr_x = self.SnakePos[index]
                next_y, next_x = self.SnakePos[index + 1]

                if prev_y == next_y:
                    image = self.snake_images["body_horizontal"]
                
                elif prev_x == next_x:
                    image = self.snake_images["body_vertical"]
                
                else:
                    up = prev_y < curr_y or next_y < curr_y
                    down = prev_y > curr_y or next_y > curr_y
                    left = prev_x < curr_x or next_x < curr_x
                    right = prev_x > curr_x or next_x > curr_x

                    if up and left:
                        image = self.snake_images["body_topleft"]
                    elif up and right:
                        image = self.snake_images["body_topright"]
                    elif down and left:
                        image = self.snake_images["body_bottomleft"]
                    else:
                        image = self.snake_images["body_bottomright"]
        
            self.screen.blit(image, (draw_x, draw_y))



    def reset(self):
        self.screenMap = np.zeros((self.nRows, self.nColumns))
        self.obstacles = self.load_map()
        self.score = 0
        self.update_score()

        self.BonusPos = None
        self.bonusTimer = 0
        self.ToxicPos = None
        self.toxicTimer = 0

        self.SnakePos = list()
        self.stepsSinceLastFood = 0
        self.lastMove = 0

        center_y = self.nRows // 2
        center_x = self.nColumns // 2

        for y, x in self.obstacles:
            self.screenMap[y, x] = 4

        for i in range(self.initSnakeLen):
            pos = (center_y + i, center_x)
            if pos in self.obstacles:
                raise ValueError("Obstacle overlaps snake spawn position.")
            else:
                self.SnakePos.append((center_y + i, center_x))
                self.screenMap[center_y + i, center_x] = 0.5
        
        self.ApplePos = self.place_fruit()
        if self.ApplePos is not None:
            y, x = self.ApplePos
            self.screenMap[y, x] = 1
        
        self.draw_screen()
        return self.get_vector_state()


    def draw_screen(self):
        tile_size = 32
        for x in range(0, self.width, tile_size):
            for y in range(0, self.height, tile_size):
                self.screen.blit(self.background_image, (x, y))
        
        cellWidth = self.width / self.nColumns
        cellHeight = self.height / self.nRows

        for j in range(self.nRows):
            for i in range(self.nColumns):
                if self.screenMap[j, i] == 1:
                    self.screen.blit(self.apple_image, (i*cellWidth, j*cellHeight))
                elif self.screenMap[j, i] == 2:
                    self.screen.blit(self.bonus_images[self.bonus_frame], (i*cellWidth, j*cellHeight))
                elif self.screenMap[j, i] == 3:
                    self.screen.blit(self.toxic_images[self.toxic_frame], (i*cellWidth, j*cellHeight))
                elif self.screenMap[j, i] == 4:
                    self.screen.blit(self.obstacle_image, (i*cellWidth, j*cellHeight))
        self.screen.blit(self.score_text,self.score_rect)

        self.bonus_animation_counter += 1
        self.toxic_animation_counter += 1

        if self.bonus_animation_counter >= self.bonus_animation_speed:
            self.bonus_animation_counter = 0
            self.bonus_frame = (self.bonus_frame + 1) % len(self.bonus_images)

        if self.toxic_animation_counter >= self.bonus_animation_speed:
            self.toxic_animation_counter = 0
            self.toxic_frame = (self.toxic_frame + 1) % len(self.toxic_images)
        
        self.draw_snake()
        self.update_score()
        pg.display.flip()
    

    def get_valid_action(self, action):
        opposite_moves = {
            0:1, #up-down
            1:0, #down-up
            2:3, #right-left
            3:2, #left-right
        }
        if action == opposite_moves[self.lastMove]:
            return self.lastMove
        return action
    

    def is_outside(self,pos):
        y, x = pos
        return not (0 <= y < self.nRows and 0 <= x < self.nColumns)
    

    def get_next_position(self, action):
        directions = {
            0:(-1, 0), #up
            1:(1, 0), #down
            2:(0, 1), #right
            3:(0, -1) #left
        }
        head_y, head_x = self.SnakePos[0]
        dy, dx = directions[action]
        return (head_y + dy, head_x + dx)

    def is_collision(self, pos):

        if self.is_outside(pos):
            return True
        
        if pos in self.SnakePos:
            return True
        
        if pos in self.obstacles:
            return True
        
        return False

    def get_vector_state(self):
        head_y, head_x = self.SnakePos[0]

        dir_up = int(self.lastMove == 0)
        dir_down = int(self.lastMove == 1)
        dir_right = int(self.lastMove == 2)
        dir_left = int(self.lastMove == 3)

        up = (head_y - 1, head_x)
        down = (head_y + 1, head_x)
        right = (head_y, head_x + 1)
        left = (head_y, head_x - 1)
        
        danger_up = int(self.is_collision(up))
        danger_down = int(self.is_collision(down))
        danger_right = int(self.is_collision(right))
        danger_left = int(self.is_collision(left))

        apple_y, apple_x = self.ApplePos
        apple_up = int(apple_y < head_y)
        apple_down = int(apple_y > head_y)
        apple_right = int(apple_x > head_x)
        apple_left = int(apple_x < head_x)

        if self.BonusPos is not None:
            bonus_y, bonus_x = self.BonusPos
            bonus_up = int(bonus_y < head_y)
            bonus_down = int(bonus_y > head_y)
            bonus_right = int(bonus_x > head_x)
            bonus_left = int(bonus_x < head_x)
        else:
            bonus_up = bonus_down = bonus_right = bonus_left = 0
        if self.ToxicPos is not None:
            toxic_y, toxic_x = self.ToxicPos
            toxic_up = int(toxic_y < head_y)
            toxic_down = int(toxic_y > head_y)
            toxic_right = int(toxic_x > head_x)
            toxic_left = int(toxic_x < head_x)
        else:
            toxic_up = toxic_down = toxic_right = toxic_left = 0
        
        bonus_exists = int(self.BonusPos is not None)
        toxic_exists = int(self.ToxicPos is not None)

        state = np.array([
            danger_up, danger_down, danger_right, danger_left,
            dir_up, dir_down, dir_right, dir_left,
            apple_up, apple_down, apple_right, apple_left,
            bonus_up, bonus_down, bonus_right, bonus_left,
            toxic_up, toxic_down, toxic_right, toxic_left,
            bonus_exists, toxic_exists
        ], dtype=np.float32)

        return state


    def step(self, action):
        self.collected = False
        gameOver = False
        reward = self.defReward

        self.stepsSinceLastFood +=1
        dynamicLimit = self.maxStepsBase + self.maxStepsPerSegment * len(self.SnakePos)

        if self.stepsSinceLastFood >= dynamicLimit:
            gameOver = True
            reward = self.negReward
            return self.get_vector_state(), reward, gameOver

        if self.bonusTimer > 0:
            self.bonusTimer -= 1
            if self.bonusTimer == 0:
                self.BonusPos = None
        
        if self.toxicTimer > 0:
            self.toxicTimer -= 1
            if self.toxicTimer == 0:
                self.ToxicPos = None

        action = self.get_valid_action(action)
        next_pos = self.get_next_position(action)
        next_y, next_x = next_pos

        head_y, head_x = self.SnakePos[0]
        apple_y, apple_x = self.ApplePos

        if self.BonusPos is not None:
            bonus_y, bonus_x = self.BonusPos
            old_distance_bonus = abs(head_y - bonus_y) + abs(head_x - bonus_x)
            new_distance_bonus = abs(next_y - bonus_y) + abs(next_x - bonus_x)

        if self.ToxicPos is not None:
            toxic_y, toxic_x = self.ToxicPos
            old_distance_toxic = abs(head_y - toxic_y) + abs(head_x - toxic_x)
            new_distance_toxic = abs(next_y - toxic_y) + abs(next_x - toxic_x)

        old_distance_apple = abs(head_y - apple_y) + abs(head_x - apple_x)
        new_distance_apple = abs(next_y - apple_y) + abs(next_x - apple_x)

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    raise SystemExit
            elif event.type == pg.QUIT:
                pg.quit()
                raise SystemExit

        if self.is_outside(next_pos):
            gameOver = True
            reward = self.negReward
        else:
            cell_value = self.screenMap[next_y, next_x]
            if cell_value == 0.5:
                gameOver = True
                reward = self.negReward

            elif cell_value == 1:
                gameOver = False
                self.stepsSinceLastFood = 0
                reward = self.posReward
                self.collected = True
                self.pick_up_sound.play()
                self.move_snake(next_pos, True)
                self.ApplePos = self.place_fruit()
                self.score +=1
                self.update_score()
                if self.BonusPos is None:
                    self.place_bonus()
                if self.ToxicPos is None:
                    self.place_toxic()
            elif cell_value == 2:
                gameOver = False
                self.stepsSinceLastFood = 0
                reward = self.bonusReward
                self.collected = True
                self.bonus_pick_up_sound.play()
                self.BonusPos = None
                self.bonusTimer = 0
                self.move_snake(next_pos, True)
                self.score +=2
                self.update_score()
            elif cell_value == 3:
                gameOver = False
                reward = self.toxicReward
                self.collected = False
                self.toxic_pick_up_sound.play()
                self.ToxicPos = None
                self.toxicTimer = 0
                self.move_snake(next_pos, False)
                self.score -=1
                self.update_score()
            elif cell_value == 4:
                gameOver = True
                reward = self.negReward
            else:
                self.move_snake(next_pos, False)
                if new_distance_apple < old_distance_apple:
                    reward += 0.03
                elif new_distance_apple > old_distance_apple:
                    reward -= 0.03
                
                if self.BonusPos is not None:
                    if new_distance_bonus < old_distance_bonus:
                        reward += 0.015
                    elif new_distance_bonus > old_distance_bonus:
                        reward -= 0.015
                
                if self.ToxicPos is not None:
                    if new_distance_toxic < old_distance_toxic:
                        reward -= 0.015
                    elif new_distance_toxic > old_distance_toxic:
                        reward += 0.015
                
        self.lastMove = action
        self.draw_screen()
        pg.time.wait(self.waittime)

        return self.get_vector_state(), reward, gameOver
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=int, default=1, help="Map id")
    args = parser.parse_args()
    env = Environment(0, args.map)
    clock = pg.time.Clock()
    gameOver = False
    start = False
    action = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    raise SystemExit
                
                if event.key == pg.K_SPACE and not start:
                    start = True
                elif event.key == pg.K_SPACE and start:
                    start = False
                if event.key == pg.K_UP:
                    action = 0
                elif event.key == pg.K_DOWN:
                    action = 1
                elif event.key == pg.K_RIGHT:
                    action = 2
                elif event.key == pg.K_LEFT:
                    action = 3
            elif event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            
        if start:
            _, _, gameOver = env.step(action)
        
        if gameOver:
            start = False
            gameOver = False
            env.reset()
            action = 0
        
        clock.tick(8)