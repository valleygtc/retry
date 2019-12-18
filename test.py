import unittest
from unittest.mock import Mock, patch, call

from retry import retry, retry_call


class TestRetryCall(unittest.TestCase):
    def test_default_inf(self):
        m_func = Mock()
        m_func.side_effect = (Exception(), Exception(), 10)
        self.assertEqual(
            retry_call(m_func),
            10,
        )

    def test_specific_exceptions(self):
        m_func1 = Mock()
        m_func1.side_effect = SyntaxError()
        with self.assertRaises(SyntaxError):
            retry_call(m_func1, exceptions=(ValueError, TimeoutError))
        
        m_func2 = Mock()
        m_func2.side_effect = (ValueError(), TimeoutError(), 10)
        self.assertEqual(
            retry_call(m_func2, exceptions=(ValueError, TimeoutError)),
            10,
        )
    
    def test_tries(self):
        m_func = Mock()
        m_func.side_effect = TimeoutError()
        with self.assertRaises(TimeoutError):
            retry_call(m_func, tries=3)
        self.assertEqual(
            m_func.call_count,
            3,
        )
    
    def test_interval(self):
        m_func = Mock()
        m_func.side_effect = (TimeoutError(), TimeoutError(), 10)
        with patch('retry.sleep') as m_sleep:
            self.assertEqual(
                retry_call(m_func, exceptions=TimeoutError, tries=3, interval=1),
                10,
            )
            self.assertEqual(
                m_sleep.call_args_list,
                [call(1), call(1)],
            )
    
    def test_multiplier(self):
        m_func = Mock()
        m_func.side_effect = (TimeoutError(), TimeoutError(), TimeoutError(), 10)
        with patch('retry.sleep') as m_sleep:
            self.assertEqual(
                retry_call(m_func, exceptions=TimeoutError, tries=4, interval=1, multiplier=2),
                10,
            )
            self.assertEqual(
                m_sleep.call_args_list,
                [call(1), call(2), call(4)],
            )
    
    def test_addend(self):
        m_func = Mock()
        m_func.side_effect = (TimeoutError(), TimeoutError(), TimeoutError(), 10)
        with patch('retry.sleep') as m_sleep:
            self.assertEqual(
                retry_call(m_func, exceptions=TimeoutError, tries=4, interval=1, addend=1),
                10,
            )
            self.assertEqual(
                m_sleep.call_args_list,
                [call(1), call(2), call(3)],
            )
    
    def test_max_interval(self):
        m_func = Mock()
        m_func.side_effect = (TimeoutError(), TimeoutError(), TimeoutError(), TimeoutError(), 10)
        with patch('retry.sleep') as m_sleep:
            self.assertEqual(
                retry_call(m_func, exceptions=TimeoutError, interval=1, addend=1, max_interval=3),
                10,
            )
            self.assertEqual(
                m_sleep.call_args_list,
                [call(1), call(2), call(3), call(3)],
            )


class TestDecorator(unittest.TestCase):
    def test_default_inf(self):
        hit = [0]
        target = 10

        @retry()
        def func():
            hit[0] += 1
            if hit[0] == 10:
                return hit[0]
            else:
                raise Exception()

        self.assertEqual(func(), target)

    def test_args(self):
        m_func = Mock()
        @retry()
        def func(a, b, c=1):
            m_func(a, b, c=c)

        func(1, 2, c=3)
        m_func.assert_called_with(1, 2, c=3)
