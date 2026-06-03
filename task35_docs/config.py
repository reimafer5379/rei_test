import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent # __file__ - служебная переменная, содержащая путь к текущему файлу
                                     # .parent - атрибут, "поднимающийся" по дереву каталогов на 1 уровень вверх

ASSETS = [
    [
        str(PROJECT_ROOT / 'assets/line_on1.png'),
        str(PROJECT_ROOT / 'assets/line_on2.png'),
        str(PROJECT_ROOT / 'assets/ang_on1.png'),
        str(PROJECT_ROOT / 'assets/ang_on2.png'),
        str(PROJECT_ROOT / 'assets/ang_on3.png'),
        str(PROJECT_ROOT / 'assets/ang_on4.png'),
    ],
    [
        str(PROJECT_ROOT / 'assets/line_off1.png'),
        str(PROJECT_ROOT / 'assets/line_off2.png'),
        str(PROJECT_ROOT / 'assets/ang_off1.png'),
        str(PROJECT_ROOT / 'assets/ang_off2.png'),
        str(PROJECT_ROOT / 'assets/ang_off3.png'),
        str(PROJECT_ROOT / 'assets/ang_off4.png'),
    ],
    [str(PROJECT_ROOT / 'assets/background1.png')],
    [str(PROJECT_ROOT / 'assets/block.png')]
]

USE_CACHE = True


