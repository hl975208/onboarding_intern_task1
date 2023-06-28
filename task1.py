from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
import copy

directions = [(-1,0), (1,0), (0,1), (0,-1)]

# multi process config
multi_process_n_threshold = 12
multi_process_base_path_len = 7
multi_process_max_workers = cpu_count()

def dfs(x : int, y : int, cnt : int, n, visited, deepth, path_type, args_pool = None):
    # print(x, y, cnt)
    if y == 1:
        if(path_type == 2):
            # a path touch both line y=1 and x-axis is invaild
            return 0
        # touch line y=1, path_type change to type-1
        path_type = 1
    if cnt < 1:
        # only type-0 path should be count twice
        return 2 - (path_type != 0)
    
    # multi process, record arguments
    if (args_pool is not None) and (deepth > multi_process_base_path_len):
        args_pool.append((copy.deepcopy(x), 
                          copy.deepcopy(y), 
                          copy.deepcopy(cnt), 
                          copy.deepcopy(n), 
                          copy.deepcopy(visited), 
                          copy.deepcopy(deepth), 
                          copy.deepcopy(path_type)))
        return 0
    
    visited[x][y] = True
    ans = 0
    for dire in directions:
        # (x2, y2) next step position
        x2 = x + dire[0]
        y2 = y + dire[1]
        # ensure (x2, y2) still inside boundary and is not visited
        if (x2 <= n+1) and (y2 <= n+1) and (1 <= y2) and (not visited[x2][y2]): 
            if (1 <= x2):
                ans += dfs(x2, y2, cnt-1, n, visited, deepth+1, copy.deepcopy(path_type), args_pool)
            elif (0 == x2) and (path_type != 1):
                # touch x-axis, path_type change to type-2
                ans += dfs(x2, y2, cnt-1, n, visited, deepth+1, 2, args_pool)

    visited[x][y] = False
    return ans

def solve(n):
    if n == 1:
        return 1
    visited = [[False for i in range(n+2)] for i in range(n+2)]
    visited[1][1] = True
    visited[0][2] = True
    visited[1][2] = True
    with ProcessPoolExecutor(max_workers = multi_process_max_workers) as executor:
        args_pool = ([] if n > multi_process_n_threshold else None)
        # start at (2,2), look up the document for details
        ans = dfs(2, 2, n - 2, n, visited, 2, 0, args_pool)

        print(f"len(args_pool): {len(args_pool)}")
        tasks_list = []
        for args in args_pool:
            t = executor.submit(dfs, *args)
            tasks_list.append(t)
        for th in as_completed(tasks_list):
            ans += th.result()
    return ans

def main():
    n = int(input())
    # n = 20  # DEBUG
    ans = solve(n)
    print(n, ans)
    
if __name__ == "__main__":
    main()

cheat_ans = (\
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
'''.split())[1::2]