#!/usr/bin/env python
# -*- coding: utf-8 -*-

from AppKit import NSWorkspace,NSApplicationActivateIgnoringOtherApps 
import sys
import pyautogui
import subprocess
from sexpdata import loads, dumps

def get_actived_app():    
    active_app_name = NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()
    print(active_app_name)

def switch_to(app_name):    
    Apps = NSWorkspace.sharedWorkspace().runningApplications()
    for app in Apps:
        if app.localizedName() == app_name:
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
            break

def list_all_running_apps():
    Apps = NSWorkspace.sharedWorkspace().runningApplications()
    print(dumps([app.localizedName() for app in Apps]))

def kill_app(app_name):
    Apps = NSWorkspace.sharedWorkspace().runningApplications()
    for app in Apps:
        if app.localizedName() == app_name:
            app.terminate()
            break

def paste_text():
    # pyautogui.keyDown('command') 
    # pyautogui.keyDown('v')
    # pyautogui.keyUp('v') 
    # pyautogui.keyUp('command')
    pyautogui.write('Hello world!') 

def main():
    arguments = sys.argv
    func_name = arguments[1]
    if (func_name == "get_actived_app"):
        get_actived_app()
    elif func_name == "switch_to":
        switch_to(arguments[2])
    elif func_name == "list_all_running_apps":
        list_all_running_apps()
    elif func_name == "kill_app":
        kill_app(arguments[2])
        
if __name__ == "__main__":
    main()
