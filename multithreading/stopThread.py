'''
Author: Thoma411
Date: 2023-05-02 14:16:32
LastEditTime: 2023-05-02 14:33:54
Description: 
'''
import inspect as ist
import ctypes as ctp
import threading as th
import time as tm


def myMethod(num: int, step: int):
    while True:
        num += step
        print('num =', num)
        tm.sleep(1)


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctp.c_long(tid)
    if not ist.isclass(exctype):
        exctype = type(exctype)
    res = ctp.pythonapi.PyThreadState_SetAsyncExc(
        tid, ctp.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctp.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


if __name__ == '__main__':
    nu, st = map(int, input('num/step: ').split())
    t1 = th.Thread(target=myMethod, args=(nu, st))
    t1.start()
    inp = input('opt: ')
    if inp == 'q':
        stop_thread(t1)
        print('thread stopped.')
