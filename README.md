# 简介：
call function with auto-retry power: 调用一个函数，如果函数抛出异常则根据自定义规则进行重试。

借鉴：[invl/retry](https://github.com/invl/retry)

# 使用：
将retry.py文件copy-paste到自己的项目中即可。

# 用法示例：
```python
from retry import retry
```

```python
@retry()
def unstable_func():
    """Retry until succeed"""
    pass
```

```python
@retry(ZeroDivisionError, tries=3, interval=2)
def unstable_func():
    """Retry on ZeroDivisionError, raise error after 3 attempts, sleep 2 seconds between attempts."""
```

```python
@retry((ValueError, TypeError), interval=1, multuplier=2)
def unstable_func():
    '''Retry on ValueError or TypeError, sleep 1, 2, 4, 8, ... seconds between attempts.'''
```

```python
@retry((ValueError, TypeError), interval=1, multuplier=2, max_interval=4)
def unstable_func():
    '''Retry on ValueError or TypeError, sleep 1, 2, 4, 4, ... seconds between attempts.'''
```

```python
@retry(ValueError, interval=1, addend=1)
def unstable_func():
    '''Retry on ValueError, sleep 1, 2, 3, 4, ... seconds between attempts.'''
```

注：以上所有使用装饰器的方法均可以等价使用`retry_call`函数。例如：
```python
retry_call(unstable_func, exceptions=ZeroDivisionError, tries=3, interval=2)
```

# 开发：
- 单元测试：`python -m unittest test`
