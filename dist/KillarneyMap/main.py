import kivy.factory
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from Graphing import *
from kivy.config import Config
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.core.text import LabelBase
from kivy.uix.spinner import SpinnerOption


Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


# from kivy.uix.textinput import TextInput
class MySpinnerOption(SpinnerOption):
    pass

class RoundButton(Button):
    btn_color = ListProperty()


class MainScreen(BoxLayout):
    Map = Graph()
    whatList, connector = Map.importNodes("finalmap.csv")

    def test(self):
        print("yes someone is typing")
        print(self.ids)

    def searchValues(self, searchValue, spinnerId):  # add value and place
        list = [x for x in self.whatList if searchValue.lower() in x.lower()]
        if len(list) == 0:
            self.ids[spinnerId].text = "no result"
        else:
            self.ids[spinnerId].text = list[0]
        self.ids[spinnerId].values = list

    def changeValue(self, value, place):
        self.ids[place].text = value
        # place = value

    def drawPath(self):
        start = self.connector[self.ids.starting_spinner.text]
        end = self.connector[self.ids.destination_spinner.text]
        print(start, end)
        self.Map.displayPath(start, end)
        self.ids.map_id.source = f"images/{start}_{end}.png"

    def clear(self):
        self.ids.destination_input.text = ""
        self.ids.starting_input.text = ""
        self.ids.destination_spinner.values = self.whatList
        self.ids.starting_spinner.values = self.whatList
        self.ids.map_id.source = "FullFloor.png"

    def select(self):
        print(self.ids.drop.text)

    pass


# [x for x in list if "input" in x]
class ClassroomInput(BoxLayout):
    pass


class KillarneyMapApp(App):
    def build(self):
        self.icon = "paw.png"
        return MainScreen()


if __name__ == '__main__':
    LabelBase.register(name='Varela', fn_regular='VarelaRound-Regular.ttf')
    KillarneyMapApp().run()

# from kivy.base import runTouchApp
# from kivy.lang import Builder
# from kivy.factory import Factory
#
# Builder.load_string('''
# <FDDButton@Button>:
#     size_hint_y: None
#     height: '50dp'
#
# <FilterDD>:
#     auto_dismiss: False
# ''')
#
#
# class FilterDD(Factory.DropDown):
#     def __init__(self, buttons, **kwargs):
#         super(FilterDD, self).__init__(**kwargs)
#         self._buttons = buttons
#         self._filter = filter = Factory.TextInput(size_hint_y=None)
#         self.add_widget(filter)
#         filter.bind(text=self.apply_filter)
#         self.apply_filter(None, '')
#
#         # You need this to add widgets here for apply_filter2:
#         # for text in buttons:
#         #    self.add_widget(Factory.FDDButton(text=text))
#
#     def apply_filter(self, wid, value):
#         self.clear_widgets()
#         self.add_widget(self._filter)
#         for btn in self._buttons:
#             if not value or value in btn:
#                 self.add_widget(Factory.FDDButton(text=btn))
#
#     def apply_filter2(self, wid, value):
#         if not value:
#             return
#         for btn in self.container.children[:-1]:  # skip textinput
#             if value in btn.text:
#                 self.scroll_to(btn)
#                 break
#
#
# fdd = FilterDD(["one", "two", "three", "four", "five", "six",
#                 "seven", "eight", "nine", "ten"])
#
# runTouchApp(Builder.load_string('''
# #:import fdd __main__.fdd
#
# Button:
#     size_hint: None, None
#     pos: 200, 200
#     on_press:
#         fdd.open(self)
# '''))
