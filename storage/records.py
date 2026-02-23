"""
数据存储模块
负责保存和读取游戏记录
"""
import json
import os
from datetime import datetime
from typing import Optional, Dict, List


class RecordManager:
    """记录管理器"""
    
    def __init__(self, storage_file: str = 'storage/records.json'):
        self.storage_file = storage_file
        self.records = self._load_records()
    
    def _load_records(self) -> dict:
        """加载记录"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载记录失败: {e}")
                return self._create_empty_records()
        else:
            return self._create_empty_records()
    
    def _create_empty_records(self) -> dict:
        """创建空记录"""
        return {
            'best_scores': {
                'slow': [],
                'normal': [],
                'fast': []
            },
            'total_games': 0,
            'total_questions': 0,
            'total_correct': 0,
            'total_wrong': 0,
            'history': []
        }
    
    def save_game_result(self, stats: dict, speed_mode: str):
        """
        保存游戏结果
        :param stats: 游戏统计数据
        :param speed_mode: 速度模式
        """
        # 更新总计
        self.records['total_games'] += 1
        self.records['total_questions'] += stats.get('total_questions', 0)
        self.records['total_correct'] += stats.get('correct_count', 0)
        self.records['total_wrong'] += stats.get('wrong_count', 0)
        
        # 创建游戏记录
        game_record = {
            'timestamp': datetime.now().isoformat(),
            'speed_mode': speed_mode,
            'score': stats.get('score', 0),
            'correct_count': stats.get('correct_count', 0),
            'wrong_count': stats.get('wrong_count', 0),
            'total_questions': stats.get('total_questions', 0),
            'accuracy': stats.get('accuracy', 0),
            'elapsed_time': stats.get('elapsed_time', 0),
            'max_combo': stats.get('max_combo', 0)
        }
        
        # 添加到历史记录（保留最近100条）
        self.records['history'].append(game_record)
        if len(self.records['history']) > 100:
            self.records['history'] = self.records['history'][-100:]
        
        # 更新最高分（每个速度模式保留前10名）
        if speed_mode in self.records['best_scores']:
            self.records['best_scores'][speed_mode].append(game_record)
            # 按分数排序
            self.records['best_scores'][speed_mode].sort(
                key=lambda x: x['score'], 
                reverse=True
            )
            # 只保留前10名
            self.records['best_scores'][speed_mode] = \
                self.records['best_scores'][speed_mode][:10]
        
        # 保存到文件
        self._save_to_file()
    
    def _save_to_file(self):
        """保存到文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
            
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存记录失败: {e}")
    
    def get_best_score(self, speed_mode: str) -> Optional[int]:
        """获取某个速度模式的最高分"""
        scores = self.records['best_scores'].get(speed_mode, [])
        if scores:
            return scores[0]['score']
        return None
    
    def get_best_records(self, speed_mode: str, limit: int = 5) -> List[dict]:
        """获取某个速度模式的最佳记录"""
        return self.records['best_scores'].get(speed_mode, [])[:limit]
    
    def get_overall_stats(self) -> dict:
        """获取总体统计"""
        total_questions = self.records['total_questions']
        total_correct = self.records['total_correct']
        
        overall_accuracy = 0
        if total_questions > 0:
            overall_accuracy = (total_correct / total_questions) * 100
        
        return {
            'total_games': self.records['total_games'],
            'total_questions': total_questions,
            'total_correct': total_correct,
            'total_wrong': self.records['total_wrong'],
            'overall_accuracy': overall_accuracy
        }
    
    def get_recent_games(self, limit: int = 10) -> List[dict]:
        """获取最近的游戏记录"""
        return self.records['history'][-limit:][::-1]  # 倒序返回
