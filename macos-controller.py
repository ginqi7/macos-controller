#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json

import pynput
import websocket_bridge_python
from AppKit import NSApplicationActivateIgnoringOtherApps, NSWorkspace
from sexpdata import dumps


def actived_app_name():
    """
    Get actived app name.
    Returns
    string: app name.
    """
    return NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']

def find_app_by_name (name):
    """
    Find running app by name.
    
    Parameters:
    name: string, the name of target app.
    
    Returns:
    matched app.
    """   
    for app in all_running_apps():
        if app.localizedName() == name:
            return app


async def update_emacs_string_variable(name, value):    
    """
    Update emacs string type variable by name and value.
    """
    await run_and_log(f'(setq {name} "{value}")')
    
def switch_to(app_name):    
    """
    Switch to the App by app_name.
    """
    find_app_by_name(app_name).activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
    
        
def all_running_apps ():
    """
    Get all running apps.
    
    Returns:
    A arrays store the information of all apps.
    
    """
    return NSWorkspace.sharedWorkspace().runningApplications()

def list_all_running_apps():
    """
    List all running apps.
    """
    Apps = all_running_apps()
    print(dumps([app.localizedName() for app in Apps]))

def kill_app(app_name):
    """
    Kill app by app_name.
    """    
    find_app_by_name(app_name).terminate()

def mouse_position():
    """
    Get current position of mouse.
    """
    mouse = pynput.mouse.Controller()
    print(dumps(mouse.position))
    
    
def press_with_modify_key(modified_key, key):
    """
    Press key bind modified_key and key.
    """
    keyboard = pynput.keyboard.Controller()

    with keyboard.pressed(modified_key):
        keyboard.press(key)
        keyboard.release(key)
    print(f'{modified_key} + {key}')

def paste():
    """
    Paste.
    """
    press_with_modify_key(pynput.keyboard.Key.cmd, "v")
    
        
def command_tab():
    """
    Press command + tab.
    """
    press_with_modify_key(pynput.keyboard.Key.cmd, pynput.keyboard.Key.tab)
        
def press(key):
    """
    Press the key.
    """
    keyboard = pynput.keyboard.Controller()
    if (len(key) > 1):
        key = pynput.keyboard.Key[key]
    keyboard.press(key)
    keyboard.release(key)
    

async def run_and_log(cmd):
    """
    eval in emacs and log the command.
    """
    print(cmd, flush=True)
    await bridge.eval_in_emacs(cmd)

async def main():
    global bridge
    bridge = websocket_bridge_python.bridge_app_regist(on_message)
    await asyncio.gather(init(), bridge.start())

async def init():
    print("init")
    
async def get_emacs_var(var_name: str):
    """
    Get Emacs variable and format it.
    """
    var_value = await bridge.get_emacs_var(var_name)
    if isinstance(var_value, str):
        var_value = var_value.strip('"')
    print(f'{var_name} : {var_value}')
    if var_value == 'null':
        return None
    return var_value

async def on_message(message):
    try:
        info = json.loads(message)
        cmd = info[1][0].strip()
        if cmd == "get_actived_app":
            await update_emacs_string_variable("macc--last-actived-app", actived_app_name())
        elif cmd == "list_all_running_apps":
            list_all_running_apps()        
        elif cmd == "switch_to":
            app_name = info[1][1].strip()
            switch_to(app_name)        
        elif cmd == "paste":
            paste();
        elif cmd == "press":
            key = info[1][1].strip()
            press(key);
        elif cmd == "command_tab":
            command_tab();
        else:
            print(f"not fount handler for {cmd}", flush=True)
    except:
        import traceback
        print(traceback.format_exc())

asyncio.run(main())

