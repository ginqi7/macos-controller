#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json

import websocket_bridge_python
from AppKit import NSWorkspace,NSApplicationActivateIgnoringOtherApps 
import sys
import pynput
from sexpdata import loads, dumps
from PyObjCTools.AppHelper import callAfter

async def get_actived_app():    
    active_app_name = NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()
    await run_and_log(f'(setq macc--last-actived-app "{active_app_name}")')
import subprocess



async def switch_to(app_name):    
    Apps = NSWorkspace.sharedWorkspace().runningApplications()
    for app in Apps:
        if app.localizedName() == app_name:
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
            break

async def list_all_running_apps():
    Apps = NSWorkspace.sharedWorkspace().runningApplications()
    print(dumps([app.localizedName() for app in Apps]))

def kill_app(app_name):
    Apps = NSWorkspace.sharedWorkspace().runningApplications()
    for app in Apps:
        if app.localizedName() == app_name:
            app.terminate()
            break

def mouse_position():
    mouse = pynput.mouse.Controller()
    print(dumps(mouse.position))

async def paste():
    keyboard = pynput.keyboard.Controller()

    with keyboard.pressed(pynput.keyboard.Key.cmd):
        keyboard.press('v')
        keyboard.release('v')
    print("command + v")
        
async def command_tab():
    keyboard = pynput.keyboard.Controller()

    with keyboard.pressed(pynput.keyboard.Key.cmd):
        keyboard.press(pynput.keyboard.Key.tab)
        keyboard.release(pynput.keyboard.Key.tab)
    print("command + tab")
        
async def press(key):
    keyboard = pynput.keyboard.Controller()
    if (len(key) > 1):
        key = pynput.keyboard.Key[key]
    keyboard.press(key)
    keyboard.release(key)
    
# eval in emacs and log the command.
async def run_and_log(cmd):
    print(cmd, flush=True)
    await bridge.eval_in_emacs(cmd)

async def main():
    global bridge
    bridge = websocket_bridge_python.bridge_app_regist(on_message)
    await asyncio.gather(init(), bridge.start())

async def init():
    print("init")
    
async def get_emacs_var(var_name: str):
    "Get Emacs variable and format it."
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
            await get_actived_app()
        elif cmd == "list_all_running_apps":
            await list_all_running_apps()        
        elif cmd == "switch_to":
            app_name = info[1][1].strip()
            await switch_to(app_name)        
        elif cmd == "paste":
            await paste();
        elif cmd == "press":
            key = info[1][1].strip()
            await press(key);
        elif cmd == "command_tab":
            await command_tab();
        else:
            print(f"not fount handler for {cmd}", flush=True)
    except:
        import traceback
        print(traceback.format_exc())

callAfter(get_actived_app)
asyncio.run(main())

