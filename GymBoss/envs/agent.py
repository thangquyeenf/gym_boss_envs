import random
from enum import Enum
import pygame # type: ignore
import sys
from os import path

class AgentAction(Enum):
    LEFT = 0
    RIGHT = 1
    FORWARD = 2


class GridTile(Enum):
    _FLOOR = 0
    AGENT = 1
    TARGET = 2

    def __str__(self):
        return self.name[:1]
    
class BossAgent:
    DIRECTIONS = ["N", "E", "S", "W"]
    E_BLOCK_POSITIONS = [(0, 1), (1, 2), (2, 1), (2, 2),  (3, 2)]
    SE_BLOCK_POSITIONS = [(1, 1)]
    NE_BLOCK_POSITIONS = [(2, 1)]
    WE_BLOCK_POSITIONS = [(1, 2), (2, 2)]
    W_BLOCK_POSITIONS = [(0, 2), (1, 3), (2, 3), (3, 3)]

    def __init__(self, grid_rows=4, grid_cols=4, fps=1):
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.reset()

        self.fps = fps
        self.last_action = ''
        self._init_pygame()
    
    def _init_pygame(self):
        pygame.init()
        pygame.display.init()

        self.clock = pygame.time.Clock()
        self.action_font = pygame.font.SysFont("Calibre", 30)
        self.action_info_height = self.action_font.get_height()

        self.cell_height = 64
        self.cell_width = 64
        self.cell_size = (self.cell_height, self.cell_width)

        self.window_size = (self.cell_width*self.grid_cols, self.cell_height*self.grid_rows + self.action_info_height)
        self.window_surface = pygame.display.set_mode(self.window_size)

        file_name = path.join(path.dirname(__file__), "sprites/floor.png")
        img = pygame.image.load(file_name)
        self.floor_img = pygame.transform.scale(img, self.cell_size)

        file_name = path.join(path.dirname(__file__), "sprites/E_Block.png")
        img = pygame.image.load(file_name)
        self.floor_EBlock_img = pygame.transform.scale(img, self.cell_size)

        file_name = path.join(path.dirname(__file__), "sprites/S_Block.png")
        img = pygame.image.load(file_name)
        self.floor_SBlock_img = pygame.transform.scale(img, self.cell_size)

        file_name = path.join(path.dirname(__file__), "sprites/SE_Block.png")
        img = pygame.image.load(file_name)
        self.floor_SEBlock_img = pygame.transform.scale(img, self.cell_size)

        file_name = path.join(path.dirname(__file__), "sprites/Target.png")
        img = pygame.image.load(file_name)
        self.goal_img = pygame.transform.scale(img, self.cell_size)

        file_name = path.join(path.dirname(__file__), "sprites/N.png")
        img = pygame.image.load(file_name)
        self.Agent_N_direct_img = pygame.transform.scale(img, self.cell_size)

        file_name = path.join(path.dirname(__file__), "sprites/S.png")
        img = pygame.image.load(file_name)
        self.Agent_S_direct_img = pygame.transform.scale(img, self.cell_size)

        file_name = path.join(path.dirname(__file__), "sprites/W.png")
        img = pygame.image.load(file_name)
        self.Agent_W_direct_img = pygame.transform.scale(img, self.cell_size)

        file_name = path.join(path.dirname(__file__), "sprites/E.png")
        img = pygame.image.load(file_name)
        self.Agent_E_direct_img = pygame.transform.scale(img, self.cell_size)

    def reset(self, seed=None):
        self.agent_pos = [0, 0]
        self.direction  = random.randint(0, 3)

        random.seed(seed)
        self.target_pos = [3, 3]

    def perform_action(self, action: AgentAction) -> bool:
        self.last_action = action
        prev_direction = self.direction

        if action == AgentAction.LEFT:
            self.direction = (self.direction - 1) % 4
        elif action == AgentAction.RIGHT:
            self.direction = (self.direction + 1) % 4
        elif action == AgentAction.FORWARD:
            new_pos = self.agent_pos.copy()
            if self.DIRECTIONS[self.direction] == "N" and self.agent_pos[0] > 0:
                new_pos[0] -= 1
            elif self.DIRECTIONS[self.direction] == "E" and self.agent_pos[1] < self.grid_cols - 1:
                new_pos[1] += 1
            elif self.DIRECTIONS[self.direction] == "S" and self.agent_pos[0] < self.grid_rows - 1:
                new_pos[0] += 1
            elif self.DIRECTIONS[self.direction] == "W" and self.agent_pos[1] > 0:
                new_pos[1] -= 1


            # Check for blockages
            if new_pos == self.agent_pos or \
                (tuple(self.agent_pos) in self.E_BLOCK_POSITIONS and self.DIRECTIONS[prev_direction] == "E") or \
                (tuple(self.agent_pos) in self.SE_BLOCK_POSITIONS and self.DIRECTIONS[prev_direction] in ["E", "S"]) or \
                (tuple(self.agent_pos) in self.WE_BLOCK_POSITIONS and self.DIRECTIONS[prev_direction] in ["E", "W"]) or \
                (tuple(self.agent_pos) in self.NE_BLOCK_POSITIONS and self.DIRECTIONS[prev_direction] in ["E", "N"]) or \
                (tuple(self.agent_pos) in self.W_BLOCK_POSITIONS and self.DIRECTIONS[prev_direction] == "W"):
                new_pos = self.agent_pos  # Stay in place

            self.agent_pos = new_pos
        
        return self.agent_pos == self.target_pos
    

    def render(self):
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                if [r, c] == self.agent_pos:
                    print(GridTile.AGENT, end=' ')
                elif [r, c] == self.target_pos:
                    print(GridTile.TARGET, end=' ')
                else:
                    print(GridTile._FLOOR, end=' ')
            print()
        print()

        self._process_events()
        self.window_surface.fill((255,255,255))

        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                pos = (c * self.cell_width, r * self.cell_height)
                if (r, c) in self.E_BLOCK_POSITIONS:
                    self.window_surface.blit(self.floor_EBlock_img, pos)
                elif (r, c) in self.SE_BLOCK_POSITIONS:
                    self.window_surface.blit(self.floor_SEBlock_img, pos)
                else:
                    self.window_surface.blit(self.floor_img, pos)

                if [r, c] == self.target_pos:
                    self.window_surface.blit(self.goal_img, pos)

                if [r, c] == self.agent_pos:
                    if self.DIRECTIONS[self.direction] == 'N':
                        self.window_surface.blit(self.Agent_N_direct_img, pos)
                    elif self.DIRECTIONS[self.direction] == 'S':
                        self.window_surface.blit(self.Agent_S_direct_img, pos)
                    elif self.DIRECTIONS[self.direction] == 'W':
                        self.window_surface.blit(self.Agent_W_direct_img, pos)
                    else:
                        self.window_surface.blit(self.Agent_E_direct_img, pos)

        direction_str = self.DIRECTIONS[self.direction]
        text_img = self.action_font.render(f'A: {self.last_action}, D: {direction_str}', True, (0, 0, 0), (255, 255, 255))
        text_pos = (0, self.window_size[1] - self.action_info_height)
        self.window_surface.blit(text_img, text_pos)

        pygame.display.update()
        self.clock.tick(self.fps)

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    agent = BossAgent()
    agent.render()
    while True:
        action = random.choice(list(AgentAction))
        agent.perform_action(action)
        agent.render()