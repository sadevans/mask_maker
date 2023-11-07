import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import font,ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import os
import numpy as np

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

class MaskEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mask Editor")

        self.path_denoised = None
        self.path_mask = None

        self.filenames_img = None
        self.filenames_mask = None
        self.filenames_img_ = None
        self.filenames_mask_ = None
        self.files_img = None
        self.files_mask = None
        self.miss_masks = None
        self.images_without_masks = None

        self.all_have_masks = True
        self.other_ext = False
        self.no_images = False

        self.layout = tk.Grid()

        instruction_label = tk.Label(root, text="Choose editing mode", font=("Montserrat", 14))
        instruction_label.grid(row=0, column=0, columnspan=2)

        edit_button = tk.Button(root, text="Edit mask", command=self.select_edit_mode)
        edit_button.grid(row=1, column=0, padx=10, pady=10)

        create_button = tk.Button(root, text="Create mask", command=self.select_create_mode)
        create_button.grid(row=1, column=1, padx=10, pady=10)

    def select_edit_mode(self):
        self.root.destroy()  # Закрываем окно выбора режима
        self.show_select_folders("Edit mask")

    def select_create_mode(self):
        self.root.destroy()  # Закрываем окно выбора режима
        self.show_select_folders("Create mask")

    def show_select_folders(self, mode):
        select_folders = SelectFolders(self.root, mode)

class SelectFolders:
    def __init__(self, root, mode):
        self.root = root
        self.mode = mode
        self.window = tk.Toplevel()
        self.window.title("Select Folders")

        self.path_denoised = None
        self.path_mask = None

        self.filenames_img = None
        self.filenames_mask = None
        self.filenames_img_ = None
        self.filenames_mask_ = None
        self.files_img = None
        self.files_mask = None
        self.miss_masks = None
        self.images_without_masks = None

        self.all_have_masks = True
        self.other_ext = False
        self.no_images = False

        self.layout = tk.Frame(self.window)
        self.which_dir()

    
    def which_dir(self):
        if self.mode == 'Create mask':
            self.choose_imgs_dir()
        elif self.mode == 'Edit mask':
            self.choose_mask_dir()


    def choose_imgs_dir(self):
        instruction_label = tk.Label(self.window, text="Choose paths to image folders", font=("Montserrat", 14))
        instruction_label.grid(row=0, column=1, columnspan=3)

        den_label = tk.Label(self.window, text="Denoised images directory:", font=("Montserrat", 14))
        den_label.grid(row=1, column=0, columnspan=1, sticky="e")
        self.dir_name_edit1 = tk.Entry(self.window)
        self.dir_name_edit1.grid(row=1, column=1, columnspan=1)
        dir_btn1 = tk.Button(self.window, text="Browse", command=self.open_imgs_dir_dialog)
        dir_btn1.grid(row=1, column=2, columnspan=1)

        submit_btn = tk.Button(self.window, text="Submit paths", command=self.check_masks)
        submit_btn.grid(row=2, column=2, columnspan=2)

    
    def choose_mask_dir(self):
        instruction_label = tk.Label(self.window, text="Choose paths to folders", font=("Montserrat", 14))
        instruction_label.grid(row=0, column=1, columnspan=3)

        den_label = tk.Label(self.window, text="Denoised images directory:", font=("Montserrat", 14))
        den_label.grid(row=1, column=0, columnspan=1, sticky="e")
        self.dir_name_edit1 = tk.Entry(self.window)
        self.dir_name_edit1.grid(row=1, column=1, columnspan=1)
        dir_btn1 = tk.Button(self.window, text="Browse", command=self.open_imgs_dir_dialog)
        dir_btn1.grid(row=1, column=2, columnspan=1)

        mask_label = tk.Label(self.window, text="Mask images directory:", font=("Montserrat", 14))
        mask_label.grid(row=2, column=0, columnspan=1, sticky="e")
        self.dir_name_edit2 = tk.Entry(self.window)
        self.dir_name_edit2.grid(row=2, column=1, columnspan=1)
        dir_btn2 = tk.Button(self.window, text="Browse", command=self.open_masks_dir_dialog)
        dir_btn2.grid(row=2, column=2, columnspan=1)

        submit_btn = tk.Button(self.window, text="Submit paths", command=self.check_masks)
        submit_btn.grid(row=3, column=2, columnspan=2)



    def check_masks(self):
        if self.mode == 'Create mask':
            if self.path_denoised is None:
                messagebox.showwarning("Warning", "Please choose imgs folder and try again.")
            else:
                self.get_images()
                if self.no_images:
                    messagebox.showwarning("Warning", "The selected folder does not contain image files.\nPlease choose a valid folder.")
                    self.no_images = False
                else:
                    self.open_photo_viewer()

        if self.mode == 'Edit mask':
            if self.path_mask is None or self.path_denoised is None:
                messagebox.showwarning("Warning", "Please choose both folders and try again.")
            else:
                self.get_images()
                if self.no_images:
                    messagebox.showwarning("Warning", "The selected folder does not contain image files.\nPlease choose a valid folder.")
                    self.no_images = False
                else:
                    if self.all_have_masks:
                        self.open_photo_viewer()
                    else: 
                        self.open_check_masks()


    def get_images(self):
        file_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff'}

        if self.mode == 'Create mask':
            self.filenames = os.listdir(self.path_denoised)
            self.ext = np.unique([file[-4:] for file in self.filenames])

            if len(set(self.ext).intersection(file_extensions)) != 0:
                self.filenames_ = [file for file in self.filenames if file[-4:] in file_extensions]
                self.filenames_.sort()
                self.filenames = None
                self.files = [file[:-4] for file in self.filenames_]

            else:
                self.no_images = True

        if self.mode == 'Edit mask':
            self.filenames_img = os.listdir(self.path_denoised)
            self.filenames_mask = os.listdir(self.path_mask)

            self.img_ext = np.unique([file[-4:] for file in self.filenames_img])
            self.mask_ext = np.unique([file[-4:] for file in self.filenames_mask])

            if len(set(self.img_ext).intersection(file_extensions)) != 0 and len(set(self.mask_ext).intersection(file_extensions)) != 0:
                self.filenames_img_ = [file for file in self.filenames_img if file[-4:] in file_extensions]
                self.filenames_mask_ = [file for file in self.filenames_mask if file[-4:] in file_extensions]

                self.filenames_img_.sort()
                self.filenames_mask_.sort()
                self.filenames_img = None
                self.filenames_mask = None
                self.files_img = [file[:-4] for file in self.filenames_img_]
                self.files_mask = [file[:-4] for file in self.filenames_mask_]
                if self.files_img != self.files_mask:
                    self.miss_masks = list(set(self.files_img) - set(self.files_mask))
                    self.images_without_masks = [file for file in self.filenames_img_ if file[:-4] in self.miss_masks]
                    self.all_have_masks = False
            else:
                self.no_images = True


    def open_photo_viewer(self):
        print('open photo viewer')
        photo_viewer = PhotoViewer(self.path_denoised, self.path_mask, self.filenames_img_, self.filenames_mask_)

    def open_check_masks(self):
        print('open check masks')
        masks_checker = CheckMasks(self.path_denoised, self.path_mask, self.filenames_img_, self.filenames_mask_, self.images_without_masks)

    def open_imgs_dir_dialog(self):
        dir_name1 = filedialog.askdirectory(title="Select a denoised images directory")
        if dir_name1:
            self.dir_name_edit1.delete(0, tk.END)
            self.dir_name_edit1.insert(0, dir_name1)
            self.path_denoised = dir_name1

    def open_masks_dir_dialog(self):
        dir_name2 = filedialog.askdirectory(title="Select a mask directory")
        if dir_name2:
            self.dir_name_edit2.delete(0, tk.END)
            self.dir_name_edit2.insert(0, dir_name2)
            self.path_mask = dir_name2


class CheckMasks:
    # def __init__(self, main_window, path_denoised, path_mask, filenames_img, filenames_mask, images_without_masks):
    def __init__(self, path_denoised, path_mask, filenames_img, filenames_mask, images_without_masks):
        # self.main_window = main_window
        self.path_denoised = path_denoised
        self.path_mask = path_mask
        self.filenames_img = filenames_img
        self.filenames_mask = filenames_mask
        self.images_without_masks = images_without_masks
        self.new_filenames_img = None
        self.new_filenames_mask = None
        self.current_img_index = 0

        self.root = tk.Toplevel()
        self.root.title("Some images don't have masks")

        instruction_label = tk.Label(self.root, text=f'Всего изображений {len(self.filenames_img)}\nИзображений без масок {len(self.images_without_masks)}\n', font=("Montserrat", 16))
        instruction_label.pack()

        images_without_masks_list = tk.Listbox(self.root, selectmode=tk.SINGLE, height=700)
        images_without_masks_list.pack()
        for file in self.images_without_masks:
            images_without_masks_list.insert(tk.END, file)

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        go_back_btn = tk.Button(button_frame, text="Go back", command=self.open_select_folders)
        go_back_btn.pack(side=tk.LEFT)

        continue_btn = tk.Button(button_frame, text="Ok, continue", command=self.check)
        continue_btn.pack(side=tk.RIGHT)

    def open_select_folders(self):
        self.root.destroy()  # Закрываем текущее окно
        # self.main_window.show_select_folders()

    def check(self):
        if len(self.filenames_img) == len(self.images_without_masks):
            messagebox.showwarning("Warning", "Нет изображений с масками.\nПожалуйста, выберите папки заново.")
        else:
            print('open photo viewer')
            self.open_photo_viewer()

    def open_photo_viewer(self):
        self.new_filenames_img = list(set(self.filenames_img) - set(self.images_without_masks))
        self.new_filenames_mask = list(set(self.filenames_mask) - set(self.images_without_masks))
        # self.photo_viewer = PhotoViewer(self.main_window, self.path_denoised, self.path_mask, self.new_filenames_img, self.new_filenames_mask)
        self.photo_viewer = PhotoViewer(self.path_denoised, self.path_mask, self.new_filenames_img, self.new_filenames_mask)


class PhotoViewer:
    def __init__(self,path_denoised, path_mask, filenames_img, filenames_mask):
        # self.main_window = main_window
        self.path_denoised = path_denoised
        self.path_mask = path_mask
        self.filenames_img = filenames_img
        self.filenames_mask = filenames_mask
        self.current_img_index = 0
        self.current_opacity = 20  # начальное значение = 20 (0.2 * 100)

        self.start_flag = False

        self.selection_rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.imscale = 1.0
        self.delta = 1.2
        self.scale = 1

        self.state_history = []
        self.state_index = -1

        self.color = None
        self.brush_size = None
        # img_path = os.path.join(self.path_denoised, self.filenames_img[index])

        img = cv2.imread(os.path.join(self.path_denoised, self.filenames_img[0]), 0)
        self.canv_height = img.shape[0]
        self.canv_width = img.shape[1]

        self.window = tk.Toplevel()
        self.window.title(self.filenames_img[self.current_img_index])

        self.image_frame = tk.Frame(self.window)
        self.image_frame.grid(row=0, column=0)

        self.canvas = tk.Canvas(self.image_frame, width=self.canv_width, height=self.canv_height, cursor='cross')
        self.canvas.bind("<Button-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)
        self.canvas.bind("<Button-3>", self.delete_area)
        # self.canvas.bind("<MouseWheel>", self.wheel)
        # self.canvas.bind("<Button-5>", self.wheel)
        # self.canvas.bind("<Button-4>", self.wheel)
        self.window.bind("<Control-z>", self.undo)
        self.window.bind("<Control-y>", self.redo)
        self.window.bind("<Control-s>", self.save_file)

        color_lab = tk.Label(self.image_frame, text="Color: ")
        color_lab.grid(row=0, column=0) 

        black_btn = tk.Button(self.image_frame, text="Black", width=10, command=lambda: self.set_color('black'))
        black_btn.grid(row=0, column=1)

        white_btn = tk.Button(self.image_frame, text="White", width=10, command=lambda:self.set_color('white'))
        white_btn.grid(row=0, column=2)

        size_lab = tk.Label(self.image_frame, text="Brush size: ")
        size_lab.grid(row=1, column=0)
        one_btn = tk.Button(self.image_frame, text="1", width=10, command=lambda:self.set_brush_size(1))
        one_btn.grid(row=1, column=1)
        one_btn = tk.Button(self.image_frame, text="2", width=10, command=lambda:self.set_brush_size(2))
        one_btn.grid(row=1, column=2)

        two_btn = tk.Button(self.image_frame, text="5", width=10, command=lambda:self.set_brush_size(5))
        two_btn.grid(row=1, column=3)

        five_btn = tk.Button(self.image_frame, text="7", width=10, command=lambda:self.set_brush_size(7))
        five_btn.grid(row=1, column=4)

        seven_btn = tk.Button(self.image_frame, text="10", width=10, command=lambda:self.set_brush_size(10))
        seven_btn.grid(row=1, column=5)

        ten_btn = tk.Button(self.image_frame, text="20", width=10, command=lambda:self.set_brush_size(20))
        ten_btn.grid(row=1, column=6)

        twenty_btn = tk.Button(self.image_frame, text="50", width=10, command=lambda:self.set_brush_size(50))
        twenty_btn.grid(row=1, column=6)
        
        self.canvas.grid(row=2, column=1, columnspan=5,sticky="nsew")
        
        if not self.start_flag:
            self.start_flag = True
            self.img_path = os.path.join(self.path_denoised, self.filenames_img[0])
            self.mask_path = os.path.join(self.path_mask, self.filenames_mask[0])
            print(self.img_path)
            self.img = Image.open(self.img_path)
            self.img = self.img.convert('L')
            self.mask = Image.open(self.mask_path)
            self.mask = self.mask.convert('L')
            img_ = Image.blend(self.img, self.mask, self.current_opacity / 100)
            photo = ImageTk.PhotoImage(img_)
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.image = photo
            self.window.title(self.filenames_img[self.current_img_index])
            self.img_cv = cv2.imread(self.img_path, 0)
            self.mask_cv = cv2.imread(self.mask_path, 0)
            self.save_state(self.mask_cv)

        prev_button = tk.Button(self.image_frame, text="<", command=self.swipe_left)
        prev_button.grid(row=2, column=0)

        next_button = tk.Button(self.image_frame, text=">", command=self.swipe_right)
        next_button.grid(row=2, column=6)

        self.show_images(self.current_img_index, mode_show='original')

        self.opacity_label = tk.Label(self.image_frame, text="Opacity")
        self.opacity_label.grid(row=3, column=0)


        self.opacity_slider = ttk.Scale(self.image_frame, from_=0, to=100, orient="horizontal", command=self.update_opacity)
        self.opacity_slider.set(20)
        self.opacity_slider.grid(row=3, column=1, columnspan=5, sticky="nsew")

        next_button = tk.Button(self.image_frame, text="save as", command=self.save_as_file)
        next_button.grid(row=3, column=6)

    def save_file(self, event):
        if self.mask_path:
            self.mask.save(self.mask_path)


    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
        initialfile=self.filenames_img[self.current_img_index],
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All Files", "*.*")]
        )
        if file_path:
            self.mask.save(file_path)

    
    def save_state(self, image):
        if self.state_index < len(self.state_history) - 1:
            self.state_history = self.state_history[:self.state_index + 1]
        self.state_history.append(image.copy())
        self.state_index = len(self.state_history) - 1
        print('state saved')


    def undo(self, event):
        print('undo')
        if self.state_index > 0:
            self.state_index -= 1
            self.mask_cv = self.state_history[self.state_index].copy()
            self.mask = Image.fromarray(self.mask_cv)
            self.show_images(self.current_img_index, mode_show=None)


    def redo(self, event):
        print('redo')

        if self.state_index < len(self.state_history) - 1:
            self.state_index += 1
            self.mask_cv = self.state_history[self.state_index].copy()
            self.mask = Image.fromarray(self.mask_cv)
            self.show_images(self.current_img_index, mode_show=None)


    def set_color(self, new_color):
        if self.color == new_color:
            self.color = None
            self.brush_color = None
            self.canvas.bind("<B1-Motion>", self.update_selection)
        else:
            self.color = new_color
            self.redefine_color(self.color)
            if (self.color is not None) and (self.brush_size is not None):
                self.canvas.bind("<B1-Motion>", self.draw)

    
    def redefine_color(self, color):
        if color == 'black':
            self.brush_color = 0
        if color == 'white':
            self.brush_color = 255
        if color == 'gray':
            self.brush_color = 128


    def set_brush_size(self, new_size):
        if self.brush_size == new_size:
            self.brush_size=None
            self.canvas.bind("<B1-Motion>", self.update_selection)
        else:
            self.brush_size = new_size
            if (self.color is not None) and (self.brush_size is not None):
                self.canvas.bind("<B1-Motion>", self.draw)


    def draw(self, event):
        print(self.color, self.brush_size)
        if self.color and self.brush_size:
            x, y = int(self.canvas.canvasx(event.x)), int(self.canvas.canvasy(event.y))
            if self.mask_cv is None:
                self.mask_cv = cv2.imread(self.mask_path, 0)

            cv2.circle(self.mask_cv, (x, y), self.brush_size, self.brush_color, -1)
            self.save_state(self.mask_cv)
            self.mask = Image.fromarray(self.mask_cv)
            self.show_images(self.current_img_index, mode_show=None)


    def refresh(self, event):
        self.color= None
        self.brush_size = None


    def update_opacity(self, value):
        self.current_opacity = float(value)
        self.show_images(self.current_img_index, mode_show=None)


    def show_images(self, index, mode_show='original'):
        if 0 <= index < len(self.filenames_img):
            if mode_show == 'original':
                self.img_path = os.path.join(self.path_denoised, self.filenames_img[index])
                self.mask_path = os.path.join(self.path_mask, self.filenames_mask[index])
                self.img = Image.open(self.img_path)
                self.img = self.img.convert('L')
                self.mask = Image.open(self.mask_path)
                self.mask = self.mask.convert('L')
                mode_show = None
                self.img_cv = cv2.imread(self.img_path, 0)
                self.mask_cv = cv2.imread(self.mask_path, 0)
                self.save_state(self.mask_cv)

            img_ = Image.blend(self.img, self.mask, self.current_opacity / 100)
            photo = ImageTk.PhotoImage(img_)
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.image = photo
            # if mode_show == 'scale':
            #     self.canvas.scale("all", self.center_x, self.center_y, self.imscale, self.imscale)

            self.window.title(self.filenames_img[self.current_img_index])

   
    def swipe_left(self):
        if self.current_img_index > 0:
            self.current_img_index -= 1
            self.state_history = []
            self.state_index = -1
            self.show_images(self.current_img_index, mode_show='original')
        elif self.current_img_index == 0:
            self.current_img_index = len(self.filenames_img) - 1
            self.state_history = []
            self.state_index = -1
            self.show_images(self.current_img_index, mode_show='original')


    def swipe_right(self):
        if self.current_img_index < len(self.filenames_img) - 1:
            self.current_img_index += 1
            self.state_history = []
            self.state_index = -1
            self.show_images(self.current_img_index, mode_show='original')
        elif self.current_img_index == len(self.filenames_img) - 1:
            self.current_img_index = 0
            self.state_history = []
            self.state_index = -1
            self.show_images(self.current_img_index,mode_show='original')


    def start_selection(self, event):
        self.start_x = int(self.canvas.canvasx(event.x))
        self.start_y = int(self.canvas.canvasy(event.y))
        self.end_x = self.start_x
        self.end_y = self.start_y


    def update_selection(self, event):
        self.end_x = int(self.canvas.canvasx(event.x))
        self.end_y = int(self.canvas.canvasy(event.y))
        self.canvas.delete("rect")
        self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.end_x,
            self.end_y,
            outline="red",
            tags="rect",
            dash=(4, 4)
        )


    def delete_area(self, event):
        if self.mask_cv is None:
            self.mask_cv = cv2.imread(self.mask_path, 0)
        self.mask_cv[self.start_y:self.end_y, self.start_x:self.end_x] = 0
        self.save_state(self.mask_cv)
        self.mask = Image.fromarray(self.mask_cv)
        self.show_images(self.current_img_index, mode_show=None)


    def end_selection(self, event):
        print("Selection Coordinates: (x1={}, y1={}, x2={}, y2={})".format(self.start_x, self.start_y, self.end_x, self.end_y))


    def on_mouse_motion(self, event):
        x, y = event.x, event.y
        print(f"Cursor position: x={x}, y={y}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MaskEditorApp(root)
    root.mainloop()