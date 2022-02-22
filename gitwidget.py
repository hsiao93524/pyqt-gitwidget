
from AnyQt.QtCore import *
from AnyQt.QtGui import *
from AnyQt.QtWidgets import *
import signal
import logging

import os, sys

try:
    from git_tool import *
    import config as git_cfg
except ModuleNotFoundError as e:
    sys.path.append(os.path.join(os.path.dirname(__file__)))
    from git_tool import *
    import config as git_cfg

class LineWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._box_line = QHBoxLayout(self)

    def addWidget(self, w):
        self._box_line.addWidget(w)

    def set_zero_margin(self, no_margin):
        """
        param:
            no_margin [bool]
        """
        if no_margin:
            self.layout().setContentsMargins(0, 0, 0, 0)
        pass

class QGitWidget(QWidget):

    def __init__(self):
        super().__init__()

        self._git_info = GitInfo()

        # UI
        self._mainbox = QVBoxLayout(self)

        margin = QMargins(0, 0, 0, 0)

        lbl_id = QLabel("UserName")
        self._txt_id = QLineEdit(git_cfg.git_id)
        self._txt_id.setPlaceholderText("UserName")
        box_id = QWidget()
        QVBoxLayout(box_id)
        box_id.layout().addWidget(lbl_id)
        box_id.layout().addWidget(self._txt_id)
        box_id.layout().setContentsMargins(margin)

        lbl_pw = QLabel("Password")
        self._txt_pw = QLineEdit(git_cfg.git_pw)
        self._txt_pw.setPlaceholderText("Password")
        box_pw = QWidget()
        QVBoxLayout(box_pw)
        box_pw.layout().addWidget(lbl_pw)
        box_pw.layout().addWidget(self._txt_pw)
        box_pw.layout().setContentsMargins(margin)

        lbl_server = QLabel("Server IP")
        self._txt_server = QLineEdit(git_cfg.git_server)
        self._txt_server.setPlaceholderText("Server IP")
        box_server = QWidget()
        QVBoxLayout(box_server)
        box_server.layout().addWidget(lbl_server)
        box_server.layout().addWidget(self._txt_server)
        box_server.layout().setContentsMargins(margin)

        lbl_repo = QLabel("Repository")
        self._txt_repo = QLineEdit(git_cfg.repo_name)
        self._txt_repo.setPlaceholderText("Repository")
        box_repo = QWidget()
        QVBoxLayout(box_repo)
        box_repo.layout().addWidget(lbl_repo)
        box_repo.layout().addWidget(self._txt_repo)
        box_repo.layout().setContentsMargins(margin)

        self._btn_submit = QPushButton("Submit")
        self._btn_submit.clicked.connect(self.submit)

        self._lbl_msg = QLabel()

        self._add_line(self, [box_id, box_pw])
        self._add_line(self, [box_server, box_repo])
        self._add_line(self, [self._btn_submit])
        self._add_line(self, [self._lbl_msg])

    def set_error_msg(self, msg=""):
        self._lbl_msg.setText(msg)

    def set_gitinfo(self, info):
        msg = self._git_info.set_gitinfo(info)

        self._txt_id.setText(
            info.get("id", ""))
        self._txt_pw.setText(
            info.get("pw", ""))
        self._txt_server.setText(
            info.get("server", ""))
        self._txt_repo.setText(
            info.get("repo", ""))

    def submit(self):
        info = {
            "id": self._txt_id.text(),
            "pw": self._txt_pw.text(),
            "server": self._txt_server.text(),
            "repo": self._txt_repo.text(),
        }
        msg = self._git_info.set_gitinfo(info)
        self.set_error_msg(msg)
        logging.info(self._git_info)

    @property
    def git_info(self):
        return self._git_info    

    def _add_line(self, parent_widget, widgets=[]):
        if not isinstance(widgets, list):
            widgets = [widgets]
        linewidget = LineWidget()
        linewidget.set_zero_margin(True)
        parent_widget.layout().addWidget(linewidget)
        for w in widgets:
            linewidget.addWidget(w)