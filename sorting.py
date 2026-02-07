import math
import time

def selection_sort(numbers, count, yield_state=False):
    n = len(numbers)
    count.setdefault("comparisons", 0)
    count.setdefault("swaps", 0)

    for i in range(n):
        m = i
        for j in range(i + 1, n):
            count["comparisons"] += 1
            if numbers[j] < numbers[m]:
                m = j
            
            if yield_state:
                time.sleep(0.02)
                yield numbers
        
        numbers[i], numbers[m] = numbers[m], numbers[i]
        count["swaps"] += 1
            

def insertion_sort(numbers, count, yield_state=False):
    n = len(numbers)
    count.setdefault("comparisons", 0)
    count.setdefault("swaps", 0)
    
    for i in range(1, n):
        key = numbers[i]
        j = i - 1
        
        while j >= 0 and key < numbers[j]:
            count["comparisons"] += 1
            numbers[j + 1] = numbers[j]
            count["swaps"] += 1
            j -= 1

            if yield_state:
                time.sleep(0.02)
                yield numbers

        

        numbers[j + 1] = key
        count["swaps"] += 1
        if yield_state:
                time.sleep(0.02)
                yield numbers
        


def bubble_sort(numbers, count, yield_state=False):
    n = len(numbers)
    count.setdefault("comparisons", 0)
    count.setdefault("swaps", 0)

    for i in range(n, 0, -1):
        for j in range(0, i - 1):
            count["comparisons"] += 1
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                count["swaps"] += 1
            if yield_state:
                time.sleep(0.02)
                yield numbers


def shell_insertion_logic(numbers, count, gaps, yield_state=False):
    n = len(numbers)
    count.setdefault("comparisons", 0)
    count.setdefault("swaps", 0)

    for gap in gaps:
        for i in range(gap, n):
            key = numbers[i]
            j = i - gap
            while j >= 0:
                count["comparisons"] += 1
                if key < numbers[j]:
                    numbers[j + gap] = numbers[j]
                    count["swaps"] += 1
                    j -= gap

                    if yield_state:
                        time.sleep(0.02)
                        yield numbers

                else:
                    break
            numbers[j + gap] = key
            count["swaps"] += 1
            if yield_state:
                time.sleep(0.02)
                yield numbers


def shell_bubble_logic(numbers, count, gaps, yield_state=False):
    n = len(numbers)
    count.setdefault("comparisons", 0)
    count.setdefault("swaps", 0)

    for gap in gaps:
        for i in range(n, gap, -1):
            for j in range(0, i - gap):
                count["comparisons"] += 1
                if numbers[j] > numbers[j + gap]:
                    numbers[j], numbers[j + gap] = numbers[j + gap], numbers[j]
                    count["swaps"] += 1
                if yield_state:
                    time.sleep(0.02)
                    yield numbers


# Helper to generate gap sequences
def get_gaps(n, method, custom_gaps=None):
    if method == "shell": # N/2^k
        gaps = []
        g = n // 2
        while g > 0:
            gaps.append(g)
            g //= 2
        return gaps
    elif method == "hibbard": # 2^k - 1
        gaps = []
        k = 1
        while (2**k - 1) < n:
            gaps.append(2**k - 1)
            k += 1
        return gaps[::-1]
    elif method == "knuth": # (3^k - 1) / 2
        gaps = []
        k = 1
        while True:
            val = (3**k - 1) // 2
            if val > math.ceil(n / 3):
                break
            gaps.append(val)
            k += 1
        return gaps[::-1]
    elif method == "custom":
        return custom_gaps
    return [1]