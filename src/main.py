import numpy as np
import datetime
import os
from PIL import Image
import torch

from game.game import Game
from agent.agent import Siam
from utils.logger import MetricLogger
from utils.plotter import plot

num_frames = num_skips = 5
state_dim = (num_frames, 32, 32)
action_dim = 2

def generate_state(frames):
    rgb_to_grayscale_parameters = np.array([0.2989, 0.5870, 0.1140])
    state = np.stack(frames)
    return np.dot(state, rgb_to_grayscale_parameters)

def train():
    scores = []
    avg_scores = []
    best_score = 0

    num_episodes = int(4e4)
    start_time = datetime.datetime.now().strftime("%Y.%m.%d(%a)@%H.%M.%S")

    game = Game()
    siam = Siam(state_dim=state_dim, action_dim=action_dim)
    metric_logger = MetricLogger(logdir=f'../logs', filename=f'log_{start_time}.csv')

    take_snapshot = False

    for episode in range(num_episodes):
        initial_frame = game.reset()
        frames = [np.zeros(initial_frame.shape)] * (num_frames - 1) + [initial_frame / 255]
        state = generate_state(frames)

        if take_snapshot:
            if not os.path.exists('../snapshots'):
                os.makedirs('../snapshots')

            Image.fromarray(initial_frame).save('../snapshots/initial_frame_colored.png')
            Image.fromarray((state[num_frames - 1] * 255).astype(np.uint8)).save('../snapshots/initial_frame_black_and_white.png')

            take_snapshot = False

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
                    siam.model.save(modeldir=f'../models/models_{start_time}', filename=f'checkpoint_{datetime.datetime.now().strftime("%Y.%m.%d(%a)@%H.%M.%S")}.pth', current_episode=episode, current_exploration_rate=siam.exploration_rate)

                scores.append(score)
                avg_scores.append(sum(scores) / len(scores))

                print(f'Episode: {episode + 1} - Score: {scores[-1]} - Avg Score: {avg_scores[-1]} - Best Score: {best_score}')
                plot(scores, avg_scores)

                break

        metric_logger.log_episode()

        if episode % 40 == 0:
            metric_logger.record(episode=episode, step=siam.current_step, epsilon=siam.exploration_rate)

def play():
    checkpoint_path = '../models/models_2022.02.20(Sun)@15.45.25/model_2022.02.20(Sun)@20.06.55.pt'
    checkpoint = torch.load(checkpoint_path)

    model = checkpoint['model'] if 'model' in checkpoint else None
    current_episode = checkpoint['current_episode'] if 'current_episode' in checkpoint else -1
    current_exploration_rate = checkpoint['current_exploration_rate'] if 'current_exploration_rate' in checkpoint else -1

    assert model is not None, 'Loaded model is None. Aborting program.'

    num_episodes = 10

    game = Game()
    siam = Siam(state_dim=state_dim, action_dim=action_dim)

    siam.model.load_state_dict(model)
    siam.model.eval()
    siam.exploration_rate = current_exploration_rate

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
            state = generate_state(frames)

            if game_over:
                print(f'Episode: {current_episode + episode + 1} - Score: {score}')
                break

if __name__ == '__main__':
    do_train = False

    if do_train:
        train()
    else:
        play()
