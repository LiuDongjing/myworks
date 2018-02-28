import numpy as np
import sys
import re
import argparse
import subprocess
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--truth', default='truth.exe')
    parser.add_argument('--comp', default='comp.exe')
    parser.add_argument('--timeout', type=int, default=1)
    args = parser.parse_args()
    prog_truth = subprocess.Popen(args.truth, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    prog_comp = subprocess.Popen(args.comp, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    lst = sys.stdin.readlines()
    data = ''.join(lst)
    truth = None
    comp = None
    try:
        truth, _ = prog_truth.communicate(input=data.encode(), timeout=args.timeout)
    except:
        print('%s 超时。'%args.truth)
        pass
    try:
        comp, _ = prog_comp.communicate(input=data.encode(), timeout=args.timeout)
        print('%s 超时。'%args.comp)
    except:
        pass
    if truth is None and comp is None:
        return
    exps = []
    for k in range(1, len(lst), 2):
        exps.append(lst[k])
    truth = truth.decode()
    truth = re.split(r'\n', truth)
    comp = comp.decode()
    comp = re.split(r'\n', comp)
    print('输入数据')
    print(data)
    print('结果比较')
    for d, t, c in zip(exps, truth, comp):
        if t != c:
            print()
            print('输入：%s'%d)
            print('%s: %s'%(args.truth, t))
            print('%s: %s'%(args.comp, c))

if __name__ == '__main__':
    main()