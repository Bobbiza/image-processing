import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import math

# ==================================================
# 1. COLORS - CATPPUCCIN MOCHA
# ==================================================

BG = "#1e1e2e"
PANEL = "#181825"
BTN = "#313244"
TEXT = "#cdd6f4"
ACCENT = "#cba6f7"
PINK = "#f5c2e7"
PEACH = "#fab387"
GREEN = "#a6e3a1"
MUTED = "#a6adc8"

# ==================================================
# 2. VARIABLES
# ==================================================

original_image = None
current_image = None
image_photo = None

matrix_entries = []

# ==================================================
# 3. MAIN WINDOW
# ==================================================

root = tk.Tk()
root.title("Linear Algebra - Image Processor")
root.geometry("1350x850")
root.minsize(1100, 750)
root.configure(bg=BG)

# ==================================================
# 4. MAIN LAYOUT
# ==================================================

sidebar = tk.Frame(root, bg=BG, width=390)
sidebar.pack(side="left", fill="y", padx=15, pady=15)
sidebar.pack_propagate(False)

workspace = tk.Frame(root, bg=PANEL)
workspace.pack(side="right", fill="both", expand=True,
               padx=(0, 15), pady=15)

# ==================================================
# 5. TITLE
# ==================================================

tk.Label(
    sidebar,
    text="LINEAR ALGEBRA",
    font=("Arial", 20, "bold"),
    bg=BG,
    fg=ACCENT
).pack(anchor="w")

tk.Label(
    sidebar,
    text="IMAGE PROCESSING PROJECT",
    font=("Arial", 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(3, 15))

# ==================================================
# 6. HELPER FUNCTIONS
# ==================================================

def make_button(parent, text, command, color=TEXT):

    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 11, "bold"),
        bg=BTN,
        fg=color,
        activebackground=ACCENT,
        activeforeground=BG,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=5,
        pady=8
    )


def set_output(text):

    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, text)
    output_box.config(state="disabled")


# ==================================================
# 7. IMAGE PREVIEW
# ==================================================

preview_label = tk.Label(
    workspace,
    text="UPLOAD AN IMAGE TO START",
    font=("Arial", 22, "bold"),
    bg=PANEL,
    fg=MUTED
)

preview_label.pack(fill="both", expand=True, padx=15, pady=15)


def show_image(img):

    global image_photo

    preview = img.copy()

    preview.thumbnail((900, 760))

    image_photo = ImageTk.PhotoImage(preview)

    preview_label.config(
        image=image_photo,
        text=""
    )

    preview_label.image = image_photo


# ==================================================
# 8. IMAGE VALIDATION
# ==================================================

def has_image():

    if current_image is None:

        messagebox.showwarning(
            "Warning",
            "Please upload an image first."
        )

        return False

    return True


# ==================================================
# 9. OPEN IMAGE
# ==================================================

def open_image():

    global original_image, current_image

    path = filedialog.askopenfilename(
        filetypes=[
            ("Image Files",
             "*.png *.jpg *.jpeg *.bmp *.webp")
        ]
    )

    if not path:
        return

    try:

        original_image = Image.open(path).convert("RGB")
        current_image = original_image.copy()

        show_image(current_image)

        set_output(
            "IMAGE LOADED\n\n"
            f"Width: {current_image.width}\n"
            f"Height: {current_image.height}\n"
            f"Pixels: {current_image.width * current_image.height}\n\n"
            "RGB Color Space"
        )

    except Exception as error:

        messagebox.showerror("Image Error", str(error))


# ==================================================
# 10. BASIC IMAGE OPERATIONS
# ==================================================

def grayscale():

    global current_image

    if not has_image():
        return

    current_image = current_image.convert("L")

    show_image(current_image)

    set_output("GRAYSCALE TRANSFORMATION\n\nRGB -> Grayscale")


def black_white():

    global current_image

    if not has_image():
        return

    gray = current_image.convert("L")

    current_image = gray.point(
        lambda p: 255 if p > 128 else 0
    )

    show_image(current_image)

    set_output(
        "BINARY IMAGE TRANSFORMATION\n\n"
        "If Pixel > 128: White (255)\n"
        "Otherwise: Black (0)"
    )


def flip_horizontal():

    global current_image

    if not has_image():
        return

    current_image = ImageOps.mirror(current_image)

    show_image(current_image)

    set_output("HORIZONTAL REFLECTION")


def reset_image():

    global current_image

    if original_image is None:
        return

    current_image = original_image.copy()

    show_image(current_image)

    set_output("IMAGE RESTORED TO ORIGINAL")


def save_image():

    if not has_image():
        return

    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG", "*.png"),
            ("JPEG", "*.jpg"),
            ("BMP", "*.bmp")
        ]
    )

    if path:

        try:

            current_image.save(path)

            messagebox.showinfo(
                "Success",
                "Image saved successfully!"
            )

        except Exception as error:

            messagebox.showerror("Save Error", str(error))


# ==================================================
# 11. MATRIX EDITOR
# ==================================================

matrix_frame = tk.LabelFrame(
    sidebar,
    text="  MATRIX A (3 x 3)  ",
    font=("Arial", 12, "bold"),
    bg=BG,
    fg=ACCENT,
    bd=1
)

matrix_frame.pack(fill="x", pady=10)


# Create 3x3 editable matrix

for row in range(3):

    row_entries = []

    for col in range(3):

        entry = tk.Entry(
            matrix_frame,
            width=9,
            justify="center",
            font=("Arial", 13, "bold"),
            bg=BTN,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat"
        )

        entry.grid(
            row=row,
            column=col,
            padx=7,
            pady=7,
            ipady=5
        )

        # Identity Matrix as default

        entry.insert(
            0,
            "1" if row == col else "0"
        )

        row_entries.append(entry)

    matrix_entries.append(row_entries)


# ==================================================
# 12. READ MATRIX
# ==================================================

def get_matrix():

    matrix = []

    for row in matrix_entries:

        matrix_row = []

        for entry in row:

            value = float(entry.get())

            if not math.isfinite(value):
                raise ValueError("Numbers must be finite.")

            matrix_row.append(value)

        matrix.append(matrix_row)

    return matrix


# ==================================================
# 13. DISPLAY MATRIX
# ==================================================

def format_matrix(matrix):

    return "\n".join(
        "[ " + "   ".join(f"{value:8.3f}" for value in row) + " ]"
        for row in matrix
    )


def update_matrix_entries(matrix):

    for i in range(3):

        for j in range(3):

            entry = matrix_entries[i][j]

            entry.delete(0, tk.END)
            entry.insert(0, str(matrix[i][j]))


# ==================================================
# 14. MATRIX IDENTITY
# ==================================================

def identity_matrix():

    matrix = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

    update_matrix_entries(matrix)

    set_output(
        "IDENTITY MATRIX\n\n"
        + format_matrix(matrix)
        + "\n\nA x I = A"
    )


# ==================================================
# 15. MATRIX DETERMINANT
# ==================================================

def determinant():

    try:

        A = get_matrix()

        det = (
            A[0][0] * (
                A[1][1] * A[2][2] -
                A[1][2] * A[2][1]
            )
            -
            A[0][1] * (
                A[1][0] * A[2][2] -
                A[1][2] * A[2][0]
            )
            +
            A[0][2] * (
                A[1][0] * A[2][1] -
                A[1][1] * A[2][0]
            )
        )

        set_output(
            "DETERMINANT OF MATRIX A\n\n"
            + format_matrix(A)
            + f"\n\nDet(A) = {det:.4f}"
            + (
                "\n\nMatrix is invertible."
                if not math.isclose(det, 0, abs_tol=1e-10)
                else "\n\nMatrix is singular (not invertible)."
            )
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Matrix",
            "Enter valid numbers in all cells."
        )


# ==================================================
# 16. MATRIX TRANSPOSE
# ==================================================

def transpose():

    try:

        A = get_matrix()

        result = [
            [A[j][i] for j in range(3)]
            for i in range(3)
        ]

        update_matrix_entries(result)

        set_output(
            "MATRIX TRANSPOSE\n\n"
            "A^T =\n\n"
            + format_matrix(result)
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Matrix",
            "Enter valid numbers."
        )


# ==================================================
# 17. MATRIX MULTIPLICATION
# ==================================================

def multiply_matrices():

    try:

        A = get_matrix()

        # Create a second matrix B

        window = tk.Toplevel(root)
        window.title("Matrix B")
        window.geometry("330x300")
        window.configure(bg=BG)
        window.transient(root)

        tk.Label(
            window,
            text="ENTER MATRIX B",
            font=("Arial", 14, "bold"),
            bg=BG,
            fg=ACCENT
        ).pack(pady=10)

        entries_B = []

        frame_B = tk.Frame(window, bg=BG)
        frame_B.pack()

        for i in range(3):

            row_entries = []

            for j in range(3):

                entry = tk.Entry(
                    frame_B,
                    width=8,
                    justify="center",
                    font=("Arial", 12),
                    bg=BTN,
                    fg=TEXT,
                    insertbackground=TEXT
                )

                entry.grid(row=i, column=j, padx=5, pady=5)

                entry.insert(
                    0,
                    "1" if i == j else "0"
                )

                row_entries.append(entry)

            entries_B.append(row_entries)

        def calculate():

            try:

                B = [
                    [float(entries_B[i][j].get())
                     for j in range(3)]
                    for i in range(3)
                ]

                if not all(
                    math.isfinite(x)
                    for row in B for x in row
                ):
                    raise ValueError

                # Matrix multiplication A x B

                result = [
                    [
                        sum(
                            A[i][k] * B[k][j]
                            for k in range(3)
                        )
                        for j in range(3)
                    ]
                    for i in range(3)
                ]

                update_matrix_entries(result)

                set_output(
                    "MATRIX MULTIPLICATION\n\n"
                    "A =\n" + format_matrix(A)
                    + "\n\nB =\n" + format_matrix(B)
                    + "\n\nA x B =\n" + format_matrix(result)
                )

                window.destroy()

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Enter valid finite numbers."
                )

        make_button(
            window,
            "Calculate A x B",
            calculate,
            GREEN
        ).pack(fill="x", padx=20, pady=15)

    except ValueError:

        messagebox.showerror(
            "Invalid Matrix",
            "Enter valid numbers in Matrix A."
        )


# ==================================================
# 18. APPLY MATRIX TO IMAGE
# ==================================================

def apply_matrix():

    global current_image

    if not has_image():
        return

    try:

        A = get_matrix()

        # Pillow uses 12 coefficients:
        # 9 matrix values + 3 offsets

        coefficients = (
            A[0][0], A[0][1], A[0][2], 0,
            A[1][0], A[1][1], A[1][2], 0,
            A[2][0], A[2][1], A[2][2], 0
        )

        current_image = current_image.convert("RGB").convert(
            "RGB",
            coefficients
        )

        show_image(current_image)

        set_output(
            "LINEAR TRANSFORMATION APPLIED\n\n"
            "P' = A x P\n\n"
            "Matrix A:\n"
            + format_matrix(A)
            + "\n\n"
            "R' = aR + bG + cB\n"
            "G' = dR + eG + fB\n"
            "B' = gR + hG + iB\n\n"
            "Pixel values are clipped to [0, 255]."
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Matrix",
            "Enter valid numbers in all 9 cells."
        )


# ==================================================
# 19. MATRIX PRESETS
# ==================================================

def set_warm():

    matrix = [
        [1.08, 0.05, 0.00],
        [0.00, 1.00, 0.02],
        [0.00, 0.00, 0.90]
    ]

    update_matrix_entries(matrix)

    set_output("WARM COLOR MATRIX\n\n" + format_matrix(matrix))


def set_cool():

    matrix = [
        [0.90, 0.00, 0.00],
        [0.00, 1.00, 0.02],
        [0.00, 0.05, 1.10]
    ]

    update_matrix_entries(matrix)

    set_output("COOL COLOR MATRIX\n\n" + format_matrix(matrix))


def set_sepia():

    matrix = [
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ]

    update_matrix_entries(matrix)

    set_output("SEPIA MATRIX\n\n" + format_matrix(matrix))


# ==================================================
# 20. BUTTONS - IMAGE OPERATIONS
# ==================================================

image_frame = tk.LabelFrame(
    sidebar,
    text="  IMAGE OPERATIONS  ",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=PEACH
)

image_frame.pack(fill="x", pady=5)

image_buttons = [
    ("Open Image", open_image),
    ("Grayscale", grayscale),
    ("Black & White", black_white),
    ("Flip Horizontal", flip_horizontal),
    ("Reset Image", reset_image),
    ("Save Image", save_image)
]

for i, (name, command) in enumerate(image_buttons):

    make_button(
        image_frame,
        name,
        command
    ).grid(
        row=i // 2,
        column=i % 2,
        padx=4,
        pady=4,
        sticky="ew"
    )

image_frame.columnconfigure(0, weight=1)
image_frame.columnconfigure(1, weight=1)


# ==================================================
# 21. BUTTONS - MATRIX OPERATIONS
# ==================================================

matrix_operations = tk.LabelFrame(
    sidebar,
    text="  MATRIX OPERATIONS  ",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=PINK
)

matrix_operations.pack(fill="x", pady=7)

operations = [
    ("Apply Matrix", apply_matrix, GREEN),
    ("Determinant", determinant, ACCENT),
    ("Transpose", transpose, TEXT),
    ("Multiply A x B", multiply_matrices, PEACH),
    ("Identity Matrix", identity_matrix, ACCENT)
]

for i, (name, command, color) in enumerate(operations):

    make_button(
        matrix_operations,
        name,
        command,
        color
    ).grid(
        row=i // 2,
        column=i % 2,
        padx=4,
        pady=4,
        sticky="ew"
    )

matrix_operations.columnconfigure(0, weight=1)
matrix_operations.columnconfigure(1, weight=1)


# ==================================================
# 22. MATRIX PRESETS
# ==================================================

preset_frame = tk.Frame(sidebar, bg=BG)
preset_frame.pack(fill="x", pady=5)

tk.Label(
    preset_frame,
    text="COLOR MATRIX PRESETS",
    bg=BG,
    fg=MUTED,
    font=("Arial", 9, "bold")
).pack(anchor="w")

preset_buttons = tk.Frame(preset_frame, bg=BG)
preset_buttons.pack(fill="x", pady=5)

make_button(
    preset_buttons, "Warm", set_warm, PEACH
).pack(side="left", expand=True, fill="x", padx=2)

make_button(
    preset_buttons, "Cool", set_cool, ACCENT
).pack(side="left", expand=True, fill="x", padx=2)

make_button(
    preset_buttons, "Sepia", set_sepia, PINK
).pack(side="left", expand=True, fill="x", padx=2)


# ==================================================
# 23. MATHEMATICAL OUTPUT
# ==================================================

output_frame = tk.LabelFrame(
    sidebar,
    text="  MATHEMATICAL RESULTS  ",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=GREEN
)

output_frame.pack(fill="both", expand=True, pady=7)

output_box = tk.Text(
    output_frame,
    height=8,
    bg=PANEL,
    fg=TEXT,
    font=("Courier New", 9),
    relief="flat",
    wrap="word",
    padx=8,
    pady=8
)

output_box.pack(fill="both", expand=True)

output_box.insert(
    tk.END,
    "Welcome to Linear Algebra Image Processor.\n\n"
    "Edit Matrix A and explore mathematical operations."
)

output_box.config(state="disabled")


# ==================================================
# 24. START APPLICATION
# ==================================================

root.mainloop()
