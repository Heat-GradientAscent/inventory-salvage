from ttkwidgets.autocomplete import AutocompleteCombobox
from difflib import get_close_matches

class Combo(AutocompleteCombobox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<FocusOut>', lambda _: self.on_finish())
        self.bind('<Control-BackSpace>', lambda _: self.ctrl_back())
    
    def get_matches(self, text):
        return get_close_matches(text, self.cget('completevalues'), n=1, cutoff=0.4)
    
    def on_finish(self):
        text = self.get()
        matches = self.get_matches(text)
        if len(matches) == 0: return
        self.set(matches[0])
        self.icursor(len(text))
    
    def ctrl_back(self):
        text = self.get().split('_')
        self.set('_'.join(text[0:len(text)-1]))
    
    # as per the documentation of ttkwidgets.autocomplete.AutocompleteCombobox in this version,
    # this allows the combobox to not mess up with the desired order of the options by NOT sorting the list
    def set_completion_list(self, completion_list):
        """
        Use the completion list as drop down selection menu, arrows move through menu.

        :param completion_list: completion values
        :type completion_list: list
        """
        self._completion_list = completion_list  # Work with a unsorted list
        self.configure(values=completion_list)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu
        