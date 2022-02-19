import numpy as np
import datetime

from game.game import Game
from agent.agent import Siam
from utils.logger import MetricLogger
from utils.plotter import plot

def generate_state(frames):
    rgb_to_grayscale_parameters = np.array([0.2989, 0.5870, 0.1140])
    state = np.stack(frames)
    return np.dot(state, rgb_to_grayscale_parameters)

scores = []
avg_scores = []
best_score = 0

num_frames = num_skips = 5
state_dim = (num_frames, 32, 32)
num_episodes = int(4e4)
start_time = datetime.datetime.now().strftime("%Y.%m.%d(%a)@%H.%M.%S")

game = Game()
siam = Siam(state_dim=state_dim, action_dim=2)
metric_logger = MetricLogger(logdir=f'../logs', filename=f'log_{start_time}.csv')

for episode in range(num_episodes):
    initial_frame = game.reset()
    frames = [np.zeros(initial_frame.shape)] * (num_frames - 1) + [initial_frame / 255]
    state = generate_state(frames)

    while True:
        action = siam.act(state)

        frames = []
        total_reward = score = 0
        game_over = False

        for skip in range(num_skips):
            next_frame, reward, game_over, score = game.step(action)
            frames.append(next_frame / 255)
            total_reward = total_reward + reward

            if game_over:
                break

        frames = frames + [np.zeros(initial_frame.shape)] * (num_skips - len(frames))
        next_state = generate_state(frames)

        siam.cache((state, next_state, action, total_reward, game_over))
        q_value, loss = siam.learn()

        metric_logger.log_step(total_reward, loss, q_value)
        state = next_state

        if game_over:
            if score > best_score:
                best_score = score

            if episode % 500 == 0:
                siam.model.save(modeldir=f'../models/models_{start_time}', filename=f'model_{datetime.datetime.now().strftime("%Y.%m.%d(%a)@%H.%M.%S")}.pt', current_episode=episode)

            scores.append(score)
            avg_scores.append(sum(scores) / len(scores))

            print(f'Episode: {episode + 1} - Score: {scores[-1]} - Avg Score: {avg_scores[-1]} - Best Score: {best_score}')
            plot(scores, avg_scores)

            break

    metric_logger.log_episode()

    if episode % 40 == 0:
        metric_logger.record(episode=episode, step=siam.current_step, epsilon=siam.exploration_rate)
