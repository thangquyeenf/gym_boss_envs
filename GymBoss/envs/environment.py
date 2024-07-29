
import gym # type: ignore
from gym import spaces # type: ignore
import numpy as np # type: ignore
import GymBoss.envs.agent as agent
# from gym.envs.registration import register

# register(
#     id='warehouse-robot-v0',
#     entry_point='environment:BossEnv',
# )

class BossEnv(gym.Env):
    metadata = {"render_mode": ["human"], "render_fps": 4}

    def __init__(self, grid_rows = 4, grid_cols = 4, render_mode=None):
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.render_mode = render_mode

        self.agent = agent.BossAgent(grid_rows=grid_rows, grid_cols=grid_cols, fps=self.metadata['render_fps'])

        self.action_space = spaces.Discrete(len(agent.AgentAction))

        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0]),
            high=np.array([self.grid_rows-1, self.grid_cols-1, 3]),
            dtype=np.int32
        )

    def _get_obs(self):
        return np.concatenate((self.agent.agent_pos, [self.agent.direction]))

    def _get_info(self):
        return {
            
        }

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.agent.reset(seed=seed)
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == 'human':
            self.render()
        
        return observation, info
    
    def step(self, action):
        target_reached = self.agent.perform_action(agent.AgentAction(action))
        reward = 0
        done = False
        if target_reached:
            reward = 100
            done = True
        
        observation = self._get_obs()
        info = self._get_info()
        if self.render_mode == 'human':
            print(agent.AgentAction(action))
            self.render()
        
        return observation, reward, done, False, info
    
    def render(self):
        self.agent.render()



# if __name__ == "__main__":
#     env = gym.make('warehouse-robot-v0', render_mode='human')

#     obs = env.reset()[0]

#     terminated = False
#     step = 0
#     while not terminated:
#         rand_action = env.action_space.sample()
#         obs, reward, terminated, _, _ = env.step(rand_action)
#         step += 1
#         print("Step: ", step)