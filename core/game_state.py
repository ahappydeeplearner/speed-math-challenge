"""
游戏状态管理模块
负责管理游戏的各种状态：分数、时间、障碍物堆叠等
"""
import time
from typing import Optional
from core.question_generator import Question


class GameState:
    """游戏状态类"""
    
    def __init__(self, settings: dict):
        """
        初始化游戏状态
        :param settings: 游戏设置字典
        """
        # 基础状态
        self.score = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.total_questions = 0
        
        # 时间
        self.start_time = None
        self.elapsed_time = 0.0
        self.last_update_time = None
        
        # 障碍物堆叠
        self.stack_count = 0
        self.max_stack = settings.get('max_stack', 10)
        
        # 速度控制
        self.speed_mode = settings.get('speed_mode', 'normal')
        self.spawn_interval_base = settings.get('spawn_interval_base', 2.0)
        self.spawn_interval_min = settings.get('spawn_interval_min', 0.5)
        self.spawn_interval = self._calculate_spawn_interval()
        self.time_since_last_spawn = 0.0
        
        # 惩罚和奖励
        self.wrong_penalty = settings.get('wrong_penalty', 0.15)
        self.correct_reward = settings.get('correct_reward', 1)
        
        # 当前题目
        self.current_question: Optional[Question] = None
        
        # 游戏状态
        self.is_running = False
        self.is_game_over = False
        
        # 连击
        self.combo = 0
        self.max_combo = 0
    
    def _calculate_spawn_interval(self) -> float:
        """根据速度模式计算生成间隔"""
        multipliers = {
            'slow': 1.5,
            'normal': 1.0,
            'fast': 0.6
        }
        multiplier = multipliers.get(self.speed_mode, 1.0)
        return self.spawn_interval_base * multiplier
    
    def start_game(self):
        """开始游戏"""
        self.is_running = True
        self.is_game_over = False
        self.start_time = time.time()
        self.last_update_time = self.start_time
    
    def update(self, dt: float) -> list:
        """
        更新游戏状态
        :param dt: 时间增量（秒）
        :return: 事件列表
        """
        if not self.is_running or self.is_game_over:
            return []
        
        events = []
        
        # 更新经过时间
        self.elapsed_time += dt
        
        # 更新生成计时
        self.time_since_last_spawn += dt
        
        # 检查是否需要生成新障碍物
        if self.time_since_last_spawn >= self.spawn_interval:
            if self.stack_count < self.max_stack:
                events.append({'type': 'spawn_obstacle'})
                self.stack_count += 1
                self.time_since_last_spawn = 0.0
            else:
                # 堆满，游戏结束
                events.append({'type': 'game_over', 'reason': 'stack_full'})
                self.game_over()
        
        return events
    
    def on_correct_answer(self) -> dict:
        """
        答对时的状态更新
        :return: 结果字典
        """
        self.correct_count += 1
        self.total_questions += 1
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        
        # 消除障碍物
        removed = 0
        if self.stack_count > 0:
            self.stack_count -= self.correct_reward
            removed = self.correct_reward
            if self.stack_count < 0:
                self.stack_count = 0
        
        # 加分（连击加成）
        combo_bonus = min(self.combo // 3, 5)  # 每3连击+1分，最多+5
        score_gained = 10 + combo_bonus * 2
        self.score += score_gained
        
        return {
            'is_correct': True,
            'removed_count': removed,
            'score_gained': score_gained,
            'combo': self.combo
        }
    
    def on_wrong_answer(self) -> dict:
        """
        答错时的状态更新
        :return: 结果字典
        """
        self.wrong_count += 1
        self.total_questions += 1
        self.combo = 0  # 重置连击
        
        # 惩罚：缩短生成间隔（加快速度）
        old_interval = self.spawn_interval
        self.spawn_interval = max(
            self.spawn_interval_min,
            self.spawn_interval - self.wrong_penalty
        )
        
        # 或者直接增加障碍物（可选）
        added = 0
        if self.stack_count < self.max_stack:
            self.stack_count += 1
            added = 1
        
        return {
            'is_correct': False,
            'added_count': added,
            'interval_changed': old_interval != self.spawn_interval,
            'new_interval': self.spawn_interval
        }
    
    def game_over(self):
        """游戏结束"""
        self.is_running = False
        self.is_game_over = True
    
    def get_accuracy(self) -> float:
        """获取正确率"""
        if self.total_questions == 0:
            return 0.0
        return (self.correct_count / self.total_questions) * 100
    
    def get_stats(self) -> dict:
        """获取游戏统计数据"""
        return {
            'score': self.score,
            'correct_count': self.correct_count,
            'wrong_count': self.wrong_count,
            'total_questions': self.total_questions,
            'accuracy': self.get_accuracy(),
            'elapsed_time': self.elapsed_time,
            'max_combo': self.max_combo,
            'speed_mode': self.speed_mode
        }
    
    def set_speed_mode(self, mode: str):
        """设置速度模式"""
        if mode in ['slow', 'normal', 'fast']:
            self.speed_mode = mode
            self.spawn_interval = self._calculate_spawn_interval()
