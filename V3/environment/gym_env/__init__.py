from gym.envs.registration import register

register(
    id='trackmania-v1',
    entry_point='gym_env.envs:TrackmaniaEnv',
)
