"""
游戏规则引擎
集中管理游戏的可调参数和规则
"""


class GameRules:
    """游戏规则配置"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        # 堆叠设置
        'max_stack': 10,
        
        # 速度设置
        'spawn_interval_base': 3.0,  # 基础生成间隔（秒）
        'spawn_interval_min': 0.8,   # 最小生成间隔（秒）
        
        # 答对奖励
        'correct_reward': 1,          # 答对消除数量
        
        # 答错惩罚
        'wrong_penalty': 0.2,         # 答错减少间隔（秒）
        'wrong_spawn_extra': True,    # 答错是否额外生成障碍物
        
        # 速度档位倍率
        'speed_multipliers': {
            'slow': 1.5,
            'normal': 1.0,
            'fast': 0.6
        },
        
        # 运算类型
        'enabled_operations': ['add', 'sub', 'mul', 'div'],
        
        # 难度
        'difficulty': 'basic',  # 'basic' 或 'advanced'
        
        # 连击加分
        'combo_bonus_threshold': 3,   # 每N连击增加奖励
        'combo_bonus_points': 2,      # 连击奖励分数
        'max_combo_bonus': 5,         # 最大连击加成档位
    }
    
    @classmethod
    def get_default_settings(cls) -> dict:
        """获取默认设置"""
        return cls.DEFAULT_CONFIG.copy()
    
    @classmethod
    def create_settings(cls, **overrides) -> dict:
        """
        创建游戏设置
        :param overrides: 要覆盖的设置
        :return: 设置字典
        """
        settings = cls.DEFAULT_CONFIG.copy()
        settings.update(overrides)
        return settings
    
    @classmethod
    def validate_settings(cls, settings: dict) -> bool:
        """
        验证设置的有效性
        :param settings: 设置字典
        :return: 是否有效
        """
        try:
            # 检查必要的键
            if settings.get('max_stack', 0) <= 0:
                return False
            
            if settings.get('spawn_interval_min', 0) <= 0:
                return False
            
            if settings.get('spawn_interval_base', 0) < settings.get('spawn_interval_min', 0):
                return False
            
            # 检查运算类型
            ops = settings.get('enabled_operations', [])
            if not ops or not all(op in ['add', 'sub', 'mul', 'div'] for op in ops):
                return False
            
            # 检查速度模式
            speed = settings.get('speed_mode', 'normal')
            if speed not in ['slow', 'normal', 'fast']:
                return False
            
            return True
        except Exception:
            return False
