import os
import time
import flet as ft
import datetime
from PIL import Image
import functions

app_instance = None
class App:
    def __init__(self, call_back, fresh_install: bool):
        """
        Inits different components of teh GUI
        :param call_back:
        """
        global app_instance
        app_instance = self
        self.fresh_install = fresh_install
        self.page = None
        self.theme_mode = "light"
        self.toggle_button = ft.Switch(label="Dark Mode", on_change=self.toggle_theme, focus_color=ft.colors.GREEN_100)
        self.search_field = ft.TextField(hint_text="Search...", border_radius=20, expand=True, autofocus=True,
                                         autocorrect=True, filled=True, fill_color='#7a95ff', border_color=ft.colors.BLACK12)
        self.search_button = ft.ElevatedButton("Search", bgcolor='#7a95ff', data="search_button", on_click=self.clicked)
        self.images = ft.GridView(expand=True, runs_count=3, spacing=5, run_spacing=5)

        self.click_event = call_back
        # Welcome page UI components
        self.welcome = ft.Text("Welcome to \ndescriptive media search", size=20, color="#0f1345")
        self.path_Selection = ft.Text("Choose the paths you want to include to get started", size=15, color="#0f1345")
        self.user_name = os.getlogin()
        self.path_list = [fr"\{self.user_name}\Documents", fr"\{self.user_name}\Pictures",
                          fr"\{self.user_name}\Pictures\Screenshots", fr"\{self.user_name}\OneDrive\Pictures",
                          fr"\{self.user_name}\OneDrive\Pictures\Screenshots", fr"\{self.user_name}\OneDrive\Documents",
                          fr"\{self.user_name}\Desktop"]
        self.check_boxes = [ft.Checkbox(label=i, value=True, focus_color="#0f1345", label_style=ft.TextStyle(color="#0f1345")) for i in self.path_list]
        self.file_picker = ft.FilePicker(on_result=self.on_dialog_result)
        self.browse = ft.ElevatedButton("Browse", tooltip="Add a custom path to the media library",
                                        on_click=lambda _: self.file_picker.get_directory_path(), color="7a95ff")
        self.generate_embeddings_button = ft.ElevatedButton("Start", on_click=self.clicked, data="start_button", tooltip="Start generating the embeddings", color="7a95ff")
        self.file_path = None
        #Generating embeddings elements
        self.file_name = ft.Text(f"Generating embedding for {self.file_path}")
        self.progress_bar = ft.ProgressBar(value=0)
        self.value = 0.0
        self.time_elapsed = ft.Text(str(datetime.time))
        self.time_remaining = ft.Text(str(datetime.time))
        self.time_data = ft.Text(f"Time elapsed {time}")
    def clicked(self, e):
        """
        Function called during a button click event
        :param e:
        :return:
        """
        self.click_event(e.control.data)
    def main(self, page: ft.Page):
        """
        Main window build function
        :param page:
        :return:
        """
        self.page = page
        self.page.title = "Descriptive Media Search"
        self.page.window.width = 500
        self.page.window.height = 400
        self.page.bgcolor = '#a3b9ff'
        if self.fresh_install:   
            self.build_welcome_ui()
        else:
            self.build_ui()
        

    def toggle_theme(self, e):
        if self.theme_mode == "light":
            self.theme_mode = "dark"
            self.page.bgcolor = '#5c5d76'
            self.search_field.bgcolor = '#9b9fcd'
            self.search_button.bgcolor = '#0b177e'
            # self.toggle_button.value = 'Dark mode'
        else:
            self.theme_mode = "light"
            self.search_field.bgcolor = '#e3e6fa'
            self.page.bgcolor = '#a3b9ff'
            self.search_button.bgcolor = '#7a95ff'
            # self.toggle_button.value = 'Light Mode'
        self.page.update()

    def build_ui(self):
        """
        Builds teh search UI for the app
        :return:
        """
        self.page.clean()
        search_row = ft.Row([self.search_field, self.search_button], alignment=ft.MainAxisAlignment.CENTER)
        self.page.add(self.toggle_button, search_row)
        self.page.add(self.images)

    def build_welcome_ui(self):
        """
        Builds the welcome UI for the app for a fresh intall/open
        :return:
        """
        self.page.clean()
        controls_stuff = ft.Column([self.path_Selection])
        for i in self.check_boxes:
            controls_stuff.controls.append(i)
        controls_stuff.controls.append(self.browse)
        welcome_section = ft.Column([self.welcome, self.generate_embeddings_button])
        data_column = ft.Row([welcome_section, controls_stuff])
        self.page.add(data_column)
        self.page.overlay.append(self.file_picker)
        self.page.update()

    def on_dialog_result(self, e: ft.FilePickerResultEvent):
        """
        Function called when a path selecting window is closed
        :param e:
        :return:
        """
        print(type(e.path))
        self.add_new_path(e.path)

    def on_image_click(self, img_path):
        """
        Function called when an image is clicked from the grid
        :param img_path:
        :return:
        """
        img = Image.open(img_path)
        img.show()
        print(f"Image clicked{img_path}")

    def add_images(self, image_paths: list):
        """
        Adds the found images to the display grid
        :param image_paths:
        :return:
        """
        self.images.controls.clear()
        for img in image_paths:
            try:
                with Image.open(img) as img_obj:
                    width, height = img_obj.size
                grid_item = ft.Container(
                    content=ft.Image(src=img, fit=ft.ImageFit.COVER),
                    width=min(width, 200),  # Set a max width limit
                    height=min(height, 200),  # Set a max height limit
                    on_click=lambda e, img=img: self.on_image_click(img)
                )

                self.images.controls.append(grid_item)
            except:
                print(f"Could't find the image{img}")
        print("images_added")
        self.build_ui()
        self.page.update()


    def add_new_path(self, path):
        """
        Brings up a pop-up window to choose new paths to add to the image collection
        :param path:
        :return:
        """
        self.page.clean()
        self.check_boxes.append(ft.Checkbox(label=path, value=True, label_style=ft.TextStyle(color="#0f1345")))
        controls_stuff = ft.Column([self.path_Selection], scroll=ft.ScrollMode.AUTO)
        for i in self.check_boxes:
            controls_stuff.controls.append(i)
        controls_stuff.controls.append(self.browse)
        controls_container = ft.Container(content=controls_stuff, height=370)
        welcome_section = ft.Column([self.welcome, self.generate_embeddings_button])
        data_column = ft.Row([welcome_section, controls_container])
        self.page.add(data_column)
        self.page.update()

    def build_embedding_ui(self):
        """
        Builds a UI to show the progress of generating embedding
        :return:
        """
        self.page.clean()
        self.page.add(self.progress_bar, self.file_name)
        self.progress_bar.value = self.value
        self.page.add(self.time_remaining, self.time_remaining)
        self.page.update()
        # for i in range(0, 100):
        #     time.sleep(0.5)
        #     self.progress_bar.value = self.value
        #     self.value = self.value + 0.1
        #     self.page.update()
            # self.build_embedding_ui()

file_paths = [
    r"C:\Users\basil\Downloads\74f00b3d171263b7e39bf283349c9d1d.png",
    r"C:\Users\basil\Downloads\7ed08613-1e46-4f12-b090-fc12d124dd83.png",
    r"C:\Users\basil\Downloads\ammaaa.jpg",
    r"C:\Users\basil\Downloads\bcba343d026e95c61f1b41c8c5a268e2.jpg",
    r"C:\Users\basil\Downloads\download.jpeg",
    r"C:\Users\basil\Downloads\eeeeeee.jpg",
    r"C:\Users\basil\Downloads\GbobSZEXkAA6Jqz.jpg",
    r"C:\Users\basil\Downloads\GOt5VtYWMAAl3HA.jpg",
    r"C:\Users\basil\Downloads\GWZUTt7WkAE2uZ5.jpg",
    r"C:\Users\basil\Downloads\image.png"
]
# def pdata(e):
#     if e == "search_button":
#         print("button found ee")
#         print(e)
#         app_instance.add_images(file_paths)
#         print("images should be aded now")
#     elif e == "start_button":
#         chosen_paths = get_choosen_paths()
#         functions.process_start(chosen_paths)
#
#     else:
#         print(f"Smth else clicked{e}")
#         get_choosen_paths()
def get_choosen_paths()->list:
    """
    To get a list of the directory paths chosen by the user
    :return: A list of the chosen paths
    """
    paths = []
    for i in app_instance.check_boxes:
        if i.value == True:
            if ":" in i.label:
                paths.append(i.label)
            else:
                paths.append(fr"C:\Users{i.label}")
    return paths
app_instance: App
if __name__ == "__main__":
    ft.app(target=App().main)


