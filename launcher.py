import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import subprocess
import threading
import time
import os
import socket
import sys
import json
import ctypes
from supabase import create_client, Client

SUPABASE_URL = "supabase_url"
SUPABASE_KEY = "supabase_key"
BUCKET_NAME = "game-saves"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Error creating Supabase client: {e}")

class GTALauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Rockstar Games Services")
        
        window_width, window_height = 500, 400
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        center_x, center_y = int(screen_width / 2 - window_width / 2), int(screen_height / 2 - window_height / 2)
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.configure(bg="#000000")
        self.root.overrideredirect(True) 
        self.root.attributes('-alpha', 0.0)
        
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)
        self.offset_x, self.offset_y = 0, 0

        if getattr(sys, 'frozen', False):
            self.game_dir = os.path.dirname(sys.executable)
        else:
            self.game_dir = os.path.dirname(os.path.abspath(__file__))

        try:
            self.resource_dir = sys._MEIPASS
        except AttributeError:
            self.resource_dir = self.game_dir

        self.video_path = os.path.join(self.resource_dir, "media", "rockstar-logo.mp4")
        self.game_exe_path = os.path.join(self.game_dir, "gta_sa.exe")
        self.save_dir = os.path.join(self.game_dir, "userfiles")
        
        self.data_dir = os.path.join(self.game_dir, "data", "launcher")
        self.config_file = os.path.join(self.data_dir, "config.json")
        
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.save_dir, exist_ok=True)

        self.mutex_name = "GTASA_Launcher_Mutex"
        self.mutex_handle = ctypes.windll.kernel32.CreateMutexW(None, False, self.mutex_name)

        self.config = self.load_config()
        self.has_saved_data = bool(self.config.get("username") and self.config.get("password"))
        
        self.is_game_running = False
        self.current_user = None
        self.video_cap = None
        self.video_running = True
        
        threading.Thread(target=self.create_desktop_shortcut, daemon=True).start()
        
        self.setup_ui()
        self.check_files()
        self.fade_in()
        
        self.root.after(100, self.check_first_time)
        self.start_video_thread()

    def create_desktop_shortcut(self):
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_name = "Grand Theft Auto San Andreas.lnk" 
            shortcut_path = os.path.join(desktop, shortcut_name)
            
            icon_path = os.path.join(self.game_dir, "data", "Icons", "icon.ico")
            if not os.path.exists(icon_path):
                icon_path = self.game_exe_path

            if getattr(sys, 'frozen', False):
                launcher_exe = sys.executable
            else:
                launcher_exe = os.path.abspath(sys.argv[0])

            ps_script = f'''
            $WScriptShell = New-Object -ComObject WScript.Shell
            $Shortcut = $WScriptShell.CreateShortcut("{shortcut_path}")
            $Shortcut.TargetPath = "{launcher_exe}"
            $Shortcut.WorkingDirectory = "{self.game_dir}"
            $Shortcut.IconLocation = "{icon_path}"
            $Shortcut.Save()
            '''
            subprocess.run(["powershell", "-WindowStyle", "Hidden", "-Command", ps_script], check=True, capture_output=True)
        except Exception as e:
            print(f"Note: Could not create desktop shortcut: {e}")

    def load_config(self):
        default_config = {
            "username": "", "password": "", "welcome_shown": False,
            "playtime": 0, "sync_state": {}
        }
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    saved = json.load(f)
                    if "email" in saved and "username" not in saved:
                        saved["username"] = saved.pop("email")
                    default_config.update(saved)
            except Exception as e: 
                print(f"Error loading config: {e}")
        return default_config

    def save_config(self):
        if hasattr(self, 'name_entry'):
            self.config["username"] = self.name_entry.get().strip()
            self.config["password"] = self.pass_entry.get().strip()
        try:
            with open(self.config_file, "w") as f: 
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def fade_in(self):
        alpha = self.root.attributes('-alpha')
        if alpha < 0.96:
            alpha += 0.05
            self.root.attributes('-alpha', alpha)
            self.root.after(15, self.fade_in)

    def start_move(self, event):
        self.offset_x, self.offset_y = event.x, event.y

    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.offset_x)
        y = self.root.winfo_y() + (event.y - self.offset_y)
        self.root.geometry(f"+{x}+{y}")

    def setup_ui(self):
        self.close_btn = tk.Button(self.root, text="✕", bg="#000000", fg="#555555", 
                                   font=("Segoe UI", 12), bd=0, 
                                   activebackground="#000000", activeforeground="#FFFFFF", 
                                   command=self.on_closing, cursor="hand2")
        self.close_btn.place(relx=0.97, rely=0.04, anchor="ne")

        self.video_label = tk.Label(self.root, bg="#000000", bd=0)
        self.video_label.place(relx=0.5, rely=0.3, anchor="center")

        self.status_label = tk.Label(self.root, text="", bg="#000000", fg="#E0E0E0", font=("Segoe UI", 9))
        self.status_label.place(relx=0.5, rely=0.65, anchor="center")

        self.time_label = tk.Label(self.root, text=self.format_time(self.config["playtime"]), 
                                   bg="#000000", fg="#444444", font=("Segoe UI", 8))
        self.time_label.place(relx=0.97, rely=0.96, anchor="se")

        if not self.has_saved_data:
            self.user_frame = tk.Frame(self.root, bg="#000000")
            self.user_frame.place(relx=0.5, rely=0.55, anchor="center")
            
            tk.Label(self.user_frame, text="Nombre:", bg="#000000", fg="#888888", font=("Segoe UI", 9)).pack(side="left", padx=2)
            self.name_entry = tk.Entry(self.user_frame, bg="#111111", fg="#FFFFFF", insertbackground="white",
                                       font=("Segoe UI", 9), bd=0, highlightthickness=1, highlightbackground="#333333", width=14)
            self.name_entry.pack(side="left", padx=2, ipadx=5, ipady=3)
            
            tk.Label(self.user_frame, text="Contraseña:", bg="#000000", fg="#888888", font=("Segoe UI", 9)).pack(side="left", padx=2)
            self.pass_entry = tk.Entry(self.user_frame, bg="#111111", fg="#FFFFFF", insertbackground="white",
                                       font=("Segoe UI", 9), bd=0, highlightthickness=1, highlightbackground="#333333", show="*", width=12)
            self.pass_entry.pack(side="left", padx=2, ipadx=5, ipady=3)

            self.btn_play = tk.Button(self.root, text="Jugar", bg="#FFFFFF", fg="#000000", 
                                      font=("Segoe UI", 10, "bold"), bd=0, activebackground="#CCCCCC", 
                                      command=self.on_play_clicked, cursor="hand2")
            self.btn_play.place(relx=0.5, rely=0.78, anchor="center", width=150, height=35)
        else:
            self.status_label.config(text="Iniciando sesión automáticamente...", fg="#E0E0E0")

    def check_first_time(self):
        if not self.config.get("welcome_shown", False):
            self.show_welcome_message()
        else:
            self.check_auto_start()

    def check_auto_start(self):
        if self.has_saved_data:
            self.root.after(1500, self.on_play_clicked)
        else:
            self.status_label.config(text="Ingresa tu nombre y contraseña", fg="#E0E0E0")

    def show_welcome_message(self):
        text = ("Hola soy Angely, la que hizo este gta re trucho,\n\n"
                "como podras ver este launcher lo hize porque si we no mames\n"
                "es para añadir guardado en la nube y recuperar esa funcion\n"
                "lo hize con supabase y quedo, por ahora esta bien y bueno nose\n"
                "nomas pon un nombre y una clave bro y listo wuachin mas nada\n"
                "si quieren que mejore algo o nose lo tiran por el dc de agustina\n\n"
                "si eres agustina y estas leyendo esto apaga stream boba\n"
                "igual con jovi desmutea loco")
        
        messagebox.showinfo("Bienvenido", text)
        self.config["welcome_shown"] = True
        self.save_config()
        self.check_auto_start()

    def start_video_thread(self):
        if os.path.exists(self.video_path):
            self.video_cap = cv2.VideoCapture(self.video_path)
            threading.Thread(target=self.video_loop, daemon=True).start()
        else:
            self.video_label.config(text="R ✦", font=("Segoe UI", 48, "bold"), fg="#222222")
            print("[WARNING] Video file not found in media folder.")

    def video_loop(self):
        while self.video_running and self.video_cap.isOpened():
            ret, frame = self.video_cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (250, 140)) 
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.root.after(0, self.update_video_ui, imgtk)
                time.sleep(0.033)
            else:
                self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                time.sleep(0.1)

    def update_video_ui(self, imgtk):
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

    def on_play_clicked(self):
        if hasattr(self, 'btn_play'):
            self.btn_play.config(state="disabled", text="Iniciando...")
        
        self.config["username"] = self.name_entry.get().strip() if hasattr(self, 'name_entry') else self.config["username"]
        self.config["password"] = self.pass_entry.get().strip() if hasattr(self, 'pass_entry') else self.config["password"]
        self.save_config() 
        
        threading.Thread(target=self.process_network_and_saves, daemon=True).start()

    def process_network_and_saves(self):
        self.update_status("Conectando con los Servicios de Juego...", "#E0E0E0")
        
        if self.check_internet():
            time.sleep(0.5)
            username = self.config["username"]
            password = self.config["password"]
            
            if username and password:
                self.update_status("Autenticando...", "#E0E0E0")
                auth_success = self.authenticate(username, password)
                
                if auth_success:
                    self.update_status("Buscando partidas en la Nube...", "#E0E0E0")
                    self.auto_download_saves()
                    
                    self.update_status("Sincronizando partidas locales...", "#E0E0E0")
                    self.auto_upload_saves()
                else:
                    self.update_status("Error de sesión. Iniciando offline...", "#FF5555")
                    time.sleep(1.5)
            else:
                self.update_status("Sin datos. Iniciando offline...", "#FFAA00")
                time.sleep(1)
        else:
            self.update_status("Conexión Fallida... Iniciando offline", "#FF5555")
            time.sleep(1)

        self.update_status("Iniciando GTA San Andreas...", "#55FF55")
        time.sleep(1)
        self.launch_game()

    def update_status(self, text, color):
        self.root.after(0, lambda: self.status_label.config(text=text, fg=color))

    def authenticate(self, username, password):
        fake_email = f"{username.replace(' ', '_')}@gta.local"
        
        try:
            res = supabase.auth.sign_in_with_password({"email": fake_email, "password": password})
            self.current_user = res.user
            return True
        except Exception as e_login:
            print(f"Login failed, trying to register: {e_login}")
            try:
                res = supabase.auth.sign_up({"email": fake_email, "password": password})
                self.current_user = res.user
                if res.session is None:
                    print("[WARNING] User created but session is None. Check 'Confirm email' setting in Supabase.")
                    self.root.after(0, lambda: messagebox.showwarning("Aviso", "Desactiva 'Confirm email' en Supabase para que el launcher funcione."))
                    return False
                return True
            except Exception as e_register:
                print(f"Registration failed: {e_register}")
                if "Invalid login credentials" in str(e_login):
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Contraseña incorrecta para '{username}'."))
                return False

    def auto_download_saves(self):
        if not self.current_user: return

        descargados = []
        for i in range(1, 9):
            file_name = f"GTASAsf{i}.b"
            local_path = os.path.join(self.save_dir, file_name)

            if not os.path.exists(local_path):
                cloud_path = f"{self.current_user.id}/{file_name}"
                try:
                    data = supabase.storage.from_(BUCKET_NAME).download(cloud_path)
                    with open(local_path, "wb") as f:
                        f.write(data)
                    descargados.append(str(i))
                    
                    self.config["sync_state"][file_name] = os.path.getmtime(local_path)
                    self.save_config()
                except Exception:
                    pass 

        if descargados:
            msj = f"Se descargaron las partidas: {', '.join(descargados)}"
            self.update_status(msj, "#00BFFF")
            time.sleep(2.5)

    def auto_upload_saves(self):
        if not self.current_user: return

        subidos = []
        for i in range(1, 9):
            file_name = f"GTASAsf{i}.b"
            local_path = os.path.join(self.save_dir, file_name)
            
            if os.path.exists(local_path):
                local_mtime = os.path.getmtime(local_path)
                last_uploaded = self.config["sync_state"].get(file_name, 0)

                if local_mtime > last_uploaded:
                    try:
                        cloud_path = f"{self.current_user.id}/{file_name}"
                        with open(local_path, "rb") as f:
                            supabase.storage.from_(BUCKET_NAME).upload(
                                path=cloud_path, file=f,
                                file_options={"content-type": "application/octet-stream", "upsert": "true"}
                            )
                        
                        self.config["sync_state"][file_name] = local_mtime
                        self.save_config() 
                        subidos.append(str(i))
                    except Exception as e:
                        print(f"Error uploading {file_name}: {e}")

        if subidos:
            msj = f"Se subieron las partidas: {', '.join(subidos)}"
            self.update_status(msj, "#55FF55")
            time.sleep(2.5)

    def check_files(self):
        if not os.path.exists(self.game_exe_path):
            print(f"Critical Error: gta_sa.exe not found in {self.game_dir}")
            messagebox.showerror("Error Crítico", f"Falta gta_sa.exe en la carpeta:\n{self.game_dir}")
            self.on_closing()
            
        if not os.path.exists(os.path.join(self.game_dir, "versionHooked.dll")):
            print("[WARNING] versionHooked.dll not found. Direct launch protection might fail.")

    def check_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def launch_game(self):
        if self.is_game_running: return
        self.is_game_running = True
        
        try:
            process = subprocess.Popen([self.game_exe_path], cwd=self.game_dir)
            self.start_time = time.time()
            self.root.withdraw()
            threading.Thread(target=self.track_time, args=(process,), daemon=True).start()
        except Exception as e:
            print(f"Error launching game: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"No se pudo iniciar el juego: {e}"))
            self.on_closing()

    def track_time(self, process):
        process.wait()
        self.root.deiconify()
        
        session_time = int(time.time() - self.start_time)
        self.config["playtime"] += session_time
        self.save_config()
        
        self.is_game_running = False
        self.root.after(0, lambda: self.status_label.config(text="Juego cerrado.", fg="#E0E0E0"))
        self.root.after(2000, self.on_closing)

    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02}h {minutes:02}m {secs:02}s" 

    def on_closing(self):
        self.video_running = False
        try:
            if self.video_cap: self.video_cap.release()
            if hasattr(self, 'mutex_handle'):
                ctypes.windll.kernel32.CloseHandle(self.mutex_handle)
        except Exception as e:
            print(f"Error during closing: {e}")
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GTALauncher(root)
    root.mainloop()
