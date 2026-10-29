import os
import subprocess
import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Snake AI Launcher")
        self.geometry("520x500")
        self.resizable(False, False)
        self.attributes("-alpha", 0.97)

        self.current_frame = None

        self.bg_image = ctk.CTkImage(
            light_image=Image.open("assets/menu_background.png"),
            dark_image=Image.open("assets/menu_background.png"),
            size=(520, 500)
        )

        self.bg_label = ctk.CTkLabel(
            self,
            image=self.bg_image,
            text=""
        )

        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_main_menu()

    def clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = ctk.CTkFrame(
            self,
            corner_radius=30,
            fg_color="#111111",
            border_width=2,
            border_color="#1e8449"
        )

        self.current_frame.pack(
            fill="both",
            expand=True,
            padx=60,
            pady=40
        )

    def game_button(self, parent, text, command=None, height=45):
        return ctk.CTkButton(
            parent,
            text=text,
            height=height,
            fg_color="#145a32",
            hover_color="#1e8449",
            font=("Consolas", 15, "bold"),
            command=command
        )

    def red_button(self, parent, text, command=None, height=40):
        return ctk.CTkButton(
            parent,
            text=text,
            height=height,
            fg_color="#8b1e1e",
            hover_color="#a83232",
            font=("Consolas", 15, "bold"),
            command=command
        )

    def gray_button(self, parent, text, command=None, height=38):
        return ctk.CTkButton(
            parent,
            text=text,
            height=height,
            fg_color="#444444",
            hover_color="#555555",
            font=("Consolas", 15, "bold"),
            command=command
        )

    def show_main_menu(self):
        self.clear_frame()

        title = ctk.CTkLabel(
            self.current_frame,
            text="SNAKE RL",
            font=("Consolas", 34, "bold"),
            text_color="#6dff8f"
        )

        title.pack(pady=(30, 5))

        subtitle = ctk.CTkLabel(
            self.current_frame,
            text="Deep Reinforcement Learning Environment",
            font=("Consolas", 13),
            text_color="#c7ffd4"
        )

        subtitle.pack(pady=(0, 25))

        self.game_button(
            self.current_frame,
            "Play Manual",
            self.show_play_menu
        ).pack(pady=10, padx=70, fill="x")

        self.game_button(
            self.current_frame,
            "Train Model",
            self.show_train_menu
        ).pack(pady=10, padx=70, fill="x")

        self.game_button(
            self.current_frame,
            "Test Model",
            self.show_test_menu
        ).pack(pady=10, padx=70, fill="x")

        self.red_button(
            self.current_frame,
            "Exit",
            self.destroy
        ).pack(pady=(30, 0), padx=70, fill="x")

    def show_play_menu(self):
        self.clear_frame()

        ctk.CTkLabel(
            self.current_frame,
            text="Play Manual",
            font=("Consolas", 26, "bold"),
            text_color="#6dff8f"
        ).pack(pady=(35, 25))

        ctk.CTkLabel(
            self.current_frame,
            text="Select Map",
            font=("Consolas", 14),
            text_color="#c7ffd4"
        ).pack(pady=(10, 5))

        map_choice = ctk.CTkOptionMenu(
            self.current_frame,
            values=["1", "2", "3", "4"],
            fg_color="#145a32",
            button_color="#1e8449",
            button_hover_color="#27ae60",
            font=("Consolas", 13)
        )

        map_choice.set("1")
        map_choice.pack(pady=10)

        self.game_button(
            self.current_frame,
            "Start",
            height=45,

            command=lambda:(
            self.destroy(),
            subprocess.Popen([
                "python",
                "environment.py",
                "--map",
                map_choice.get()
            ]))

        ).pack(pady=20, padx=80, fill="x")

        self.back_button()

    def show_train_menu(self):
        self.clear_frame()

        ctk.CTkLabel(
            self.current_frame,
            text="Train Model",
            font=("Consolas", 26, "bold"),
            text_color="#6dff8f"
        ).pack(pady=(15, 12))

        ctk.CTkLabel(
            self.current_frame,
            text="Select Map",
            font=("Consolas", 14),
            text_color="#c7ffd4"
        ).pack(pady=(5, 3))

        map_choice = ctk.CTkOptionMenu(
            self.current_frame,
            values=["1", "2", "3", "4"],
            fg_color="#145a32",
            button_color="#1e8449",
            button_hover_color="#27ae60",
            font=("Consolas", 13)
        )

        map_choice.set("1")
        map_choice.pack(pady=5)

        ctk.CTkLabel(
            self.current_frame,
            text="Training Algorithm",
            font=("Consolas", 14),
            text_color="#c7ffd4"
        ).pack(pady=(10, 3))

        exp_choice = ctk.CTkOptionMenu(
            self.current_frame,
            values=[
                "baseline",
                "double_dqn",
                "per_baseline",
                "per_double_dqn"
            ],
            fg_color="#145a32",
            button_color="#1e8449",
            button_hover_color="#27ae60",
            font=("Consolas", 13)
        )

        exp_choice.set("baseline")
        exp_choice.pack(pady=5)

        curriculum_var = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(
            self.current_frame,
            text="Use Curriculum Learning",
            variable=curriculum_var,
            fg_color="#145a32",
            hover_color="#1e8449",
            font=("Consolas", 13),
            text_color="#c7ffd4"
        ).pack(pady=8)

        self.game_button(
            self.current_frame,
            "Start Training",
            height=42,

            command=lambda:(
            self.destroy(),
            subprocess.Popen([
                "python",
                "train.py",
                "--exp",
                exp_choice.get(),
                "--map",
                map_choice.get()
            ]))

        ).pack(pady=12, padx=80, fill="x")

        self.back_button()

    def show_test_menu(self):
        self.clear_frame()

        ctk.CTkLabel(
            self.current_frame,
            text="Test Model",
            font=("Consolas", 26, "bold"),
            text_color="#6dff8f"
        ).pack(pady=(25, 20))

        ctk.CTkLabel(
            self.current_frame,
            text="Select Map",
            font=("Consolas", 14),
            text_color="#c7ffd4"
        ).pack(pady=(10, 5))

        map_choice = ctk.CTkOptionMenu(
            self.current_frame,
            values=["1", "2", "3", "4"],
            fg_color="#145a32",
            button_color="#1e8449",
            button_hover_color="#27ae60",
            font=("Consolas", 13)
        )

        map_choice.set("1")
        map_choice.pack(pady=10)

        ctk.CTkLabel(
            self.current_frame,
            text="Select Model",
            font=("Consolas", 14),
            text_color="#c7ffd4"
        ).pack(pady=(15, 5))

        models = self.get_models()

        model_choice = ctk.CTkOptionMenu(
            self.current_frame,
            values=models if models else ["No models found"],
            fg_color="#145a32",
            button_color="#1e8449",
            button_hover_color="#27ae60",
            font=("Consolas", 13)
        )

        if models:
            model_choice.set(models[0])

        model_choice.pack(pady=10)

        self.game_button(
            self.current_frame,
            "Start Test",
            height=45,

            command=lambda:(
            self.destroy(),
            subprocess.Popen([
                "python",
                os.path.abspath("test.py"),
                "--model",
                os.path.join("models", model_choice.get()),
                "--map",
                map_choice.get()
            ]))
        ).pack(pady=20, padx=80, fill="x")

        self.back_button()

    def back_button(self):
        self.gray_button(
            self.current_frame,
            "Back",
            self.show_main_menu
        ).pack(pady=10, padx=80, fill="x")

    def get_models(self):
        if not os.path.exists("models"):
            return []

        return [
            file for file in os.listdir("models")
            if file.endswith(".keras")
        ]


if __name__ == "__main__":
    app = Launcher()
    app.mainloop()