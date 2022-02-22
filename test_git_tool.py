
from AnyQt.QtCore import *
from AnyQt.QtGui import *
from AnyQt.QtWidgets import *

import sys
import signal
import subprocess
from subprocess import Popen, PIPE
from git_tool import *
from gitwidget import *

def test_git_combobox():
    app = QApplication(sys.argv)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    w = QWidget()
    QVBoxLayout(w)

    git_widget = QGitWidget()
    w.layout().addWidget(git_widget)

    w_files = QWidget()
    w.layout().addWidget(w_files)
    box_files = QHBoxLayout(w_files)
    btn_refresh = QPushButton("Refresh")
    box_files.addWidget(btn_refresh)
    cmb_files = QComboBox()
    box_files.addWidget(cmb_files)
    update_cmb = lambda: set_git_combobox(
        cmb_files, git_widget.git_info, 
        "git-repo",
        extensions=[".txt"])
    btn_refresh.clicked.connect(update_cmb)

    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    test_git_combobox()