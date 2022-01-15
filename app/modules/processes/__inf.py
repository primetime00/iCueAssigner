import copy
class ProcessResponder:

    def __init__(self):
        self.keyMap = {}


    def process(self):
        return ""

    def name(self):
        return ""

    def hasKey(self, eventType, button):
        return button in self.keyMap and eventType in self.keyMap[button]

    def key(self, eventType, button, proc, text):
        if button in self.keyMap and eventType in self.keyMap[button]:
            self.keyMap[button][eventType]['function'](text, proc)

    def help(self, *args):
        hm = copy.deepcopy(self.keyMap)
        for button, events in hm.items():
            for event, action in events.items():
                helpText = '('+self.name()+')' + ' ' + action['help']
                action['help'] = helpText
        return hm
