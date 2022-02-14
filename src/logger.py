import os
import time
# import matplotlib.pyplot as plt
# import csv

class MetricLogger:
    def __init__(self, logdir):
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        self.log_file_name = f'{logdir}/log.csv'
        self.fields = ['Episode', 'Step', 'Epsilon', 'Avg Reward', 'Avg Length', 'Avg Loss', 'Avg Q Value', 'Time Delta', 'Time']
        self.episode_rewards_plot = f'{logdir}/rewards.jpg'
        self.episode_lengths_plot = f'{logdir}/lengths.jpg'
        self.episode_avg_losses_plot = f'{logdir}/losses.jpg'
        self.episode_avg_q_values_plot = f'{logdir}/Qvalues.jpg'

        self.episode_rewards = []
        self.episode_lengths = []
        self.episode_avg_losses = []
        self.episode_avg_q_values = []
        self.moving_avg_episode_rewards = []
        self.moving_avg_episode_lengths = []
        self.moving_avg_episode_avg_losses = []
        self.moving_avg_episode_avg_q_values = []

        self.current_episode_reward = self.current_episode_length = self.current_episode_loss = self.current_episode_q_value = self.current_episode_loss_length = 0

        self.init_episode()
        self.record_time = time.time()

    def init_episode(self):
        self.current_episode_reward = self.current_episode_length = self.current_episode_loss = self.current_episode_q_value = self.current_episode_loss_length = 0

    def log_step(self, reward, loss, q_value):
        self.current_episode_reward = self.current_episode_reward + reward
        self.current_episode_length = self.current_episode_length + 1

        if not loss == 0:
            self.current_episode_loss = self.current_episode_loss + loss
            self.current_episode_q_value = self.current_episode_q_value + q_value
            self.current_episode_loss_length = self.current_episode_loss_length + 1

    def log_episode(self):
        self.episode_rewards.append(self.current_episode_reward)
        self.episode_lengths.append(self.current_episode_length)
        self.episode_avg_losses.append(0 if self.current_episode_loss_length == 0 else round(self.current_episode_loss / self.current_episode_loss_length, ndigits=5))
        self.episode_avg_q_values.append(0 if self.current_episode_loss_length == 0 else round(self.current_episode_q_value / self.current_episode_loss_length, ndigits=5))
        self.init_episode()

    def record(self, episode, epsilon, step):
        mean_ep_reward = np.round(np.mean(self.ep_rewards[-100:]), 3)
        mean_ep_length = np.round(np.mean(self.ep_lengths[-100:]), 3)
        mean_ep_loss = np.round(np.mean(self.ep_avg_losses[-100:]), 3)
        mean_ep_q = np.round(np.mean(self.ep_avg_qs[-100:]), 3)
        self.moving_avg_ep_rewards.append(mean_ep_reward)
        self.moving_avg_ep_lengths.append(mean_ep_length)
        self.moving_avg_ep_avg_losses.append(mean_ep_loss)
        self.moving_avg_ep_avg_qs.append(mean_ep_q)

        last_record_time = self.record_time
        self.record_time = time.time()
        time_since_last_record = np.round(self.record_time - last_record_time, 3)

        print(
            f"Episode {episode} - "
            f"Step {step} - "
            f"Epsilon {epsilon} - "
            f"Mean Reward {mean_ep_reward} - "
            f"Mean Length {mean_ep_length} - "
            f"Mean Loss {mean_ep_loss} - "
            f"Mean Q Value {mean_ep_q} - "
            f"Time Delta {time_since_last_record} - "
            f"Time {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}"
        )

        with open(self.save_log, "a") as f:
            f.write(
                f"{episode:8d}{step:8d}{epsilon:10.3f}"
                f"{mean_ep_reward:15.3f}{mean_ep_length:15.3f}{mean_ep_loss:15.3f}{mean_ep_q:15.3f}"
                f"{time_since_last_record:15.3f}"
                f"{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'):>20}\n"
            )

        for metric in ["ep_rewards", "ep_lengths", "ep_avg_losses", "ep_avg_qs"]:
            plt.plot(getattr(self, f"moving_avg_{metric}"))
            plt.savefig(getattr(self, f"{metric}_plot"))
            plt.clf()