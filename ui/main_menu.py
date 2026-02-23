"""
主菜单界面
包含运算类型选择、速度选择、开始游戏等功能
"""
import pygame
from typing import Optional, Tuple
from ui.fonts import get_font


class Button:
    """按钮类"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, bg_color: tuple, text_color: tuple = (255, 255, 255),
                 font_size: int = 36, icon: str = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.font_size = font_size
        self.icon = icon
        self.selected = False
        self.hovered = False
        
    def draw(self, screen: pygame.Surface, font: pygame.font.Font, 
             small_font: pygame.font.Font = None):
        """绘制按钮"""
        # 背景
        color = self.bg_color
        if self.selected:
            # 选中状态：添加阴影效果
            shadow_rect = self.rect.copy()
            shadow_rect.x += 4
            shadow_rect.y += 4
            pygame.draw.rect(screen, (80, 80, 80), shadow_rect, border_radius=15)
            pygame.draw.rect(screen, color, self.rect, border_radius=15)
            pygame.draw.rect(screen, (255, 255, 100), self.rect, 5, border_radius=15)
        elif self.hovered:
            # 悬停状态：稍微变亮 + 边框
            color = tuple(min(255, c + 20) for c in self.bg_color)
            pygame.draw.rect(screen, color, self.rect, border_radius=15)
            pygame.draw.rect(screen, (200, 200, 200), self.rect, 2, border_radius=15)
        else:
            pygame.draw.rect(screen, color, self.rect, border_radius=15)
        
        # 图标（如果有）
        if self.icon:
            icon_font = get_font(self.font_size + 20, bold=True)
            icon_surface = icon_font.render(self.icon, True, self.text_color)
            icon_rect = icon_surface.get_rect(center=(self.rect.centerx, self.rect.centery - 20))
            screen.blit(icon_surface, icon_rect)
            
            # 文字在下方
            text_surface = small_font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery + 30))
            screen.blit(text_surface, text_rect)
        else:
            # 只有文字
            text_surface = font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """处理事件，返回是否被点击"""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def toggle_select(self):
        """切换选中状态"""
        self.selected = not self.selected


class MainMenu:
    """主菜单界面"""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # 字体
        self.title_font = get_font(60, bold=True)
        self.button_font = get_font(32, bold=True)
        self.small_font = get_font(24)
        
        # 背景颜色（紫色渐变）
        self.bg_color = (147, 112, 219)  # 中紫色
        
        # 按钮尺寸
        button_width = 160
        button_height = 140
        small_button_width = 220
        small_button_height = 100
        
        # 计算居中位置
        content_width = button_width * 4 + 30 * 3
        start_x = (self.width - content_width) // 2
        
        # 运算类型按钮（4个）- 增加间隔
        y_ops = 250  # 从280改为250
        self.op_buttons = {
            'add': Button(start_x, y_ops, button_width, button_height, 
                         '加法', (100, 149, 237), icon='+'),
            'sub': Button(start_x + button_width + 30, y_ops, button_width, button_height,
                         '减法', (76, 187, 23), icon='−'),
            'mul': Button(start_x + (button_width + 30) * 2, y_ops, button_width, button_height,
                         '乘法', (255, 140, 0), icon='×'),
            'div': Button(start_x + (button_width + 30) * 3, y_ops, button_width, button_height,
                         '除法', (138, 43, 226), icon='÷')
        }
        
        # 默认全选
        for btn in self.op_buttons.values():
            btn.selected = True
        
        # 速度选择按钮（3个）- 增加间隔
        y_speed = 460  # 从480改为460
        speed_width = small_button_width
        speed_height = small_button_height
        speed_content_width = speed_width * 3 + 30 * 2
        speed_start_x = (self.width - speed_content_width) // 2
        
        self.speed_buttons = {
            'slow': Button(speed_start_x, y_speed, speed_width, speed_height,
                          '慢速', (144, 238, 144)),
            'normal': Button(speed_start_x + speed_width + 30, y_speed, speed_width, speed_height,
                            '中速', (255, 215, 0)),
            'fast': Button(speed_start_x + (speed_width + 30) * 2, y_speed, speed_width, speed_height,
                          '快速', (255, 99, 71))
        }
        
        # 默认选中中速
        self.speed_buttons['normal'].selected = True
        self.selected_speed = 'normal'
        
        # 开始游戏按钮 - 增加间隔
        start_button_width = 280
        start_button_height = 70
        start_x = (self.width - start_button_width) // 2
        self.start_button = Button(start_x, 650, start_button_width, start_button_height,
                                   '开始游戏', (138, 43, 226))  # 从640改为650
        
        # 设置按钮
        settings_button_width = 200
        settings_x = (self.width - settings_button_width) // 2
        self.settings_button = Button(settings_x, 730, settings_button_width, 60,
                                      '设置', (200, 200, 200), (50, 50, 50))
    
    def draw(self):
        """绘制主菜单"""
        # 背景
        self.screen.fill(self.bg_color)
        
        # 标题
        title_text = self.title_font.render('速算闯关', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.small_font.render('Speed Math Challenge', True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, 150))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # 选择运算类型标题 - 贴近按钮
        ops_title = self.button_font.render('选择运算类型', True, (255, 255, 255))
        ops_title_rect = ops_title.get_rect(center=(self.width // 2, 220))  # 贴近按钮，保持15px间距
        self.screen.blit(ops_title, ops_title_rect)
        
        # 运算类型按钮
        for btn in self.op_buttons.values():
            btn.draw(self.screen, self.button_font, self.small_font)
        
        # 速度选择标题 - 贴近按钮
        speed_title = self.button_font.render('速度选择', True, (255, 255, 255))
        speed_title_rect = speed_title.get_rect(center=(self.width // 2, 432))  # 贴近按钮，保持15px间距
        self.screen.blit(speed_title, speed_title_rect)
        
        # 速度按钮
        for btn in self.speed_buttons.values():
            btn.draw(self.screen, self.small_font)
        
        # 开始游戏按钮
        self.start_button.draw(self.screen, self.button_font)
        
        # 设置按钮 - 暂时禁用
        # self.settings_button.draw(self.screen, self.small_font)
        
        # 显示当前选择的提示
        self._draw_selection_hint()
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """
        处理事件
        :return: 'start' 开始游戏, 'settings' 打开设置, None 无操作
        """
        # 运算类型按钮
        for op_name, btn in self.op_buttons.items():
            if btn.handle_event(event):
                btn.toggle_select()
                # 确保至少有一个被选中
                if not any(b.selected for b in self.op_buttons.values()):
                    btn.selected = True
        
        # 速度按钮（单选）
        for speed_name, btn in self.speed_buttons.items():
            if btn.handle_event(event):
                # 取消其他速度按钮的选中状态
                for other_btn in self.speed_buttons.values():
                    other_btn.selected = False
                btn.selected = True
                self.selected_speed = speed_name
        
        # 开始按钮
        if self.start_button.handle_event(event):
            return 'start'
        
        # 设置按钮 - 暂时禁用
        # if self.settings_button.handle_event(event):
        #     return 'settings'
        
        # 鼠标移动效果
        for btn in list(self.op_buttons.values()) + list(self.speed_buttons.values()) + [self.start_button, self.settings_button]:
            btn.handle_event(event)
        
        return None
    
    def get_selected_operations(self) -> list:
        """获取选中的运算类型"""
        return [op for op, btn in self.op_buttons.items() if btn.selected]
    
    def get_selected_speed(self) -> str:
        """获取选中的速度"""
        return self.selected_speed
    
    def get_game_settings(self) -> dict:
        """获取游戏设置"""
        from core.rules import GameRules
        
        return GameRules.create_settings(
            enabled_operations=self.get_selected_operations(),
            speed_mode=self.get_selected_speed()
        )
    
    def _draw_selection_hint(self):
        """绘制选择提示"""
        # 运算类型提示
        selected_ops = self.get_selected_operations()
        ops_names = {
            'add': '加法',
            'sub': '减法', 
            'mul': '乘法',
            'div': '除法'
        }
        ops_text = '、'.join([ops_names[op] for op in selected_ops])
        
        # 速度提示
        speed_names = {
            'slow': '慢速',
            'normal': '中速',
            'fast': '快速'
        }
        speed_text = speed_names[self.selected_speed]
        
        # 绘制提示框 - 贴近开始游戏按钮
        hint_text = f"已选择: {ops_text}  |  速度: {speed_text}"
        hint_surface = self.small_font.render(hint_text, True, (255, 255, 255))
        hint_rect = hint_surface.get_rect(center=(self.width // 2, 620))  # 贴近开始游戏按钮（Y=650），保持约15px间距
        
        # 半透明背景
        bg_rect = hint_rect.inflate(40, 20)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((100, 80, 160, 180))
        self.screen.blit(bg_surface, bg_rect)
        
        self.screen.blit(hint_surface, hint_rect)
