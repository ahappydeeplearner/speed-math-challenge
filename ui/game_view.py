"""
游戏主界面
显示题目、输入框、障碍物堆叠等
"""
import pygame
from typing import Optional
from core.game_state import GameState
from core.question_generator import QuestionGenerator, Question
from ui.fonts import get_font


class Obstacle:
    """敌人类（小怪物）"""
    
    def __init__(self, x: int, y: int, size: int = 28, index: int = 0):
        self.x = x
        self.y = y
        self.size = size
        self.target_x = x
        self.target_y = y
        self.alpha = 255
        self.scale = 1.0
        self.color = self._random_color()
        
        # 动画参数
        import random
        self.float_offset = 0  # 悬浮偏移
        self.float_speed = 1.5 + random.random() * 1.0  # 悬浮速度（随机）
        self.float_amplitude = 8 + random.random() * 4  # 悬浮幅度（随机）
        self.wobble_offset = 0  # 摆动偏移
        self.wobble_speed = 2.0 + random.random() * 1.0  # 摆动速度
        self.time = random.random() * 6.28  # 随机起始时间（避免所有怪兽同步）
        self.index = index  # 怪兽索引（用于交错排列）
    
    def _random_color(self) -> tuple:
        """随机颜色"""
        import random
        colors = [
            (255, 100, 100),  # 红色怪物
            (255, 150, 50),   # 橙色怪物
            (200, 100, 200),  # 紫色怪物
            (100, 150, 255),  # 蓝色怪物
        ]
        return random.choice(colors)
    
    def update(self, dt: float):
        """更新位置和动画"""
        import math
        
        # 向目标位置移动
        if abs(self.target_y - self.y) > 1:
            self.y += (self.target_y - self.y) * 5 * dt
        if abs(self.target_x - self.x) > 1:
            self.x += (self.target_x - self.x) * 5 * dt
        
        # 更新动画时间
        self.time += dt
        
        # 悬浮动画（上下浮动）
        self.float_offset = math.sin(self.time * self.float_speed) * self.float_amplitude
        
        # 摆动动画（轻微左右摆动）
        self.wobble_offset = math.sin(self.time * self.wobble_speed) * 3
    
    def draw(self, screen: pygame.Surface):
        """绘制👾样式的外星怪兽"""
        size = int(self.size * self.scale)
        # 应用动画偏移
        center_x = int(self.x + self.wobble_offset)
        center_y = int(self.y + self.float_offset)
        
        # 创建带透明度的表面
        monster_surface = pygame.Surface((size * 2 + 20, size * 2 + 20), pygame.SRCALPHA)
        base_x = size + 10
        base_y = size + 10
        
        # 外星人身体（方形）
        body_rect = pygame.Rect(base_x - size, base_y - size, size * 2, size * 2)
        pygame.draw.rect(monster_surface, (*self.color, self.alpha), body_rect)
        
        # 触角（上方两个小方块）
        antenna_size = size // 3
        pygame.draw.rect(monster_surface, (*self.color, self.alpha), 
                        (base_x - size // 2 - antenna_size // 2, base_y - size - antenna_size, 
                         antenna_size, antenna_size))
        pygame.draw.rect(monster_surface, (*self.color, self.alpha), 
                        (base_x + size // 2 - antenna_size // 2, base_y - size - antenna_size, 
                         antenna_size, antenna_size))
        
        # 眼睛（方形）
        eye_size = size // 3
        left_eye_x = base_x - size // 2
        right_eye_x = base_x + size // 2 - eye_size
        eye_y = base_y - size // 3
        
        pygame.draw.rect(monster_surface, (255, 255, 255, self.alpha),
                        (left_eye_x, eye_y, eye_size, eye_size))
        pygame.draw.rect(monster_surface, (255, 255, 255, self.alpha),
                        (right_eye_x, eye_y, eye_size, eye_size))
        
        # 眼珠（小方块）
        pupil_size = eye_size // 2
        pygame.draw.rect(monster_surface, (0, 0, 0, self.alpha),
                        (left_eye_x + eye_size // 4, eye_y + eye_size // 4, pupil_size, pupil_size))
        pygame.draw.rect(monster_surface, (0, 0, 0, self.alpha),
                        (right_eye_x + eye_size // 4, eye_y + eye_size // 4, pupil_size, pupil_size))
        
        # 嘴巴（锯齿状）
        mouth_y = base_y + size // 4
        tooth_width = size // 5
        for i in range(5):
            x = base_x - size + i * tooth_width * 2
            if i % 2 == 0:
                points = [
                    (x, mouth_y),
                    (x + tooth_width, mouth_y),
                    (x + tooth_width // 2, mouth_y + tooth_width)
                ]
                pygame.draw.polygon(monster_surface, (50, 50, 50, self.alpha), points)
        
        # 手臂（两侧小方块）
        arm_size = size // 4
        pygame.draw.rect(monster_surface, (*self.color, self.alpha),
                        (base_x - size - arm_size, base_y, arm_size, size // 2))
        pygame.draw.rect(monster_surface, (*self.color, self.alpha),
                        (base_x + size, base_y, arm_size, size // 2))
        
        # 绘制到屏幕
        rect = monster_surface.get_rect(center=(center_x, center_y))
        screen.blit(monster_surface, rect)


class GameView:
    """游戏主界面"""
    
    def __init__(self, screen: pygame.Surface, settings: dict):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # 游戏状态
        self.game_state = GameState(settings)
        self.question_generator = QuestionGenerator(
            enabled_ops=settings.get('enabled_operations', ['add']),
            difficulty=settings.get('difficulty', 'basic')
        )
        
        # 字体
        self.title_font = get_font(38, bold=True)
        self.question_font = get_font(68, bold=True)
        self.input_font = get_font(60)
        self.info_font = get_font(28)
        self.small_font = get_font(22)
        
        # 输入（右半区）
        self.user_input = ""
        right_center = self.width // 2 + self.width // 4
        self.input_rect = pygame.Rect(right_center - 180, 420, 360, 90)
        
        # 怪兽进攻（交错排列在左半区，避免重叠）
        self.obstacles = []
        self.obstacle_area_x = self.width // 4  # 左半区中心（与标题对齐）
        self.obstacle_start_y = 200  # 从这里开始往下排（往下移20px）
        self.obstacle_spacing_y = 56   # 垂直间距（确保10个能排下：200+9*56=704 < 740飞机位置）
        self.obstacle_spacing_x = 40   # 水平交错间距（怪兽变小，间距也减小）
        self.obstacle_label = "怪兽"
        
        # 飞机（左半区底部）
        self.plane_x = self.width // 4
        self.plane_y = self.height - 60  # 距离底部60px（从80改为60，往下移20px）
        self.plane_size = 50
        
        # 子弹系统
        self.bullets = []  # 存储飞行中的子弹
        
        # 提示信息
        self.feedback_text = ""
        self.feedback_color = (0, 255, 0)
        self.feedback_timer = 0
        
        # 动画
        self.removing_obstacles = []  # 正在消除的障碍物
        
        # 背景
        self.bg_color = (147, 112, 219)
        
        # 生成第一个题目
        self._generate_new_question()
        
        # 开始游戏
        self.game_state.start_game()
    
    def _generate_new_question(self):
        """生成新题目"""
        self.game_state.current_question = self.question_generator.generate()
        self.user_input = ""
    
    def update(self, dt: float):
        """更新游戏状态"""
        if self.game_state.is_game_over:
            return
        
        # 更新游戏状态
        events = self.game_state.update(dt)
        
        # 处理事件
        for event in events:
            if event['type'] == 'spawn_obstacle':
                self._spawn_obstacle()
            elif event['type'] == 'game_over':
                pass  # 游戏结束在 game_state 中已处理
        
        # 更新障碍物位置（交错排列，避免重叠）
        for i, obs in enumerate(self.obstacles):
            obs.target_y = self.obstacle_start_y + i * self.obstacle_spacing_y
            # 交错排列：奇数向左，偶数向右
            x_offset = self.obstacle_spacing_x if i % 2 == 0 else -self.obstacle_spacing_x
            obs.target_x = self.obstacle_area_x + x_offset
            obs.update(dt)
        
        # 更新正在消除的障碍物
        for obs in self.removing_obstacles[:]:
            obs.alpha -= 500 * dt
            obs.scale += 1.5 * dt
            if obs.alpha <= 0:
                self.removing_obstacles.remove(obs)
        
        # 更新子弹 - 垂直向上飞
        for bullet in self.bullets[:]:
            bullet['time'] += dt
            bullet['y'] -= bullet['speed'] * dt  # 垂直向上
            
            # 到达目标高度或超时，移除子弹
            if bullet['y'] <= bullet['target_y'] or bullet['time'] > 2:
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
        
        # 更新反馈计时
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
    
    def _spawn_obstacle(self):
        """生成新障碍物"""
        index = len(self.obstacles)
        y = self.obstacle_start_y + index * self.obstacle_spacing_y
        # 根据索引决定初始X位置（交错）
        x_offset = self.obstacle_spacing_x if index % 2 == 0 else -self.obstacle_spacing_x
        x = self.obstacle_area_x + x_offset
        obstacle = Obstacle(x, y, index=index)
        self.obstacles.append(obstacle)
    
    def _remove_obstacle(self):
        """移除障碍物 - 发射子弹"""
        if self.obstacles:
            obs = self.obstacles.pop()
            # 发射子弹特效
            self._fire_bullet(obs)
            self.removing_obstacles.append(obs)
    
    def _fire_bullet(self, target):
        """发射子弹击中怪兽 - 从飞机发射"""
        bullet = {
            'x': target.target_x,  # 和怪兽目标X坐标对齐（不包含摆动偏移）
            'y': self.plane_y - 20,  # 从飞机顶部发射
            'target_y': target.target_y,  # 目标Y坐标（不包含悬浮偏移）
            'time': 0,
            'speed': 600,  # 子弹速度
            'color': (255, 255, 0)  # 黄色子弹
        }
        self.bullets.append(bullet)
    
    def draw(self):
        """绘制游戏界面"""
        # 背景
        self.screen.fill(self.bg_color)
        
        # 顶部信息栏
        self._draw_info_bar()
        
        # 障碍物
        self._draw_obstacles()
        
        # 飞机（在左半区底部）
        self._draw_plane()
        
        # 子弹（在题目下方绘制）
        for bullet in self.bullets:
            self._draw_bullet(bullet)
        
        # 题目
        self._draw_question()
        
        # 输入框
        self._draw_input()
        
        # 反馈信息（右半区）
        if self.feedback_timer > 0:
            right_center = self.width // 2 + self.width // 4
            feedback_surface = self.info_font.render(self.feedback_text, True, self.feedback_color)
            feedback_rect = feedback_surface.get_rect(center=(right_center, 560))
            self.screen.blit(feedback_surface, feedback_rect)
        
        # 游戏结束提示
        if self.game_state.is_game_over:
            self._draw_game_over()
    
    def _draw_info_bar(self):
        """绘制信息栏"""
        # 背景
        info_rect = pygame.Rect(0, 0, self.width, 50)
        pygame.draw.rect(self.screen, (120, 90, 200), info_rect)
        
        # 分数（左）
        score_text = self.info_font.render(f'分数: {self.game_state.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (30, 12))
        
        # 时间（中）
        time_str = f'{int(self.game_state.elapsed_time)}秒'
        time_text = self.info_font.render(f'时间: {time_str}', True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(self.width // 2, 25))
        self.screen.blit(time_text, time_rect)
        
        # 连击或正确率（右）
        if self.game_state.combo > 0:
            combo_text = self.info_font.render(f'连击: {self.game_state.combo}', True, (255, 215, 0))
            combo_rect = combo_text.get_rect(right=self.width - 30, centery=25)
            self.screen.blit(combo_text, combo_rect)
        else:
            accuracy = self.game_state.get_accuracy()
            accuracy_text = self.info_font.render(f'正确率: {accuracy:.0f}%', True, (255, 255, 255))
            accuracy_rect = accuracy_text.get_rect(right=self.width - 30, centery=25)
            self.screen.blit(accuracy_text, accuracy_rect)
    
    def _draw_obstacles(self):
        """绘制怪兽区域"""
        # 绘制左半区分隔线
        divider_x = self.width // 2
        pygame.draw.line(self.screen, (150, 120, 200), 
                        (divider_x, 50), (divider_x, self.height), 3)
        
        # 计算状态
        progress = self.game_state.stack_count / self.game_state.max_stack
        if progress < 0.3:
            status = "安全"
            status_color = (100, 255, 100)
        elif progress < 0.6:
            status = "警戒"
            status_color = (255, 255, 100)
        elif progress < 0.8:
            status = "危险"
            status_color = (255, 150, 0)
        else:
            status = "紧急"
            status_color = (255, 50, 50)
        
        # 左半区域信息（往上提）
        info_y = 65  # 从80改为65，往上提
        left_x = self.width // 4
        
        # 标题 "👾 外星入侵"（左侧）
        title_text = self.title_font.render('👾 外星入侵', True, (255, 255, 255))
        
        # 数量和状态（竖着排列，右侧）
        count_text = self.info_font.render(f'{self.game_state.stack_count}/{self.game_state.max_stack}', 
                                          True, (255, 255, 255))
        status_text = self.info_font.render(status, True, status_color)
        
        # 计算布局：标题在左，数量状态在右（竖着）
        title_width = title_text.get_width()
        status_block_width = max(count_text.get_width(), status_text.get_width())
        total_width = title_width + 30 + status_block_width  # 30px间距
        
        # 起始X位置（居中整个组合）
        start_x = left_x - total_width // 2
        
        # 绘制标题（垂直居中于数量+状态的整体）
        title_height = title_text.get_height()
        status_total_height = count_text.get_height() + 8 + status_text.get_height()
        title_y_offset = (status_total_height - title_height) // 2
        
        self.screen.blit(title_text, (start_x, info_y + title_y_offset))
        
        # 绘制数量（竖着，第一行）
        count_x = start_x + title_width + 30
        self.screen.blit(count_text, (count_x, info_y))
        
        # 绘制状态（竖着，第二行）
        status_x = count_x + (count_text.get_width() - status_text.get_width()) // 2  # 状态文本居中对齐数量
        self.screen.blit(status_text, (status_x, info_y + count_text.get_height() + 8))
        
        # 绘制怪兽（保持与上方信息居中对齐）
        for obs in self.obstacles:
            obs.draw(self.screen)
        
        # 绘制正在消除的怪兽
        for obs in self.removing_obstacles:
            obs.draw(self.screen)
    
    def _draw_question(self):
        """绘制题目（右半区）"""
        # 右半区标题
        right_center = self.width // 2 + self.width // 4
        title_text = self.title_font.render('答题区', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(right_center, 80))
        self.screen.blit(title_text, title_rect)
        
        # 题目
        if self.game_state.current_question:
            question_text = self.question_font.render(
                self.game_state.current_question.text, 
                True, (255, 255, 255)
            )
            question_rect = question_text.get_rect(center=(right_center, 280))
            
            # 背景
            bg_rect = question_rect.inflate(60, 30)
            pygame.draw.rect(self.screen, (120, 90, 200), bg_rect, border_radius=15)
            
            self.screen.blit(question_text, question_rect)
    
    def _draw_input(self):
        """绘制输入框"""
        # 输入框背景
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, border_radius=12)
        pygame.draw.rect(self.screen, (100, 100, 255), self.input_rect, 5, border_radius=12)
        
        # 输入文本
        input_surface = self.input_font.render(self.user_input or '?', True, (50, 50, 50))
        input_rect = input_surface.get_rect(center=self.input_rect.center)
        self.screen.blit(input_surface, input_rect)
        
        # 提示（更小）
        hint = self.small_font.render('回车提交', True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(self.input_rect.centerx, self.input_rect.bottom + 25))
        self.screen.blit(hint, hint_rect)
    
    def _draw_game_over(self):
        """绘制游戏结束界面"""
        # 半透明遮罩
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束文字
        game_over_text = self.title_font.render('游戏结束!', True, (255, 100, 100))
        game_over_rect = game_over_text.get_rect(center=(self.width // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)
        
        # 统计信息
        stats = self.game_state.get_stats()
        y = 280
        info_lines = [
            f'得分: {stats["score"]}',
            f'答对: {stats["correct_count"]} / {stats["total_questions"]}',
            f'正确率: {stats["accuracy"]:.1f}%',
            f'用时: {stats["elapsed_time"]:.1f}秒',
            f'最高连击: {stats["max_combo"]}',
        ]
        
        for line in info_lines:
            text = self.info_font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
            y += 50
        
        # 提示
        hint = self.info_font.render('按 ESC 返回主菜单', True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(self.width // 2, 600))
        self.screen.blit(hint, hint_rect)
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """
        处理事件
        :return: 'menu' 返回主菜单, None 继续游戏
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'menu'
            
            if not self.game_state.is_game_over:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self._submit_answer()
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                elif event.unicode.isdigit() or event.unicode == '-':
                    if len(self.user_input) < 10:  # 限制长度
                        self.user_input += event.unicode
        
        return None
    
    def _submit_answer(self):
        """提交答案"""
        if not self.user_input:
            return
        
        question = self.game_state.current_question
        if question.check_answer(self.user_input):
            # 答对
            result = self.game_state.on_correct_answer()
            self.feedback_text = f'正确! +{result["score_gained"]}分'
            if result['combo'] > 1:
                self.feedback_text += f' ({result["combo"]}连击!)'
            self.feedback_color = (0, 255, 0)
            self.feedback_timer = 1.0
            
            # 消除障碍物
            for _ in range(result['removed_count']):
                self._remove_obstacle()
        else:
            # 答错
            result = self.game_state.on_wrong_answer()
            self.feedback_text = f'错误! 答案是 {question.answer}'
            self.feedback_color = (255, 100, 100)
            self.feedback_timer = 1.5
        
        # 生成新题目
        self._generate_new_question()
    
    def _draw_plane(self):
        """绘制飞机（战斗机样式）"""
        x = int(self.plane_x)
        y = int(self.plane_y)
        size = self.plane_size
        
        # 创建飞机表面
        plane_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        center = size
        
        # 机身（三角形）
        body_points = [
            (center, center - size // 2),  # 顶部（机头）
            (center - size // 3, center + size // 2),  # 左下
            (center + size // 3, center + size // 2),  # 右下
        ]
        pygame.draw.polygon(plane_surface, (100, 200, 255), body_points)
        pygame.draw.polygon(plane_surface, (50, 150, 200), body_points, 3)
        
        # 机翼（左右两侧）
        # 左翼
        left_wing = [
            (center - size // 3, center),
            (center - size, center + size // 4),
            (center - size // 2, center + size // 3),
        ]
        pygame.draw.polygon(plane_surface, (80, 180, 230), left_wing)
        
        # 右翼
        right_wing = [
            (center + size // 3, center),
            (center + size, center + size // 4),
            (center + size // 2, center + size // 3),
        ]
        pygame.draw.polygon(plane_surface, (80, 180, 230), right_wing)
        
        # 驾驶舱（亮点）
        pygame.draw.circle(plane_surface, (200, 230, 255), (center, center), size // 6)
        
        # 喷射火焰（尾部）
        flame_points = [
            (center - size // 6, center + size // 2),
            (center, center + size // 2 + size // 4),
            (center + size // 6, center + size // 2),
        ]
        pygame.draw.polygon(plane_surface, (255, 150, 50), flame_points)
        pygame.draw.polygon(plane_surface, (255, 200, 100), flame_points, 2)
        
        # 绘制到屏幕
        rect = plane_surface.get_rect(center=(x, y))
        self.screen.blit(plane_surface, rect)
    
    def _draw_bullet(self, bullet):
        """绘制子弹特效"""
        x = int(bullet['x'])
        y = int(bullet['y'])
        
        # 子弹核心（黄色圆点）
        pygame.draw.circle(self.screen, bullet['color'], (x, y), 8)
        pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 5)
        
        # 子弹尾迹（渐变效果）
        for i in range(3):
            trail_y = y + i * 15
            trail_alpha = 255 - i * 80
            trail_size = 6 - i * 2
            if trail_size > 0:
                trail_surface = pygame.Surface((trail_size * 2, trail_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, (*bullet['color'], trail_alpha), 
                                 (trail_size, trail_size), trail_size)
                self.screen.blit(trail_surface, (x - trail_size, trail_y - trail_size))
    
    def is_game_over(self) -> bool:
        """是否游戏结束"""
        return self.game_state.is_game_over
    
    def get_stats(self) -> dict:
        """获取统计数据"""
        return self.game_state.get_stats()
