from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps

# ===== الألوان =====
BG       = '#1e1e2e'
PANEL    = '#11111b'
BTN      = '#313244'
BTN_TEXT = '#cdd6f4'
ACCENT   = '#89b4fa'
MUTED    = '#6c7086'

# ===== متغيرات الصورة =====
original_image = None   
current_image = None    

root = Tk()
root.title("project liner ")
root.geometry("1100x700")
root.minsize(850, 550)
root.configure(background=BG)

title_label = Label(root, text="image processing", font=("Arial", 16, "bold"),
                    bg=BG, fg=ACCENT)
title_label.place(x=20, y=20, width=240, height=40)

preview_label = Label(root, text="upload image", font=("Arial", 20, "bold"),
                      bg=PANEL, fg=MUTED,
                      highlightbackground=ACCENT, highlightthickness=2)
preview_label.place(x=300, y=20, width=760, height=640)


def make_button(text, y, command=None):
    b = Button(root, text=text, font=("Arial", 16, "bold"),
               bg=BTN, fg=BTN_TEXT,
               activebackground=ACCENT, activeforeground=PANEL,
               highlightbackground=ACCENT, highlightthickness=2,
               relief=FLAT, bd=0, cursor="hand2",
               command=command)
    b.place(x=20, y=y, width=240, height=60)
    return b


def show_image(img):
    """بتعرض أي صورة في مكان العرض"""
    preview = img.copy()
    preview.thumbnail((750, 630))
    photo = ImageTk.PhotoImage(preview)
    preview_label.config(image=photo, text="")
    preview_label.image = photo


def has_image():
    """بتتأكد إن فيه صورة مفتوحة قبل أي تعديل"""
    if current_image is None:
        messagebox.showwarning("تنبيه", "افتح صورة الأول")
        return False
    return True


def open_image():
    global original_image, current_image
    file_path = filedialog.askopenfilename(
        filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif *.webp")])
    if file_path:
        original_image = Image.open(file_path).convert("RGB")
        current_image = original_image.copy()
        show_image(current_image)


def to_gray():
    global current_image
    if not has_image():
        return
    current_image = current_image.convert("L")
    show_image(current_image)


def to_bw():
    global current_image
    if not has_image():
        return
    gray = current_image.convert("L")
    current_image = gray.point(lambda p: 255 if p > 128 else 0)
    show_image(current_image)


def flip_h():
    global current_image
    if not has_image():
        return
    current_image = ImageOps.mirror(current_image)
    show_image(current_image)


def reset_image():
    global current_image
    if not has_image():
        return
    current_image = original_image.copy()
    show_image(current_image)


def save_image():
    if not has_image():
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")])
    if file_path:
        current_image.save(file_path)
        messagebox.showinfo("تم", "الصورة اتحفظت")


b1 = make_button('open image', 80, open_image)
b2 = make_button('grayscale', 160, to_gray)
b3 = make_button('black & white', 240, to_bw)
b4 = make_button('flip horizontal', 320, flip_h)
b5 = make_button('reset', 400, reset_image)
b6 = make_button('save image', 480, save_image)
