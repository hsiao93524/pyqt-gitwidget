
import git
import shutil
import os
import logging
from collections import defaultdict
import config as git_cfg

import shutil

file_dir = os.path.dirname(__file__)

logging_level = (git_cfg.logging_level 
    if hasattr(git_cfg, "logging_level") 
    else logging.ERROR)
logging.basicConfig(level=logging_level)

git_dict = defaultdict(lambda: {
    "dir": "", "git": ""})

git_url_format = "http://{git_id}:{git_pw}@{git_server}/{git_id}/{repo_name}.git"

def set_git_target(key, git, dirpath=""):
    if not dirpath:
        dirpath = os.path.join(
            file_dir, "scripts", key)
    git_dict.update(
        {key: dict(
            dir=dirpath, 
            git=git)})

class GitInfo(object):
    def __init__(self, git_id="", git_pw="", 
            git_server="", repo_name=""):

        self._git_id = git_id
        self._git_pw = git_pw
        self._git_server = git_server
        self._repo_name = repo_name

    def set_gitinfo(self, info={}):
        """
        retrun [str]: submit message
        """

        if not info:
            return ""

        git_id = info.get("id", "")
        git_pw = info.get("pw", "")
        git_server = info.get("server", "")
        repo_name = info.get("repo", "")

        self._git_id = git_id
        self._git_pw = git_pw
        self._git_server = git_server
        self._repo_name = repo_name
        
        return check_repo(self)

    @property
    def values(self):
        return dict(
            id=self.git_id,
            pw=self.git_pw,
            server=self.git_server,
            repo=self.repo_name)

    def __repr__(self):
        return " ".join([str(dict(
            UserName=self._git_id,
            Password=self._git_pw,
            Server=self._git_server,
            Repository=self._repo_name,
        )), "at", str(hex(id(self)))])

    @property
    def git_id(self):
        return self._git_id

    @property
    def git_pw(self):
        return self._git_pw

    @property
    def git_server(self):
        return self._git_server

    @property
    def repo_name(self):
        return self._repo_name

def get_git_url(git_info):

    git_url = git_url_format.format(
        git_id=git_info.git_id,
        git_pw=git_info.git_pw,
        git_server=git_info.git_server,
        repo_name=git_info.repo_name
    )
    logging.info(f"Git Url: {git_url}")
    return git_url

def check_repo(git_info):

    git_dict.clear()

    if not all(git_info.values.values()):
        return "Insufficient data."

    git_url = get_git_url(git_info)

    try:
        git.cmd.Git().ls_remote(git_url)
    except git.exc.GitCommandError as err:
        logging.info(err.stderr)
        if "Authentication failed" in err.stderr:
            err_msg = "Authentication failed."
            err_msg = "\n".join([
                "Authentication failed.",
                "Maybe have wrong UserName or ",
                "Password."])
        elif ("repository" in err.stderr 
                and "not found" in err.stderr):
            err_msg = "\n".join([
                "Repository not found.",
                "Maybe have wrong UserName or", 
                "Repository name."])
        elif "Failed to connect to" in err.stderr:
            err_msg = "\n".join([
                "Failed to connect.",
                "Maybe have wrong port."])
        elif "Could not resolve host" in err.stderr:
            err_msg = "\n".join([
                "Could not resolve host.",
                "Maybe have wrong hostname."])
        else:
            err_msg = err.stderr
        logging.info(err_msg)
        return err_msg

    return "Submit Success."

def set_scripts_path( 
        scripts_folder, git_info):

    git_url = get_git_url(git_info)
    repo_name = git_info.repo_name

    scripts_path = os.path.join(
        scripts_folder, repo_name)
    set_git_target(repo_name, 
        git_url, scripts_path)

def set_git_combobox(cmb=None, git_info=None,
        scripts_folder=".", extensions=[]):

    if git_info is None:
        return
    if cmb is not None:
        cmb.clear()

    msg = check_repo(git_info)
    set_scripts_path(scripts_folder, git_info)

    repo_name = git_info.repo_name

    try:
        logging.info("Git Loading...")
        
        logging.info("Clear folder: \"" + 
            git_dict[repo_name]["dir"] + "\"...")

        shutil.rmtree(git_dict[repo_name]["dir"], 
            ignore_errors=True)
        
        logging.info("Clone Repo.")
        logging.info("Clone from" +
            git_dict[repo_name]["git"])
        git.Repo.clone_from(
            git_dict[repo_name]["git"], 
            git_dict[repo_name]["dir"])

        logging.info("Clone to \"" + 
            git_dict[repo_name]["dir"] + "\".")

    except Exception as e:
        logging.info("Clone failed.")
        raise(e)
        return

    logging.info("Git Setting...")

    if extensions:
        scripts = []
        for f in os.listdir(git_dict[repo_name]["dir"]):
            if os.path.isfile(
                    os.path.join(
                    git_dict[repo_name]["dir"], f)):
                for extension in extensions:
                    if f.lower().endswith(extension.lower()):
                        scripts.append(f)
                        break
    else:
        scripts = [f for f in os.listdir(git_dict[repo_name]["dir"]) 
            if os.path.isfile(os.path.join(git_dict[repo_name]["dir"], f))]
    
    if cmb is not None:
        cmb.addItems(scripts)

    logging.info("Git Complete")