import gym # type: ignore
from gym.spaces import Box # type: ignore
import numpy as np # type: ignore

class RelativePostion(gym.ObservationWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.observation_space = Box(shape=(2,), low=-np.inf, high=np.inf)

    def observation(self, obs):
        return obs['target'] - obs['agent']