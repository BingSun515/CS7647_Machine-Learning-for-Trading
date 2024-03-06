""""""  		  	   		 	   			  		 			     			  	 
"""Assess a betting strategy.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	   			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		 	   			  		 			     			  	 
All Rights Reserved  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Template code for CS 4646/7646  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	   			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		 	   			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		 	   			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		 	   			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	   			  		 			     			  	 
or edited.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		 	   			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		 	   			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	   			  		 			     			  	 
GT honor code violation.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
-----do not edit anything above this line---  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Student Name: Bing Sun (replace with your name)  		  	   		 	   			  		 			     			  	 
GT User ID: bsun*** (replace with your User ID)  		  	   		 	   			  		 			     			  	 
GT ID: ******* (replace with your GT ID)  		  	   		 	   			  		 			     			  	 
"""
import numpy as np
import matplotlib.pyplot as plt
import os


def author():
    """  		  	   		 	   			  		 			     			  	 
    :return: The GT username of the student  		  	   		 	   			  		 			     			  	 
    :rtype: str  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    return "bsun***"  # replace tb34 with your Georgia Tech username.


def gtid():  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    :return: The GT ID of the student  		  	   		 	   			  		 			     			  	 
    :rtype: int  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    return *******  # replace with your GT ID number


def get_spin_result(win_prob):
    """  		  	   		 	   			  		 			     			  	 
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		 	   			  		 			     			  	 
    :param win_prob: The probability of winning  		  	   		 	   			  		 			     			  	 
    :type win_prob: float  		  	   		 	   			  		 			     			  	 
    :return: The result of the spin.  		  	   		 	   			  		 			     			  	 
    :rtype: bool  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    result = False  		  	   		 	   			  		 			     			  	 
    if np.random.random() <= win_prob:
        result = True  		  	   		 	   			  		 			     			  	 
    return result


def test_code():

    """  		  	   		 	   			  		 			     			  	 
    Method to test your code  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    win_prob = 18/38  # set appropriately to the probability of a win
    np.random.seed(gtid())  # do this only once
    print(get_spin_result(win_prob))  # test the roulette spin  		  	   		 	   			  		 			     			  	 
    # add your code here to implement the experiments


def strategy(wp):
    res = [0]
    episode_winnings = 0
    bet_times = 0
    while episode_winnings < 80 and bet_times < 1000:
        won = False
        bet_amount = 1
        while not won:
            won = get_spin_result(wp)
            bet_times += 1
            if bet_times > 1000:
                break
            if won:
                episode_winnings = episode_winnings + bet_amount
            else:
                episode_winnings = episode_winnings - bet_amount
                bet_amount = bet_amount * 2
            res.append(episode_winnings)
    while len(res) < 300:
        res.append(80)

    res = np.array(res)
    return res


def realistic_strategy(wp):
    res = [0]
    episode_winnings = 0
    bet_times = 0
    while episode_winnings < 80 and bet_times < 1000 and episode_winnings > -256:
        won = False
        bet_amount = 1
        while not won:
            won = get_spin_result(wp)
            bet_times += 1
            if bet_times > 1000:
                break
            if won:
                episode_winnings = episode_winnings + bet_amount
            else:
                episode_winnings = episode_winnings - bet_amount
                if episode_winnings <= -256:
                    break
                else:
                    bet_amount = bet_amount * 2
                    if bet_amount > episode_winnings + 256:
                        bet_amount = episode_winnings + 256

            res.append(episode_winnings)

    while len(res) < 300:
        if res[-1] == 80:
            res.append(80)
        else:
            res.append(-256)
    res = np.array(res)[:300]
    return res


def get_cmap(n, name='hsv'):
    return plt.cm.get_cmap(name, n)


def figure_default_settings():
    plt.figure(figsize=(10, 6))
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Bet_Times')
    plt.ylabel('Episode_Winnings')
    plt.grid(True)


def figure_1():
    figure_default_settings()
    num_episode = 10
    cmap = get_cmap(num_episode) # obtain color map
    for i in range(num_episode):
      data = strategy(18/38)
      label = "Episode" + str(i + 1)
      plt.plot(data, '-',label=label,linewidth=0.5,c=cmap(i))
    plt.title('Figure_1')
    plt.legend()
    plt.savefig('images/figure_1.png')


def figure_2():
    figure_default_settings()
    num_episode = 1000
    data_list = []
    for i in range(num_episode):
        data = strategy(18 / 38)
        data_list.append(data)
    stacked_data = np.stack(data_list, axis=0)
    mean_data = np.mean(stacked_data, axis=0)
    std_deviation = np.std(stacked_data, axis=0)
    meanplus_std = mean_data + std_deviation
    meanminus_std = mean_data - std_deviation
    plt.plot(mean_data, '-', label='Mean', linewidth=0.5)
    plt.plot(meanplus_std, '-', label='Mean + STD', linewidth=0.5)
    plt.plot(meanminus_std, '-', label='Mean - STD', linewidth=0.5)
    plt.title('Figure_2')
    plt.legend()
    plt.savefig('images/figure_2.png')


def figure_3():
    figure_default_settings()
    num_episode = 1000
    data_list = []
    for i in range(num_episode):
        data = strategy(18 / 38)
        data_list.append(data)
    stacked_data = np.stack(data_list, axis=0)
    median_data = np.median(stacked_data, axis=0)
    std_deviation = np.std(stacked_data, axis=0)
    medianplus_std = median_data + std_deviation
    medianminus_std = median_data - std_deviation
    plt.plot(median_data, '-', label='Median', linewidth=0.5)
    plt.plot(medianplus_std, '-', label='Median + STD', linewidth=0.5)
    plt.plot(medianminus_std, '-', label='Median - STD', linewidth=0.5)
    plt.title('Figure_3')
    plt.legend()
    plt.savefig('images/figure_3.png')


def figure_4():
    figure_default_settings()
    num_episode = 1000
    data_list = []
    for i in range(num_episode):
        data = realistic_strategy(18 / 38)
        data_list.append(data)
    stacked_data = np.stack(data_list, axis=0)
    mean_data = np.mean(stacked_data, axis=0)
    std_deviation = np.std(stacked_data, axis=0)
    meanplus_std = mean_data + std_deviation
    meanminus_std = mean_data - std_deviation
    plt.plot(mean_data, '-',  label = 'Mean', linewidth=0.5)
    plt.plot(meanplus_std, '-', label = 'Mean + STD', linewidth=0.5)
    plt.plot(meanminus_std, '-', label = 'Mean - STD', linewidth=0.5)
    plt.title('Figure_4')
    plt.legend()
    plt.savefig('images/figure_4.png')


def figure_5():
    figure_default_settings()
    num_episode = 1000
    data_list = []
    for i in range(num_episode):
        data = realistic_strategy(18 / 38)
        data_list.append(data)
    stacked_data = np.stack(data_list, axis=0)
    median_data = np.median(stacked_data, axis=0)
    std_deviation = np.std(stacked_data, axis=0)
    medianplus_std = median_data + std_deviation
    medianminus_std = median_data - std_deviation
    plt.plot(median_data, '-', label='Median', linewidth=0.5)
    plt.plot(medianplus_std, '-', label='Median + STD', linewidth=0.5)
    plt.plot(medianminus_std, '-', label='Median - STD', linewidth=0.5)
    plt.title('Figure_5')
    plt.legend()
    plt.savefig('images/figure_5.png')


def question1():
    res = []
    for j in range(1000):
        amount = []
        for i in strategy(18 / 38):
            if i == 80:
                amount.append(i)
        res.append(len(amount))
    k = 0
    for i in res:
        if i >= 0:
            k += 1
    return k


def question2():
    res = 0
    for j in range(10000):
        for i in realistic_strategy(18 / 38):
            if i == 80:
                res += 1
                break
            continue
    return res


def question6():
    num_episode = 1000
    data_list = []
    for i in range(num_episode):
        data = realistic_strategy(18 / 38)
        data_list.append(data)
    stacked_data = np.stack(data_list, axis=0)
    mean_data = np.mean(stacked_data, axis=0)
    std_deviation = np.std(stacked_data, axis=0)
    meanplus_std = mean_data + std_deviation
    meanminus_std = mean_data - std_deviation
    return mean_data[-10:], meanplus_std[-10:], meanminus_std[-10:]


def report_q():
    # Sample output results
    # Specify the file path
    file_path = "p1_results.txt"
    # Open the file in write mode
    with open(file_path, 'w') as file:
        # Write the output results to the file

        q1_intro = """Question 1:
    The simulation is executed across 1000 episodes 
    of initial strategy (strategy) to determine the 
    numbers of episodes required for the winnings to
    reach $80.\nThe Q1 output is: \n"""
        q2_intro = """Question 2:
    The simulation is executed across 10000 episodes 
    of improved strategy (realistic_strategy) to 
    determine the numbers of episodes required for"
    the winnings to reach $80. \nThe Q4 output is: \n"""
        q6_intro = """Question 6:
    The simulation is executed across 1000 episodes 
    of improved stratege (realistic_strategy) to 
    output the last ten elememnts in the array of 
    mean, mean + std, and mean - std. \nThe Q6 output is: \n"""
        file.write(q1_intro)
        file.write(str(question1()) + '\n')
        file.write(q2_intro)
        file.write(str(question2()) + '\n')
        file.write(q6_intro)
        file.write(str(question6()) + '\n')

figure_1()
figure_2()
figure_3()
figure_4()
figure_5()
report_q()

if __name__ == "__main__":
    test_code()
