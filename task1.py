from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
import copy

directions = [(-1,0), (1,0), (0,1), (0,-1)]

def args_zip(x : int, y : int, cnt : int, n, visited, deepth, path_tag):
    return (x, y, cnt, n, copy.deepcopy(visited), deepth, path_tag)

def walk_ziped_args(args):
    return walk(args[0], args[1], args[2], args[3], args[4], args[5], args[6])

def walk(x : int, y : int, cnt : int, n, visited, deepth, path_tag, args_pool = None):
    # print(x, y, cnt)
    if y == 1:
        if(path_tag == 2):
            return 0
        path_tag = 1
    if cnt < 1:
        return 2 - (path_tag != 0)
    if (args_pool is not None) and (deepth > 7):
        args_pool.append(args_zip(x, y, cnt, n, copy.deepcopy(visited), deepth, path_tag))
        return 0
    
    visited[x][y] = True
    ans = 0
    for dire in directions:
        x2 = x + dire[0]
        y2 = y + dire[1]
        if (x2 <= n+1) and (y2 <= n+1) and (1 <= y2) and (not visited[x2][y2]):
            if (1 <= x2):
                ans += walk(x2, y2, cnt-1, n, visited, deepth+1, copy.deepcopy(path_tag), args_pool)
            elif (0 == x2) and (path_tag != 1):
                ans += walk(x2, y2, cnt-1, n, visited, deepth+1, 2, args_pool)

    visited[x][y] = False
    return ans

def solve(n):
    if n == 1:
        return 1
    visited = [[False for i in range(n+2)] for i in range(n+2)]
    visited[1][1] = True
    visited[0][2] = True
    visited[1][2] = True
    with ProcessPoolExecutor(max_workers = cpu_count()) as executor:
        args_pool = []
        ans = walk(2, 2, n - 2, n, visited, 2, 0, (args_pool if n > 10 else None))
        print(f"len(args_pool): {len(args_pool)}")
        tasks_list = []
        for args in args_pool:
            t = executor.submit(walk_ziped_args, args)
            tasks_list.append(t)
        # tasks_list = executor.map(walk_ziped_args, args_pool)
        for th in as_completed(tasks_list):
            ans += th.result()
    return ans

def main():
    n = int(input())
    # n = 22
    ans = solve(n)
    print(n, ans)
    
if __name__ == "__main__":
    main()

'''
1 1
2 2
3 5
4 12
5 30
6 73
7 183
8 456
9 1151
10 2900
11 7361
12 18684
13 47652
14 121584
15 311259
16 797311
17 2047384
18 5260692
19 13542718
20 34884239
21 89991344
22 232282110
23 600281932
24 1552096361
25 4017128206
'''