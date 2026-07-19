"""
report.py

Responsável pela geração dos relatórios da análise.
"""

import os
from datetime import datetime

class Report:
    def __init__(self):
        self.pasta = "reports"

        if not os.path.exists(self.pasta):
            os.makedirs(self.pasta)

    