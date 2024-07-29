from gym.envs.registration import register # type: ignore

register(
    id="GymBoss/BossGame-v0",
    entry_point="GymBoss.envs:BossEnv"
)