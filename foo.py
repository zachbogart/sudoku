import numpy as np

all_three = list(np.array([1,2,3]))

all_three.remove([[4]])

all_three = np.array([1,2,3,4,5,7,8,9])

new_number = np.setdiff1d(all_three, range(1,10))
print(new_number)

row = [0,1,2,3,4]
col = [0, 2,6,7,8]
box = [9, 8, 6, 5]

all_three = np.array(row + col + box)
all_three = np.sort(all_three[all_three != 0])
if unique:
    all_three = np.unique(all_three)
