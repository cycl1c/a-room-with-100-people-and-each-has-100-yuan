#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# date:    2022.04.24
# author:  cycl1c
#

import matplotlib.pyplot as plt
import random
random.seed(5)

# 设置模拟的次数
loop = 10000
# 设置人数
player_number = 100
# 设置求解第几小问(flag = 1,2,3,4,5)
flag = 1


class Player():
    def __init__(self, number):
        self.number = number
        self.money = 100
        self.state = 1  # 0表示穷人，2表示富人
    
    def get_target(self, lengh):
        while self.number == random.randint(0, lengh-1):
            random.randint(0, lengh-1)
        return random.randint(0, lengh-1)

    def get_state_loanable(self):
        if self.money > 200:
            self.state = 2
        elif self.money > 50:
            self.state = 1
        else:
            self.state = 0
        return self.state
    
    def get_state_not_loanable(self):
        if self.money > 200:
            self.state = 2
        elif self.money > 50:
            self.state = 1
        elif self.money > 0:
            self.state = 0
        return self.state

    def random_cost(self):
        return random.choice([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2])

    def transaction_loanable(self, players):
        target = self.get_target(player_number)
        self.money -= 1
        players[target].money += 1

    def transaction_loanable_with_RandomCost(self, players):
        target = self.get_target(player_number)
        self.money -= self.random_cost()
        players[target].money += 1

    def transaction_loanable_with_RandomCost_and_Tax(self, players, tax, compensation, num):
        target = self.get_target(player_number)
        self.money -= self.random_cost()
        if self.get_state_loanable() == 0:
            num += 1
        if players[target].get_state_loanable() == 2:
            players[target].money += (1-tax)
            compensation += tax
        else:
            players[target].money += 1
        return compensation, num

    def transaction_not_loanable(self, remaining_players):
        target = self.get_target(len(remaining_players))
        self.money -= 1
        remaining_players[target].money += 1

    def transaction_not_loanable_with_tax(self, remaining_players, tax, compensation, num):
        target = self.get_target(len(remaining_players))
        self.money -= 1
        if self.get_state_not_loanable() == 0:
            num += 1
        if remaining_players[target].get_state_not_loanable() == 2:
            remaining_players[target].money += (1-tax)
            compensation += tax
        else:
            remaining_players[target].money += 1
        return compensation, num
        
        
players = [Player(i) for i in range(player_number)]
remaining_players = players[:]
if flag == 4 or flag == 5:
    pool_num = 15
    rich_num = 5
else:
    pool_num = 0
    rich_num = 0
for i in range(loop):
    # 5种情况
    if flag == 1:
        for player in players:
            player.transaction_loanable(players)
    if flag == 2:
        for player in remaining_players:
            player.transaction_not_loanable(remaining_players)
            if player.money == 0:
                remaining_players.remove(player)
    if flag == 3:
        '''
        假设金钱∈(200,∞)的玩家为富人，(0,50]以下的为穷人。对富人每一笔交易征税的税率为25%，税金将平均地分给穷人。
        '''
        compensation = 0    # 表示累计的税金
        num = 0             # 表示 remaining_players 中穷人的人数
        for player in remaining_players:
            compensation, num = player.transaction_not_loanable_with_tax(remaining_players, 0.25, compensation, num)   # 税率要用小数表示
            if player.money < 1:    # 现金不足一块，无法给别人钱
                remaining_players.remove(player)
        for player in remaining_players:
            if player.get_state_not_loanable() == 0:
                player.money += (compensation / num)
    if flag == 4:
        '''
        每人每次付出的成本在[0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]中随机选择。最初设定15个穷人每人持有50元，5个富人每人持有250元，其余的人均持有100元
        '''
        for player in players[:pool_num]:
            player.money = 50
        for player in players[-rich_num:]:
            player.money = 250
        for player in players:
            player.transaction_loanable_with_RandomCost(players)
    if flag == 5:
        '''
        每人每次付出的成本在[0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]中随机选择。最初设定15个穷人每人持有50元，5个富人每人持有250元，其余的人均持有100元
        假设金钱∈(200,∞)的玩家为富人，(-∞,50]以下的为穷人。对富人每一笔交易征税的税率为25%，税金将平均地分给穷人。
        '''
        # 初始化
        compensation = 0    # 表示累计的税金
        num = 0             # 表示 players 中穷人的人数
        for player in players[:pool_num]:
            player.money = 50
        for player in players[-rich_num:]:
            player.money = 250
        # 开始一轮模拟
        for player in players:
            compensation, num = player.transaction_loanable_with_RandomCost_and_Tax(players, 0.25, compensation, num)   # 税率要用小数表示
        # 一轮模拟结束后对穷人发放补偿金
        for player in players:
            if player.get_state_loanable() == 0:
                player.money += (compensation / num)

# 作图
distribution = [player.money for player in players]
numbers = [player.number+1 for player in players]
plt.figure(1)
plt.xlabel('player')
plt.ylabel('money')
color_backup = ['g']*pool_num + ['steelblue']*(100-pool_num-rich_num) + ['r']*rich_num
plt.bar(numbers, distribution, color = color_backup)
# 排序
plt.figure(2)
plt.xlabel('player')
plt.ylabel('money')
plt.bar(numbers, sorted(distribution))
plt.show()