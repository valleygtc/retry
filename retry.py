from time import sleep
from functools import wraps
import logging


_logger = logging.getLogger(__name__)


def retry_call(
    func,
    fargs=(),
    fkwargs={},
    exceptions=Exception,
    tries=-1,
    interval=0,
    multiplier=1,
    addend=0,
    max_interval=None,
    logger=_logger,
):
    """call func with retry power.

    Params:
        func [Function]
        fargs [tuple]: 作为*args传给func。
        fkwargs [dict]: 作为**kwargs传给func。
        exceptions [Exception] | [tuple[Exception]]
        tries [int]: 次数。如果是负数则一直retry直至成功。
        interval [int]: 间隔时间，单位：秒。
        multiplier [int]: 每次重试间隔增加倍数。
        addend [int]: 每次重试间隔增加时间，单位：秒。
        max_interval [int]: 最长间隔，单位：秒。
        logger [Logger]: 每次失败log一个warning消息。
    """
    while tries != 0:
        try:
            return func(*fargs, **fkwargs)
        except exceptions as e:
            tries -= 1
            if tries == 0:
                raise
            logger.warning('encounter an error: %s, retry in %s seconds.', e, interval)

        sleep(interval)
        interval *= multiplier
        interval += addend
        if max_interval is not None:
            interval = min(interval, max_interval)


def retry(
    exceptions=Exception,
    tries=-1,
    interval=0,
    multiplier=1,
    addend=0,
    max_interval=None,
    logger=_logger,
):
    """retry power decorator.

    Params:
        exceptions [Exception] | [tuple[Exception]]
        tries [int]: 次数。如果是负数则一直retry直至成功。
        interval [int]: 间隔时间，单位：秒。
        multiplier [int]: 每次重试间隔增加倍数。
        addend [int]: 每次重试间隔增加时间，单位：秒。
        max_interval [int]: 最长间隔，单位：秒。
        logger [Logger]: 每次失败log一个warning消息。
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return retry_call(
                func,
                args,
                kwargs,
                exceptions,
                tries,
                interval,
                multiplier,
                addend,
                max_interval,
                logger,
            )
        return wrapper
    return decorator
