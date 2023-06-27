from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import copy

directions = [(-1,0), (1,0), (0,1), (0,-1)]

def args_zip(x : int, y : int, cnt : int, n, visited, deepth):
    return ((x), (y), (cnt), (n), copy.deepcopy(visited), (deepth))

def walk_ziped_args(args):
    return walk(args[0], args[1], args[2], args[3], args[4], args[5])

def walk(x : int, y : int, cnt : int, n, visited, deepth, args_pool = None):
    # print(x, y, cnt)
    if cnt < 1:
        return 1
    if (args_pool is not None) and deepth > 7 and (cnt > 3):
        args_pool.append(args_zip(x, y, cnt, n, copy.deepcopy(visited), deepth))
        return 0
    visited[x][y] = True
    ans = 0
    for dire in directions:
        x2 = x + dire[0]
        y2 = y + dire[1]
        if (x2 <= n) and (0 <= x2) and (y2 <= n) and (0 <= y2) and (not visited[x2][y2]):
            ans += walk(x2, y2, cnt-1, n, visited, deepth+1, args_pool)
    visited[x][y] = False
    return ans

def solve(n):
    visited = [[False for i in range(n+1)] for i in range(n+1)]
    visited[0][0] = True
    with ProcessPoolExecutor(max_workers=60) as executor:
        args_pool = []
        ans = walk(0, 1, n - 1, n, visited, 1, args_pool)
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
    # n = 24
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
26 10401997092
27 26957667445
28 69892976538
29 181340757857
30 470680630478
31 1222433229262
32 3175981845982
33 8255898715518
34 21467989716002
35 55850067698545
36 145339886752867
37 378379746027286
38 985346905294729
39 2566922857037007
40 6688754646791611
'''