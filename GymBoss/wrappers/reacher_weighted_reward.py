import gym # type: ignore

class ReacherRewardWrapper(gym.Wrapper):
    def __init__(self, env, reward_dist_weight, reward_crtl_weight):
        super().__init__(env)
        self.reward_dist_weight = reward_dist_weight
        self.reward_ctrl_weight =reward_crtl_weight

    def step(self, action):
        observation, _, done, truncated, info = self.env.step(action)
        reward = (
            self.reward_dist_weight * info["reward_dist"]
            + self.reward_ctrl_weight * info["reward_ctrl"]
        )

        return observation, reward, done, truncated, info