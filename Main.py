
# 프로그램명: 바이트 계산 패드
# 설명: 바이트 계산 기능이 있는 간단한 메모 프로그램
# 날짜: 2024. 8. 8.

# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox, font

class Notepad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cpad")
        self.geometry("600x400")

        self.opened_file_path = None  # 파일 경로를 저장할 변수
        self.is_modified = False  # 변경 사항 여부를 저장할 변수
        self.line_spacing = 4  # 기본 줄 간격

        # 기본 폰트 설정
        self.default_font = font.Font(family="Nanum Gothic", size=12)  # '나눔 고딕'을 기본 폰트로 설정
        self.status_font = font.Font(family="Nanum Gothic", size=12)  # 상태 표시줄의 기본 폰트 크기 설정

        # 기본 폰트를 인터페이스에 적용
        self.option_add("*Font", self.default_font)

        # 메인 프레임 생성
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 상태 표시줄 프레임
        self.status_frame = tk.Frame(self.main_frame)
        self.status_frame.pack(side=tk.TOP, fill=tk.X)

        # 상태 표시줄
        self.status_bar = tk.Label(self.status_frame, text="number of character: 0, byte: 0, modified: no", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=self.status_font)
        self.status_bar.pack(fill=tk.X)

        # 텍스트 영역과 스크롤바를 위한 프레임 생성
        self.text_frame = tk.Frame(self.main_frame)
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        # 텍스트 영역
        self.text_area = tk.Text(self.text_frame, undo=True, font=self.default_font, wrap=tk.WORD, spacing1=self.line_spacing, spacing2=self.line_spacing, spacing3=self.line_spacing)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 스크롤바 추가
        self.scrollbar = tk.Scrollbar(self.text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)

        # 텍스트 변경 이벤트 바인딩
        self.text_area.bind("<KeyRelease>", self.update_status_bar)
        self.text_area.bind("<<Modified>>", self.on_modified)

        # 메뉴바 설정
        self.setup_menu()
        # 단축키 바인딩
        self.bind_shortcuts()

    def setup_menu(self):
        # 메뉴바의 폰트를 지정함.
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # 파일 메뉴바의 폰트를 지정함.
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")  # 다른 이름으로 저장 기능 추가
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Close", command=self.quit, accelerator="Ctrl+Q")

        # 문자 변환 메뉴 항목 추가
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Convert to Smart Quotes", command=self.auto_replace, accelerator="Ctrl+T")
        self.edit_menu.add_command(label="Select All and Copy", command=self.select_all_and_copy, accelerator="Alt+C")

        # 폰트 메뉴 추가
        self.font_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Font", menu=self.font_menu)
        self.font_menu.add_command(label="Increase Font Size", command=self.increase_font_size, accelerator="Ctrl+Up")
        self.font_menu.add_command(label="Decrease Font Size", command=self.decrease_font_size, accelerator="Ctrl+Down")
        self.font_menu.add_command(label="Increase Status Font Size", command=self.increase_status_font_size, accelerator="Ctrl+Right")
        self.font_menu.add_command(label="Decrease Status Font Size", command=self.decrease_status_font_size, accelerator="Ctrl+Left")
        self.font_menu.add_command(label="Increase Line Spacing", command=self.increase_line_spacing, accelerator="Alt+Up")
        self.font_menu.add_command(label="Decrease Line Spacing", command=self.decrease_line_spacing, accelerator="Alt+Down")

    def bind_shortcuts(self):
        self.bind("<Control-o>", lambda event: self.open_file())
        self.bind("<Control-s>", lambda event: self.save_file())
        self.bind("<Control-S>", lambda event: self.save_as_file())
        self.bind("<Control-q>", lambda event: self.quit())
        self.bind("<Control-t>", lambda event: self.auto_replace())
        self.bind("<Alt-c>", lambda event: self.select_all_and_copy())
        self.bind("<Control-Up>", lambda event: self.increase_font_size())
        self.bind("<Control-Down>", lambda event: self.decrease_font_size())
        self.bind("<Control-Right>", lambda event: self.increase_status_font_size())
        self.bind("<Control-Left>", lambda event: self.decrease_status_font_size())
        self.bind("<Alt-Up>", lambda event: self.increase_line_spacing())
        self.bind("<Alt-Down>", lambda event: self.decrease_line_spacing())

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                    self.opened_file_path = file_path
                    self.is_modified = False
                    self.update_status_bar()
                    self.text_area.edit_modified(False)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")

    def save_file(self):
        if self.opened_file_path:
            try:
                with open(self.opened_file_path, "w", encoding="utf-8") as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                    messagebox.showinfo("Save", "The file has been saved")
                    self.is_modified = False
                    self.update_status_bar()
                    self.text_area.edit_modified(False)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension="txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                    messagebox.showinfo("Save", "The file has been saved")
                    self.opened_file_path = file_path
                    self.is_modified = False
                    self.update_status_bar()
                    self.text_area.edit_modified(False)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def update_status_bar(self, event=None):
        text_content = self.text_area.get(1.0, tk.END)
        char_count = len(text_content) - 1  # 마지막의 '\n'을 제외
        byte_count = sum(1 if ord(char) < 128 else len(char.encode('utf-8')) for char in text_content[:-1])  # 마지막의 '\n'을 제외
        modified_text = "yes" if self.is_modified else "no"
        self.status_bar.config(text=f"number of character: {char_count}, byte: {byte_count}, modified: {modified_text}")

    def on_modified(self, event=None):
        if self.text_area.edit_modified():
            self.is_modified = True
            self.update_status_bar()
            self.text_area.edit_modified(False)

    def auto_replace(self, event=None):
        # 1. 커서 위치 저장
        cursor_pos = self.text_area.index(tk.INSERT)

        # 2. 텍스트 전체를 trailing newline 제외한 형태로 가져오기
        text_content = self.text_area.get("1.0", "end-1c")

        # 3. 스마트/커스티 따옴표 → ASCII 따옴표 변환
        replacements = {
            "‘": "'", "’": "'",
            "“": '"', "”": '"',
            "´": "'", "˝": '"'
        }
        for old, new in replacements.items():
            text_content = text_content.replace(old, new)

        # 4. 원본과 같은 범위만 지우고 새로 삽입
        self.text_area.delete("1.0", "end-1c")
        self.text_area.insert("1.0", text_content)

        # 5. 커서 복원, 수정 플래그 및 상태표시줄 갱신
        self.text_area.mark_set(tk.INSERT, cursor_pos)
        self.is_modified = True
        self.update_status_bar()

    def increase_font_size(self):
        current_size = self.default_font['size']
        new_size = current_size + 2
        self.default_font.configure(size=new_size)
        self.text_area.configure(font=self.default_font)
        self.update_status_bar()

    def decrease_font_size(self):
        current_size = self.default_font['size']
        new_size = max(8, current_size - 2)  # 최소 크기를 8로 제한
        self.default_font.configure(size=new_size)
        self.text_area.configure(font=self.default_font)
        self.update_status_bar()

    def increase_status_font_size(self):
        current_size = self.status_font['size']
        new_size = current_size + 2
        self.status_font.configure(size=new_size)
        self.status_bar.configure(font=self.status_font)
        self.update_status_bar()

    def decrease_status_font_size(self):
        current_size = self.status_font['size']
        new_size = max(8, current_size - 2)  # 최소 크기를 8로 제한
        self.status_font.configure(size=new_size)
        self.status_bar.configure(font=self.status_font)
        self.update_status_bar()

    def increase_line_spacing(self):
        self.line_spacing += 2
        self.text_area.configure(spacing1=self.line_spacing, spacing2=self.line_spacing, spacing3=self.line_spacing)

    def decrease_line_spacing(self):
        self.line_spacing = max(0, self.line_spacing - 2)
        self.text_area.configure(spacing1=self.line_spacing, spacing2=self.line_spacing, spacing3=self.line_spacing)

    def select_all_and_copy(self):
        self.text_area.tag_add('sel', '1.0', 'end')
        self.clipboard_clear()
        text = self.text_area.get('1.0', 'end')
        self.clipboard_append(text)
        messagebox.showinfo("Copy", "Text has been copied to clipboard")

if __name__ == "__main__":
    app = Notepad()
    app.mainloop()