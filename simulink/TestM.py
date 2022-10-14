import time
from multiprocessing import Process
import random


def func_a():
    return "func_a"
def func_b():
    return "func_b"
def func_c():
    return "func_c"


if __name__ == '__main__':
    from multiprocessing import Pool

    pool = Pool(processes=3)    # 开进程进程池
    results = []
    results.append(pool.apply_async(func_a))
    results.append(pool.apply_async(func_b))
    results.append(pool.apply_async(func_c))
    pool.close()  # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
    pool.join()  # 等待进程池中的所有进程执行完毕
    print("Sub-process(es) done.")

    for res in results:
        print("我拿到值了",res.get())
