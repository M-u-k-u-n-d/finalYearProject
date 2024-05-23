from tkinter import ttk
from tkinter import *
import cv2

import cv2
import time
import os
import ImageCaption

import traceback
import logging





def capture_process_image(camera,things):
    # Open the webcam
    camera=int(camera)
    cap = cv2.VideoCapture(camera)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Unable to access the webcam.")
        return

    # Set the capture resolution (optional)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if not ret:
                print("Error: Unable to capture frame.")
                break

            # Process the image (Replace this with your own image processing code)
            processed_frame = frame.copy()  # Placeholder example: No processing

            # Save the image with a timestamp as the filename
            timestamp = int(time.time())
            image_filename = f"captured_image_{timestamp}.jpg"
            

            cv2.imwrite(image_filename, processed_frame)
            
            print(f"Image saved as: {image_filename}")
            caption=ImageCaption.caption_this_image(image_filename)
            print(caption)
            flag=0
            for i in things:

                if i in caption:
                    flag=1
                    
                
            if(flag==0):
                os.remove(image_filename)


            # Wait for 10 seconds before capturing the next image
            time.sleep(10)
            

            

            
            

    except KeyboardInterrupt:
        print("Image capturing stopped by the user.")

    # Release the webcam and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


window=Tk()
window.title('cctv')
x_=50
y_=50
window.geometry("600x300+" + str(x_) + "+" + str(y_))
altertypes=[]


# label
lbl=Label(window,text="CCTV MONITOR")
lbl.config(font=("Courier", 22))
lbl.config(fg="#0000FF")

lbl.place(x=200,y=15)

lbl = Label(window, text="Camera ")
lbl.config(font=("Courier", 12))
lbl.place(x=70, y=70)

camera_options=[]

# Load camera values from file
def load_camera_list():
    try:
        with open("camera_list.txt", "r") as file:
            camera_options.extend(file.read().splitlines())
            camera_dropdown['values'] = camera_options
    except:
        pass

# Function to handle saving the camera list
def save_camera_list():
    entered_text = camera_entry.get()
    camera_options.append(entered_text)
    camera_dropdown['values'] = camera_options
    camera_entry.delete(0, END)
    

    # Save camera values to file
    with open("camera_list.txt", "w") as file:
        file.write("\n".join(camera_options))

# Function to handle deleting the selected camera
def delete_camera():
    selected_camera = camera_dropdown.get()
    camera_options.remove(selected_camera)
    camera_dropdown.set('')
    camera_dropdown['values'] = camera_options
    print("Deleted Camera:", selected_camera)

    # Save camera values to file
    with open("camera_list.txt", "w") as file:
        file.write("\n".join(camera_options))

selected_camera = StringVar()

# Create the combobox widget
camera_dropdown = ttk.Combobox(window, textvariable=selected_camera, state='readonly')
camera_dropdown['values'] = camera_options
camera_dropdown.place(x=150, y=70)

# Create an entry field for the user to enter a camera
placeholder="Enter camera path"
def remove_placeholder(event):
    if camera_entry.get() == placeholder:
        camera_entry.delete(0, 'end')
        camera_entry.config(fg='black')

def add_placeholder(event):
    if camera_entry.get() == "":
        camera_entry.insert(0, placeholder)
        camera_entry.config(fg='gray')

camera_entry = Entry(window,fg='gray')

camera_entry.insert(0, placeholder)
camera_entry.bind("<FocusIn>", remove_placeholder)
camera_entry.bind("<FocusOut>", add_placeholder)
camera_entry.place(x=310, y=70)


# Create a button to save the entered camera
save_button = Button(window, text="Save", command=save_camera_list)
save_button.place(x=460, y=65)

# Create a button to delete the selected camera
delete_button = Button(window, text="Delete", command=delete_camera)
delete_button.place(x=517, y=65)


# Load camera values on startup
load_camera_list()

# Function to handle the selection change
def on_camera_selected(event):
    selected_camera = camera_dropdown.get()
    

# Bind the event handler function to the combobox selection change event
camera_dropdown.bind("<<ComboboxSelected>>", on_camera_selected)




# entering values to detect
lbl=Label(window,text='Enter values ')
lbl.config(font=("Courier", 10))
lbl.place(x=70,y=150)

lbl=Label(window,text='to detect ')
lbl.config(font=("Courier", 10))
lbl.place(x=70,y=170)


things_options=[]

# Load things values from file
def load_things_list():
    try:
        with open("things_list.txt", "r") as file:
            things_options.extend(file.read().splitlines())
            things_dropdown['values'] = things_options
    except:
        pass

# Function to handle saving the things list
def save_things_list():
    entered_text = things_entry.get()
    things_options.append(entered_text)
    things_dropdown['values'] = things_options
    things_entry.delete(0, END)
    

    # Save things values to file
    with open("things_list.txt", "w") as file:
        file.write("\n".join(things_options))

# Function to handle deleting the selected things
def delete_things():
    selected_things = things_dropdown.get()
    things_options.remove(selected_things)
    things_dropdown.set('')
    things_dropdown['values'] = things_options
    print("Deleted things:", selected_things)

    # Save things values to file
    with open("things_list.txt", "w") as file:
        file.write("\n".join(things_options))

selected_things = StringVar()

# Create the combobox widget
things_dropdown = ttk.Combobox(window, textvariable=selected_things, state='readonly')
things_dropdown['values'] = things_options
things_dropdown.place(x=340, y=150)

# Create an entry field for the user to enter a things
placeholderthings="Enter things"
def remove_placeholder(event):
    if things_entry.get() == placeholderthings:
        things_entry.delete(0, 'end')
        things_entry.config(fg='black')

def add_placeholder(event):
    if things_entry.get() == "":
        things_entry.insert(0, placeholderthings)
        things_entry.config(fg='gray')

things_entry = Entry(window,fg='gray')

things_entry.insert(0, placeholderthings)
things_entry.bind("<FocusIn>", remove_placeholder)
things_entry.bind("<FocusOut>", add_placeholder)
things_entry.place(x=200, y=150)


# Create a button to save the entered things
save_button_things = Button(window, text="Save", command=save_things_list)
save_button_things.place(x=200, y=183)

# Create a button to delete the selected things
delete_button_things = Button(window, text="Delete", command=delete_things)
delete_button_things.place(x=270, y=183)


# Load things values on startup
load_things_list()

# Function to handle the selection change
def on_things_selected(event):
    selected_things = things_dropdown.get()
    

# Bind the event handler function to the combobox selection change event
things_dropdown.bind("<<ComboboxSelected>>", on_things_selected)




def run_command():
    
    # window.withdraw()

    try:
        capture_process_image(camera_dropdown.get(),things_options)
    except Exception as e:
            logging.error(traceback.format_exc())


## RUN BUTTON
run_button = Button(window, text="RUN", command=run_command)
run_button.place(x=460, y=255)












window.mainloop()

