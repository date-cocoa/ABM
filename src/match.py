import numpy as np
import random
import matplotlib.pyplot as plt

N_MEN = 50
N_WOMEN = 50
MEAN = 50
SD = 10

# これはいじらない
TIME = 1000
OVER_TIME = 1000

attr_true_men = np.random.normal(loc=MEAN, scale=SD, size=N_MEN)
attr_true_women = np.random.normal(loc=MEAN, scale=SD, size=N_WOMEN)

attr_swipe_men = attr_true_men + np.random.normal(loc=0, scale=5, size=N_MEN)
attr_meet_men = attr_true_men + np.random.normal(loc=0, scale=5, size=N_MEN)

attr_swipe_women = attr_true_women + np.random.normal(loc=0, scale=5, size=N_WOMEN)
attr_meet_women = attr_true_women + np.random.normal(loc=0, scale=5, size=N_WOMEN)

result = []
for _ in range(OVER_TIME):
    N_DATE = 0
    for _ in range(TIME):
        idx_man = random.randint(0, N_MEN-1)
        idx_woman = random.randint(0, N_WOMEN-1)

        diff_swipe = attr_swipe_men[idx_man] - attr_swipe_women[idx_woman]
        if diff_swipe >= 10:
            # マッチする
            if np.random.binomial(1, diff_swipe/100) == 1:
                # 会う
                diff_meet = abs(attr_meet_men[idx_man] - attr_meet_women[idx_woman])
                if diff_meet < 5:
                    # 付き合う
                    N_DATE += 1
                else:
                    pass # 付き合わない
            else:
                pass # 会わない
        else:
            pass # マッチしない
    
    result.append(N_DATE)

mean_result = np.mean(result)
print(f'カップルの人数の平均値は{mean_result}人です！')