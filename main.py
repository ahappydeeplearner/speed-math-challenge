"""
少儿速算闯关程序 - 主入口
Speed Math Challenge for Kids
"""
import pygame
import sys
from ui.main_menu import MainMenu
from ui.game_view import GameView
from storage.records import RecordManager


class SpeedMathGame:
    """游戏主类"""
    
    def __init__(self):
        # 初始化 Pygame
        pygame.init()
        
        # 设置窗口
        self.width = 1000
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('速算闯关 - Speed Math Challenge')
        
        # 时钟
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # 状态
        self.state = 'menu'  # 'menu', 'game', 'result'
        self.main_menu = MainMenu(self.screen)
        self.game_view = None
        
        # 游戏设置
        self.game_settings = None
        
        # 记录管理器
        self.record_manager = RecordManager()
    
    def run(self):
        """主循环"""
        running = True
        
        while running:
            dt = self.clock.tick(self.fps) / 1000.0  # 转换为秒
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self._handle_event(event)
            
            # 更新
            self._update(dt)
            
            # 绘制
            self._draw()
            
            # 刷新显示
            pygame.display.flip()
        
        # 退出
        pygame.quit()
        sys.exit()
    
    def _handle_event(self, event: pygame.event.Event):
        """处理事件"""
        if self.state == 'menu':
            action = self.main_menu.handle_event(event)
            if action == 'start':
                self._start_game()
            elif action == 'settings':
                # TODO: 打开设置界面
                pass
        
        elif self.state == 'game':
            action = self.game_view.handle_event(event)
            if action == 'menu':
                self._return_to_menu()
    
    def _update(self, dt: float):
        """更新游戏状态"""
        if self.state == 'game' and self.game_view:
            self.game_view.update(dt)
            
            # 检查游戏是否结束
            if self.game_view.is_game_over():
                # 保存游戏记录
                stats = self.game_view.get_stats()
                speed_mode = self.game_settings.get('speed_mode', 'normal')
                self.record_manager.save_game_result(stats, speed_mode)
    
    def _draw(self):
        """绘制画面"""
        if self.state == 'menu':
            self.main_menu.draw()
        elif self.state == 'game' and self.game_view:
            self.game_view.draw()
    
    def _start_game(self):
        """开始游戏"""
        # 获取游戏设置
        self.game_settings = self.main_menu.get_game_settings()
        
        # 创建游戏视图
        self.game_view = GameView(self.screen, self.game_settings)
        
        # 切换状态
        self.state = 'game'
    
    def _return_to_menu(self):
        """返回主菜单"""
        self.state = 'menu'
        self.game_view = None


def main():
    """程序入口"""
    game = SpeedMathGame()
    game.run()


if __name__ == '__main__':
    main()
