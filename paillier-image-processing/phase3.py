import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from PIL import Image as PILImage
from paillier import paillier
import numpy as np
import tkinter as tk
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from tkinter import ttk
from functools import partial


class Phase3Screen(Screen):
    def __init__(self, **kwargs):
        super(Phase3Screen, self).__init__(**kwargs)
        self.screen_index = None
        self.pail = paillier()
        self.priv, self.pub = self.pail.generate_keypair(int(20))
        self.c_image = None
        self.d_image = None
        self.output_image = None
        self.input_image = None
        self.is_encrypted = False
        self.import_button_disabled = False

    def import_image(self):
        if self.import_button_disabled:
            return

        initial_dir = os.getcwd()  # Set initial directory here
        file_chooser = FileChooserListView(path=initial_dir)
        file_chooser.bind(on_submit=self.load_image)
        self.ids.file_chooser_container.clear_widgets()
        self.ids.file_chooser_container.add_widget(file_chooser)
        self.import_button_disabled = True

    def load_image(self, chooser, file_path, *args):
        self.input_image = PILImage.open(file_path[0])
        self.input_image.thumbnail((588, 375))
        self.ids.input_image.source = file_path[0]
        self.is_encrypted = False
        self.output_image = None

    def encrypt_image(self):
        if self.input_image is None:
            return
        image = np.array(self.input_image)
        self.c_image = self.pail.encrypt_image(self.pub, image)
        self.is_encrypted = True
        self.output_image = PILImage.fromarray(self.c_image.astype(np.uint8))  # Convert to uint8
        output_path = "encrypted_image.png"  # Set output path
        self.output_image.save(output_path)  # Save encrypted image
        self.ids.output_image.source = output_path

    def decrypt_image(self):
        if not self.is_encrypted:
            return

        self.d_image = self.pail.decrypt_image(self.priv, self.pub, self.c_image)
        self.is_encrypted = False
        self.output_image = PILImage.fromarray(self.d_image.astype(np.uint8))  # Convert to uint8
        output_path = "decrypted_image.png"  # Set output path
        self.output_image.save(output_path)  # Save decrypted image
        self.ids.output_image.source = output_path
    
    def flip_image(self):
        if not self.is_encrypted:
            self.encrypt_image()

        self.c_image = self.pail.flip_image(self.pub, self.c_image)
        self.output_image = PILImage.fromarray(self.c_image.astype(np.uint8))  # Convert to uint8
        output_path = "flipped_encrypted_image.png"  # Set output path
        self.output_image.save(output_path)  # Save flipped encrypted image
        self.ids.output_image.source = output_path

    def mirror_image(self):
        if not self.is_encrypted:
            self.encrypt_image()

        self.c_image = self.pail.mirroring_image(self.pub, self.c_image)
        self.output_image = PILImage.fromarray(self.c_image.astype(np.uint8))  # Convert to uint8
        output_path = "mirrored_encrypted_image.png"  # Set output path
        self.output_image.save(output_path)  # Save mirrored encrypted image
        self.ids.output_image.source = output_path

    def output_image_callback(self, c_image, screen_index):
        if screen_index == 1:
            self.root.ids.input_image.source = 'temp_input_image.png'
        elif screen_index == 2:
            self.root.ids.output_image.source = 'temp_output_image.png'

    def brightness(self):
        def apply_brightness(slider, value):
            # Update the brightness of the image
            self.c_image = self.pail.brightness(self.pub, self.c_image, value)
            self.output_image = PILImage.fromarray(self.c_image.astype(np.uint8))  # Convert to uint8
            temp_output_path = "temp_output_image.png"  # Temporary output path
            self.output_image.save(temp_output_path)  # Save temporary output image
            self.ids.output_image.source = temp_output_path  # Update the source of the output image widget
            self.output_image_callback(self.output_image, self.screen_index)  # Call output_image_callback

        brightness_popup = Popup(title="Adjust Brightness", size_hint=(None, None), size=(250, 180))
        
        brightness_label = Label(text="Brightness")
        brightness_slider = Slider(min=0, max=255, value=255/2)
        
        # Bind the value of the slider to the apply_brightness function
        brightness_slider.bind(value=apply_brightness)
        
        cancel_button = Button(text="Cancel", on_release=brightness_popup.dismiss)
        
        brightness_popup_content = BoxLayout(orientation='vertical')
        brightness_popup_content.add_widget(brightness_label)
        brightness_popup_content.add_widget(brightness_slider)
        brightness_popup_content.add_widget(cancel_button)
        
        brightness_popup.content = brightness_popup_content
        brightness_popup.open()


 
class MainApp(App):
    def build(self):
        return Phase3Screen()

if __name__ == "__main__":
    MainApp().run()

