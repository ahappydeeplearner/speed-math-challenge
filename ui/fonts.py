"""
字体管理模块 - 直接使用系统字体文件
"""
import pygame
import sys
import os


class FontManager:
    """字体管理器"""
    
    def __init__(self):
        pygame.font.init()
        self._font_path = self._find_system_font()
        print(f"使用字体文件: {self._font_path}")
    
    def _find_system_font(self):
        """查找系统中文字体文件"""
        if sys.platform == 'darwin':  # macOS
            # 尝试的字体路径
            font_paths = [
                '/System/Library/Fonts/PingFang.ttc',
                '/System/Library/Fonts/STHeiti Medium.ttc',
                '/System/Library/Fonts/STHeiti Light.ttc',
                '/Library/Fonts/Arial Unicode.ttf',
            ]
            
            for path in font_paths:
                if os.path.exists(path):
                    return path
        
        elif sys.platform == 'win32':  # Windows
            font_paths = [
                'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
                'C:/Windows/Fonts/simhei.ttf',  # 黑体
                'C:/Windows/Fonts/simsun.ttc',  # 宋体
            ]
            
            for path in font_paths:
                if os.path.exists(path):
                    return path
        
        else:  # Linux
            font_paths = [
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            ]
            
            for path in font_paths:
                if os.path.exists(path):
                    return path
        
        return None
    
    def get_font(self, size: int, bold: bool = False) -> pygame.font.Font:
        """获取指定大小的字体"""
        try:
            if self._font_path:
                return pygame.font.Font(self._font_path, size)
            else:
                # 降级：使用系统字体名称
                return pygame.font.SysFont('pingfang sc,arial unicode ms,helvetica', size, bold=bold)
        except Exception as e:
            print(f"字体加载失败: {e}")
            return pygame.font.Font(None, size)


# 全局字体管理器实例
_font_manager = None


def get_font_manager() -> FontManager:
    """获取全局字体管理器实例"""
    global _font_manager
    if _font_manager is None:
        _font_manager = FontManager()
    return _font_manager


def get_font(size: int, bold: bool = False) -> pygame.font.Font:
    """快捷函数：获取字体"""
    return get_font_manager().get_font(size, bold)
