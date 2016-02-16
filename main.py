#!/usr/bin/env python
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty
from kivy.factory import Factory
from kivy.uix.popup import Popup
import glob, threading, os
from PIL import Image
from Processing import tspart

class FileChooser(Widget):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class EditorGame(Widget):
    filename = StringProperty("")
    path = StringProperty("")

    def convert_file(self):
        self.ids.progress_bar.anim_delay = 0.04
        self.ids.choose_btn.disabled = True
        self.ids.convert_btn.disabled = True
        mythread = threading.Thread(target=self.run)
        mythread.start()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_chooser(self):
        content = FileChooser(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Choose File", content=content, size_hint=(0.9,0.9))
        self._popup.open()

    def load(self, path, filename):
        self.path = path
        self.filename = filename
        self.ids.file_label.text = filename
        self.ids.convert_btn.disabled = False
        self.dismiss_popup()

    def exit(self):
        exit(0)

    def run(self):
        for filename in glob.glob(self.filename):
            im = Image.open(filename)
            im = im.convert('1')
            newFilename = os.path.splitext(filename)[0] + '.pbm'
            im.save(newFilename)
            saveFilename = self.path + "/" + os.path.splitext(os.path.basename(filename))[0] + '.svg'
            tspart.runtspart(newFilename, saveFilename)
        self.ids.progress_bar.anim_delay = -1
        self.ids.choose_btn.disabled = False
        self.ids.file_label.text = "SVG File Written to " + self.path

class EditorApp(App):
    def build(self):
        editor = EditorGame()
        # editor.run()
        return editor

Factory.register('FileChooser', cls=FileChooser)

if __name__ == '__main__':
    EditorApp().run()