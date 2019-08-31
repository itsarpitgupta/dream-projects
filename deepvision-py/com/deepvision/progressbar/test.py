import sys
from time import sleep
from tqdm import tqdm

for i in tqdm(range(0, 10), desc="Main Tool"):
    for j in tqdm(range(0, 3), desc="Second Loop"):
        sleep(0.5)
