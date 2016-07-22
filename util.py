# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-22 12:30:24
# @Last Modified by:   edward
# @Last Modified time: 2016-07-22 13:51:05

def result(matches=[], default=None):
    def _decoractor(f):
        def fn(*args, **kwds):
            r = f(*args, **kwds)
            return  default if r in matches else r
        return fn
    return _decoractor

def set_default_result(instance, matches, methods):
    default_result = result(matches=matches, default=instance)
    for n in methods:
        raw_method = getattr(instance, n)
        setattr(instance, n, default_result(raw_method))

class Default:
    def set_default_result(self, *args, **kwds):
        return set_default_result(self, *args, **kwds)

def main():
    default_result = result(matches=[None], default=1)
    class A:
        def greet(self, name):
            print 'Hello,%s!' % name
    a = A()
    print a.greet('Edward')
    for n in (i for i in dir(a) if not i.startswith('_')):
        raw_mth = getattr(a, n)
        setattr(a, n, default_result(raw_mth))
    print a.greet('Edward')
    
if __name__ == '__main__':
    main()
