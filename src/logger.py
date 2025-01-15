import threading
from tkinter import StringVar
from dataclasses import dataclass

@dataclass
class Logger:
    successMsg: StringVar
    errorMsg: StringVar

    def afterSuccess(self, text):
        self.errorMsg.set('')
        self.successMsg.set(text)
        threading.Timer(function = lambda: self.successMsg.set(''), interval = 3.0).start()
    
    def afterError(self, text):
        self.errorMsg.set(text)
        self.successMsg.set('')
        threading.Timer(function = lambda: self.errorMsg.set(''), interval = 3.0).start()