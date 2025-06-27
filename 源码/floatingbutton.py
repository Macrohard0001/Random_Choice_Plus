# floatingbutton.py
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, pyqtProperty, QSize
from PyQt5.QtGui import QMouseEvent
import sys

class FloatingButton(QPushButton):
    def __init__(self, text, click_function, 
                 opacity=0.7, hover_opacity=0.9, 
                 button_color=(100, 100, 100), 
                 text_color=(255, 255, 255),
                 parent=None):
        super().__init__(text, parent)
        self.setMouseTracking(True)
        self.click_function = click_function
        self.normal_opacity = opacity
        self.hover_opacity = hover_opacity
        self.button_color = button_color
        self.text_color = text_color
        
        # 设置初始大小
        self.setMinimumSize(100, 40)
        self.adjustSize()
        
        # 设置按钮样式
        self.update_style()
        
        # 设置窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        # 设置初始位置
        screen_geo = QApplication.primaryScreen().availableGeometry()
        self.move(64, screen_geo.height() - self.height() - 64)
        
        # 动画设置
        self.press_animation = QPropertyAnimation(self, b"size")
        self.press_animation.setDuration(100)
        self.press_animation.setEasingCurve(QEasingCurve.OutQuad)
        
        self.hover_animation = QPropertyAnimation(self, b"opacity")
        self.hover_animation.setDuration(200)
        
        # 初始化拖动位置和状态
        self.drag_start_position = QPoint(0, 0)
        self.drag_button_position = QPoint(0, 0)
        self.is_dragging = False
        self.drag_threshold = 5  # 拖动阈值（像素）
        
        self.show()
    
    def update_style(self):
        """更新按钮样式"""
        r, g, b = self.button_color
        tr, tg, tb = self.text_color
        
        # 使用固定圆角半径
        border_radius = min(self.width(), self.height()) // 2
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba({r}, {g}, {b}, {int(self.normal_opacity * 255)});
                color: rgb({tr}, {tg}, {tb});
                border-radius: {border_radius}px;
                font-weight: bold;
                font-size: 12px;
                border: 1px solid rgba(255, 255, 255, 100);
                padding: 5px 15px;
            }}
            QPushButton:hover {{
                background-color: rgba({r+20}, {g+20}, {b+20}, {int(self.hover_opacity * 255)});
            }}
        """)
    
    def get_opacity(self):
        """获取当前透明度"""
        return self.windowOpacity()
    
    def set_opacity(self, value):
        """设置透明度"""
        self.setWindowOpacity(value)
    
    opacity = pyqtProperty(float, get_opacity, set_opacity)
    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件 - 开始拖动/点击动画"""
        if event.button() == Qt.LeftButton:
            # 记录拖动起始位置
            self.drag_start_position = event.globalPos()
            # 记录按钮当前位置
            self.drag_button_position = self.pos()
            self.is_dragging = False
            self.start_press_animation()
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件 - 拖动按钮"""
        if event.buttons() == Qt.LeftButton:
            # 检查是否超过拖动阈值
            if not self.is_dragging:
                delta = (event.globalPos() - self.drag_start_position).manhattanLength()
                if delta > self.drag_threshold:
                    self.is_dragging = True
            
            # 如果确定是拖动操作，则移动按钮
            if self.is_dragging:
                # 计算正确的移动偏移量
                offset = event.globalPos() - self.drag_start_position
                # 应用偏移量到按钮的原始位置
                new_pos = self.drag_button_position + offset
                self.move(new_pos)
                event.accept()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件 - 执行点击函数"""
        if event.button() == Qt.LeftButton:
            # 只有当不是拖动操作时才执行点击函数
            if not self.is_dragging:
                self.click_function()
            
            # 重置拖动状态
            self.is_dragging = False
            self.end_press_animation()
            event.accept()
    
    def enterEvent(self, event):
        """鼠标进入事件 - 悬停动画"""
        self.start_hover_animation(self.hover_opacity)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """鼠标离开事件 - 恢复动画"""
        self.start_hover_animation(self.normal_opacity)
        super().leaveEvent(event)
    
    def start_hover_animation(self, target_opacity):
        """启动悬停透明度动画"""
        self.hover_animation.stop()
        self.hover_animation.setStartValue(self.windowOpacity())
        self.hover_animation.setEndValue(target_opacity)
        self.hover_animation.start()
    
    def start_press_animation(self):
        """启动按下动画（缩小效果）"""
        self.press_animation.stop()
        self.press_animation.setStartValue(self.size())
        self.press_animation.setEndValue(QSize(int(self.width() * 0.9), int(self.height() * 0.9)))
        self.press_animation.start()
    
    def end_press_animation(self):
        """结束按下动画（恢复大小）"""
        self.press_animation.stop()
        # 直接设置回原始大小
        self.resize(self.sizeHint())
    
    def sizeHint(self):
        """设置按钮大小"""
        hint = super().sizeHint()
        return QSize(max(100, hint.width() + 30), max(40, hint.height() + 10))
    
    def resizeEvent(self, event):
        """当按钮大小改变时更新样式"""
        super().resizeEvent(event)
        self.update_style()

def show_floating_button():
    """显示悬浮按钮的函数"""
    global app, button
    
    # 如果应用实例不存在，则创建
    if 'app' not in globals() or app is None:
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
    
    # 创建悬浮按钮
    button = FloatingButton(
        text="想点名就点我~",
        click_function=handle_button_click,
        opacity=0.7,
        hover_opacity=0.9,
        button_color=(70, 130, 180),  # 钢蓝色
        text_color=(255, 255, 255)    # 白色
    )
    
    # 启动事件循环
    app.exec_()

def handle_button_click():
    """处理按钮点击事件"""
    print("悬浮按钮被点击了!")
    # 设置全局变量通知主程序
    globals()['load'] = 1
    # 关闭悬浮按钮
    button.close()
    # 退出Qt事件循环
    app.quit()