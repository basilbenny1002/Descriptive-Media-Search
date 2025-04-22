
import threading
import app
import flet as ft
import functions
def pdata(e):
    if e == "search_button":
        print("button found ee")
        results = functions.process_search(app.app_instance.search_field.value)
        app.app_instance.add_images(results)
    elif e == "start_button":
        thread = threading.Thread(target=functions.process_start, args=(app.get_choosen_paths(), update_progress))
        thread.start()
        app.app_instance.build_embedding_ui()
    else:
        print(e)

def update_progress():
    max_value = functions.number_of_files
    current_value = functions.completed_files
    new_value = ((current_value - 0) / (max_value - 0)) * (100 - 0) + 0
    new_value = new_value / 100
    print(new_value)
    print(max_value)
    print(current_value)
    app.app_instance.value = new_value
    app.app_instance.build_embedding_ui()
    time_taken = functions.time_per_it
    time_remaining = int(time_taken) * (max_value - current_value)
    time_string = f"{time_remaining // 60}: {time_remaining % 60}"
    app.app_instance.time_remaining = ft.Text(time_string)
    if current_value == max_value:
        app.app_instance.build_ui()


FRESH_INSTALL = False
try:
    with open("ebbeddings.db", 'r') as database:
        pass
except FileNotFoundError:
    print("Fresh install")
    FRESH_INSTALL = True

ft.app(target=app.App(call_back=pdata, fresh_install=FRESH_INSTALL).main)





