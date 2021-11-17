import os
import PySimpleGUI as sg
from psgtray import SystemTray
from user import User
from PIL import Image
import base64
from io import BytesIO
import globals

"""
def image_to_base64(image: Image):
    buffer = BytesIO()
    image.save(buffer, format=image.format)
    result = base64.b64encode(buffer.getvalue())
    print(result)
    return result

app_icon = Image.open(os.path.join(os.path.dirname(__file__), os.pardir, "img", "logo_without_text.png"))
app_icon = image_to_base64(app_icon)"""

def gui_loop():
    menu = ['', ['Show Window', 'Hide Window', 'Exit']]
    tooltip = 'Tooltip'

    layout = [[sg.Text("AULIS Login", size =(15, 1), font=40)],
              [sg.Text("Username", size =(15, 1), font=16),sg.InputText(key='-USERNAME-', size=(25, 1), font=16)],
              [sg.Text("Password", size =(15, 1), font=16),sg.InputText(key='-PASSWORD-', size=(25, 1), password_char='*', font=16)],
              [sg.Button("Login"), sg.B("Logout")],
              [sg.HorizontalSeparator(key='sep')],
              [sg.Button("Synchronize", disabled=True)],
              [sg.HorizontalSeparator(key='sep')],
              [sg.Text("Synchronization Options", size =(25, 1), font=40)],
              [sg.Text("Courses to sync:")],
              [sg.Checkbox('BESYST', default=True)],
              [sg.Text("Other:")],
              [sg.Checkbox("Live mode", default=False)],
              [sg.Text("Output Folder:"), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
              [sg.Listbox(values=[], enable_events=True, size=(60,10),key='-FILE LIST-')],
              [sg.HorizontalSeparator(key='sep')],
              [sg.Text("Console", size =(25, 1), font=40)],
              [sg.Multiline(size=(60,10), reroute_stdout=False, reroute_cprint=True, write_only=True, key='-OUT-')],
              [sg.HorizontalSeparator(key='sep')],
              [sg.Button('Go'), sg.B('Hide Window'), sg.Button('Exit')]]

    window = sg.Window("IliasSync", layout, finalize=True, enable_close_attempted_event=True)

    # Disable login button if logged in
    window.FindElement("Logout").Update(disabled=True, visible=False)
    # Disable logout button if not logged in TODO

    tray = SystemTray(menu, single_click_events=False, window=window, tooltip=tooltip, icon=sg.EMOJI_BASE64_HAPPY_BIG_SMILE)
    sg.cprint(sg.get_versions())

    user = None # TODO
    print(globals.user)
    if globals.user:
        window.FindElement("-USERNAME-").Update(globals.user.username)
        window.FindElement("-PASSWORD-").Update(globals.user.password_hash)
        window["Login"].click()
        sg.cprint(globals.user)
        print("A user exists!")
        print("hide login button")

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        sg.cprint(event)

        if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()
        elif event in ('Hide Window', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            window.hide()
            tray.show_icon()  # if hiding window, better make sure the icon is visible
            # tray.notify('System Tray Item Chosen', f'You chose {event}')
        elif event == "Login":
            sg.cprint("Starting the login...")
            # Grabbing the username and password input
            user = User(values["-USERNAME-"], values["-PASSWORD-"])
            # Make the logout button visible if we were successfully logged in
            if user.login():
                sg.cprint("We successfully logged in")
                window.FindElement("Logout").Update(disabled=False, visible=True)
                window.FindElement("Login").Update(disabled=True, visible=False)
                window.FindElement("Synchronize").Update(disabled=False)
            else:
                sg.cprint("Login was not successful, please check your password!")
        elif event == "Logout":
            sg.cprint("You are logged out")
            # Hide logout button and show login
            window.FindElement("Logout").Update(disabled=True, visible=False)
            window.FindElement("Login").Update(disabled=False, visible=True)
        elif event == "Synchronize":
            # Synchronize the elements of the user
            user.synchronize()
        elif event == '-FOLDER-': # Folder name was filled in, make a list of files in the folder
            folder = values['-FOLDER-']
            try:
                file_list = os.listdir(folder) # get list of files in folder
            except:
                file_list = []
            finally:
                fnames = [f for f in file_list]
                window['-FILE LIST-'].update(fnames)

    tray.close() # optional but without a close, the icon may "linger" until moused over
    window.close()
