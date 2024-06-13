# pip install cx_Freeze
# pip install streamlit

import streamlit as st
import json
from streamlit_option_menu import option_menu
import datetime

import streamlit.web.cli as stcli
import os, sys

# Import the other libraries you need here


def resolve_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path


if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("app.py"),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())