import gym # type: ignore
import GymBoss

if __name__ == "__main__":
    env = gym.make("GymBoss/BossGame-v0")

    obs = env.reset()[0]

    terminated = False
    step = 0
    while not terminated:
        rand_action = env.action_space.sample()
        obs, reward, terminated, _, _ = env.step(rand_action)
        step += 1
        print("Step: ", step)
