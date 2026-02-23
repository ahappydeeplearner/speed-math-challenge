"""
题目生成器模块
负责生成加减乘除四则运算题目
"""
import random
from typing import Tuple, Optional


class Question:
    """题目对象"""
    def __init__(self, a: int, b: int, op: str, answer: int):
        self.a = a
        self.b = b
        self.op = op
        self.answer = answer
        self.text = self._generate_text()
    
    def _generate_text(self) -> str:
        """生成题目文本"""
        op_symbol = {
            'add': '+',
            'sub': '-',
            'mul': '×',
            'div': '÷'
        }
        return f"{self.a} {op_symbol[self.op]} {self.b} = ?"
    
    def check_answer(self, user_answer: str) -> bool:
        """检查答案是否正确"""
        try:
            return int(user_answer) == self.answer
        except (ValueError, TypeError):
            return False


class QuestionGenerator:
    """题目生成器"""
    
    def __init__(self, enabled_ops: list = None, difficulty: str = 'basic'):
        """
        初始化题目生成器
        :param enabled_ops: 启用的运算类型列表 ['add', 'sub', 'mul', 'div']
        :param difficulty: 难度级别 'basic' 或 'advanced'
        """
        self.enabled_ops = enabled_ops or ['add', 'sub', 'mul', 'div']
        self.difficulty = difficulty
        
        # 数值范围配置
        self.config = {
            'basic': {
                'add': (0, 99, 100),  # (最小值, 最大值, 结果上限)
                'sub': (0, 99, 0),     # (最小值, 最大值, 结果下限-保证非负)
                'mul': (1, 9, None),   # 99乘法表
                'div': (1, 9, None)    # 确保整除
            },
            'advanced': {
                'add': (0, 999, 1000),
                'sub': (-50, 99, -50),
                'mul': (1, 12, None),
                'div': (1, 12, None)
            }
        }
    
    def generate(self) -> Question:
        """生成一个新题目"""
        op = random.choice(self.enabled_ops)
        
        if op == 'add':
            return self._generate_addition()
        elif op == 'sub':
            return self._generate_subtraction()
        elif op == 'mul':
            return self._generate_multiplication()
        elif op == 'div':
            return self._generate_division()
    
    def _generate_addition(self) -> Question:
        """生成加法题"""
        min_val, max_val, result_limit = self.config[self.difficulty]['add']
        
        # 确保结果不超过上限
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, min(max_val, result_limit - a))
        
        return Question(a, b, 'add', a + b)
    
    def _generate_subtraction(self) -> Question:
        """生成减法题"""
        min_val, max_val, result_limit = self.config[self.difficulty]['sub']
        
        # 确保结果非负（基础模式）或符合下限
        if self.difficulty == 'basic':
            # 被减数必须大于等于减数
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, a)
        else:
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
        
        return Question(a, b, 'sub', a - b)
    
    def _generate_multiplication(self) -> Question:
        """生成乘法题"""
        min_val, max_val, _ = self.config[self.difficulty]['mul']
        
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        
        return Question(a, b, 'mul', a * b)
    
    def _generate_division(self) -> Question:
        """生成除法题（确保整除）"""
        min_val, max_val, _ = self.config[self.difficulty]['div']
        
        # 先生成商和除数，再计算被除数
        quotient = random.randint(min_val, max_val)
        divisor = random.randint(min_val, max_val)
        dividend = quotient * divisor
        
        return Question(dividend, divisor, 'div', quotient)
    
    def set_enabled_ops(self, ops: list):
        """设置启用的运算类型"""
        self.enabled_ops = [op for op in ops if op in ['add', 'sub', 'mul', 'div']]
        if not self.enabled_ops:
            self.enabled_ops = ['add']  # 至少保留一个
    
    def set_difficulty(self, difficulty: str):
        """设置难度"""
        if difficulty in ['basic', 'advanced']:
            self.difficulty = difficulty
