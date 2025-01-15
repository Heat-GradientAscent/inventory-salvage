import os
import threading
import nbtlib
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from combos import Combo
import aiohttp
import asyncio
from logger import Logger
from textwrap import TextWrapper
from uuid import uuid4

class World:
    def __init__(self, root: tk.Tk, combo: Combo, logger: Logger, namemodifier, button: ttk.Button, *args, **kwargs):
        self.root = root
        self.combo = combo
        self.logger = logger
        self.namemodifier = namemodifier
        self.button = button
        self.path = None
        self.combo.bind('<<ComboboxSelected>>', lambda _: self.select_player())
        self.mode = 'Singleplayer'
        self.players = {}
        self.player = None
        self.usernames = {}
        self.id = kwargs.get('uuid', uuid4())
        self.advancements = None
        self.stats = None
        self.server_props = None
    
    def select_save(self):
        try:
            self.unselect()
            self.root.withdraw()
            self.path = askdirectory()
            assert self.path not in [None, ''], 'No world selected'
            savename = self.path.split('/')[-1]
            self.name_btn(savename)
        except Exception as e:
            self.logger.afterError(e)
        finally:
            self.root.wm_deiconify()
            if self.path in [None, '']: return
        
        try:
            self.set_mode()
            def has_dat_files(path):
                return any(os.scandir(path))
            assert has_dat_files(self.advancements) or has_dat_files(self.stats), 'World has no player data available.'
        except Exception as e:
            self.logger.afterError(e)
            self.unselect()
            return
        playerdata = os.path.join(self.path, 'playerdata')
        self.players = {f:nbtlib.load(os.path.join(playerdata, f)) for f in os.listdir(playerdata) if f.endswith('.dat')}
        self.get_usernames()
    
    def name_btn(self, savename):
        self.namemodifier(TextWrapper(12).fill(savename[:30] + ('...' if len(savename) > 30 else '')))
    
    def set_mode(self):
        self.advancements = os.path.join(self.path, 'advancements')
        self.stats = os.path.join(self.path, 'stats')
        self.server_props = os.path.join(self.path, 'server.properties')
        self.mode = 'Multiplayer' if os.path.exists(self.server_props) or len(os.listdir(self.advancements))//2 > 1 or len(os.listdir(self.stats))//2 > 1 else 'Singleplayer'

    def unselect(self):
        self.__init__(**self.__dict__)
        self.combo['completevalues'] = []
        self.combo.configure(state='disabled')
        self.combo.set('')
        self.name_btn('Select save')
    
    def fill_combo(self, usernames):
        self.combo['completevalues'] = ([username for _, username in usernames.items()])
        self.combo.configure(state='normal')
        if self.mode == 'Singleplayer':
            self.combo.set(self.combo['completevalues'][0])
            self.player_single()
    
    def select_player(self):
        if self.mode == 'Singleplayer':
            self.player_single()
        else:
            self.player_multi()
    
    def player_single(self):
        level = os.path.join(self.path, 'level.dat')
        self.player = nbtlib.load(level)
    
    def player_multi(self):
        selected = self.combo.get()
        if selected == '': self.logger.afterError('No players found.'); return
        valuetokey = {v:k for k,v in self.usernames.items()}
        uuid = valuetokey[selected]
        uuid = f'{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}.dat'
        self.player = self.players[uuid]
    
    def extract_prop(self, prop):
        if self.mode == 'Singleplayer':
            return self.player['Data']['Player'][prop]
        else:
            return self.player[prop]
    
    def replace_prop(self, prop, val):
        if self.mode == 'Singleplayer':
            self.player['Data']['Player'][prop] = val
        else:
            self.player[prop] = val
    
    def save(self):
        self.player.save()
    
    def get_usernames(self):
        uuids = [p.replace('-', '').replace('.dat', '') for p in self.players.keys()]
        async def get_username_from_uuid(session, uuid):
            url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return uuid, data.get("name")
                else:
                    return uuid, None
        
        async def fetch_usernames(uuids):
            self.logger.afterSuccess('Retreiving player usernames.')
            async with aiohttp.ClientSession() as session:
                tasks = [get_username_from_uuid(session, uuid) for uuid in uuids]
                results = await asyncio.gather(*tasks)
                self.usernames = {uuid: name for uuid, name in results if name}
                if len(self.usernames):
                    self.logger.afterSuccess('Found usernames.')
                    self.fill_combo(self.usernames)
                else:
                    self.logger.afterError('Found no usernames.')

        def run_thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(fetch_usernames(uuids))
            loop.close()
        
        threading.Thread(target=run_thread).start()
    

if __name__ == '__main__':
    w = World()
    w.select_save()

    print (w.path)