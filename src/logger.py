import os
import csv
import time
import datetime

class MetricLogger:
    def __init__(self, logdir):
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        self.log_file_name = f'{logdir}/log.csv'

        with open(self.log_file_name, 'w') as log_file:
            csv_writer = csv.writer(log_file)
            csv_writer.writerow(['Episode', 'Step', 'Epsilon', 'Avg Reward', 'Avg Length', 'Avg Loss', 'Avg Q Value', 'Time Delta', 'Current Time'])

        self.episode_rewards = []
        self.episode_lengths = []
        self.episode_avg_losses = []
        self.episode_avg_q_values = []

        self.current_episode_reward = self.current_episode_length = self.current_episode_loss = self.current_episode_q_value = self.current_episode_loss_length = 0

        self.init_episode()
        self.record_time = time.time()

    def init_episode(self):
        self.current_episode_reward = self.current_episode_length = self.current_episode_loss = self.current_episode_q_value = self.current_episode_loss_length = 0

    def log_step(self, reward, loss, q_value):
        self.current_episode_reward = self.current_episode_reward + reward
        self.current_episode_length = self.current_episode_length + 1

        if loss:
            self.current_episode_loss = self.current_episode_loss + loss
            self.current_episode_q_value = self.current_episode_q_value + q_value
            self.current_episode_loss_length = self.current_episode_loss_length + 1

    def log_episode(self):
        self.episode_rewards.append(self.current_episode_reward)
        self.episode_lengths.append(self.current_episode_length)
        self.episode_avg_losses.append(0 if self.current_episode_loss_length == 0 else round(self.current_episode_loss / self.current_episode_loss_length, ndigits=5))
        self.episode_avg_q_values.append(0 if self.current_episode_loss_length == 0 else round(self.current_episode_q_value / self.current_episode_loss_length, ndigits=5))
        self.init_episode()

    def record(self, episode, step, epsilon):
        mean_episode_reward = round(0 if len(self.episode_rewards[-100:]) == 0 else sum(self.episode_rewards[-100:]) / len(self.episode_rewards[-100:]), ndigits=3)
        mean_episode_length = round(0 if len(self.episode_lengths[-100:]) == 0 else sum(self.episode_lengths[-100:]) / len(self.episode_lengths[-100:]), ndigits=3)
        mean_episode_avg_loss = round(0 if len(self.episode_avg_losses[-100:]) == 0 else sum(self.episode_avg_losses[-100:]) / len(self.episode_avg_losses[-100:]), ndigits=3)
        mean_episode_avg_q_value = round(0 if len(self.episode_avg_q_values[-100:]) == 0 else sum(self.episode_avg_q_values[-100:]) / len(self.episode_avg_q_values[-100:]), ndigits=3)

        last_record_time = self.record_time
        self.record_time = time.time()
        time_spent_after_last_record = round(self.record_time - last_record_time, ndigits=3)

        print(f'Episode: {episode} - Step: {step} - Epsilon: {epsilon} - Avg Reward: {mean_episode_reward} - Avg Length: {mean_episode_length} - Avg Loss: {mean_episode_avg_loss} - Avg Q Value: {mean_episode_avg_q_value} - Time Delta: {time_spent_after_last_record} - Current Time: {datetime.datetime.now().strftime("%Y/%m/%d(%a)@%H:%M:%S")}')

        with open(self.log_file_name, 'a') as log_file:
            csv_writer = csv.writer(log_file)
            csv_writer.writerow([episode, step, epsilon, mean_episode_reward, mean_episode_length, mean_episode_avg_loss, mean_episode_avg_q_value, time_spent_after_last_record, datetime.datetime.now().strftime("%Y/%m/%d(%a)@%H:%M:%S")])
