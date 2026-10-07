MAIN_STYLE = """
QMainWindow {
    background-color: #1e1e2e;
    color: #cdd6f4;
}
QWidget {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
QLabel {
    font-size: 14px;
    color: #cdd6f4;
}
QLineEdit, QTextEdit {
    padding: 10px;
    border: 1px solid #45475a;
    border-radius: 8px;
    background-color: #313244;
    color: #cdd6f4;
    font-size: 14px;
}
QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #89b4fa;
}
QPushButton {
    padding: 10px 20px;
    background-color: #89b4fa;
    color: #11111b;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #b4befe;
}
QPushButton:pressed {
    background-color: #74c7ec;
}
QPushButton:disabled {
    background-color: #45475a;
    color: #a6adc8;
}
QTabWidget::pane {
    border: 1px solid #45475a;
    border-radius: 8px;
    background-color: #1e1e2e;
    margin-top: 10px;
}
QTabBar::tab {
    background: #313244;
    color: #cdd6f4;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: bold;
}
QTabBar::tab:selected {
    background: #89b4fa;
    color: #11111b;
}
QTabBar::tab:hover:!selected {
    background: #45475a;
}
"""
