import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from controller.analyze_controller import analyze_system
from controller.control_observ_controller import control_observ
from controller.state_feedback_controller import compute_state_feedback
from controller.nonlinear_controller import analyze_nonlinear_system
import sympy as sp
from controller.pid_controller import simulate_pid
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import tempfile, os
import tempfile
import csv


class MainWindow:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Analyse Système d'État")
        self.root.geometry("1000x600")
        self.fig_anim = Figure(figsize=(3, 3), dpi=100)
        self.ax_anim = self.fig_anim.add_subplot(111)
        
        self.canvas_anim = FigureCanvasTkAgg(self.fig_anim, master=self.root)
        self.canvas_anim.get_tk_widget().pack(side="top", fill="both", expand=True)

        # Création de self.frame_matrices AVANT d'utiliser self.btn_controle_obs
        self.frame_matrices = tk.Frame(self.root, padx=10, pady=10)
        self.frame_matrices.pack(side=tk.LEFT, fill=tk.Y)

    

        self.setup_ui()
    
    def open_pid_window(self):
        pid_win = tk.Toplevel(self.root)
        pid_win.title("Module PID - Régulation")
        pid_win.geometry("900x700")

        # --- Frame gauche : saisie système ---
        frame_sys = tk.LabelFrame(pid_win, text="Système à réguler", padx=5, pady=5)
        frame_sys.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(frame_sys, text="Numérateur (ex: 1)").pack()
        entry_num = tk.Entry(frame_sys, width=40)
        entry_num.insert(0, "1")
        entry_num.pack(pady=5)

        tk.Label(frame_sys, text="Dénominateur (ex: [1,1,0])").pack()
        entry_den = tk.Entry(frame_sys, width=40)
        entry_den.insert(0, "1,1,0")   # équivalent à s^2 + s
        entry_den.pack(pady=5)

        # --- Frame milieu : réglage PID ---
        frame_pid = tk.LabelFrame(pid_win, text="Réglage PID", padx=5, pady=5)
        frame_pid.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(frame_pid, text="Kp").pack()
        entry_Kp = tk.Entry(frame_pid, width=10)
        entry_Kp.insert(0, "1.0")
        entry_Kp.pack()

        tk.Label(frame_pid, text="Ki").pack()
        entry_Ki = tk.Entry(frame_pid, width=10)
        entry_Ki.insert(0, "0.0")
        entry_Ki.pack()

        tk.Label(frame_pid, text="Kd").pack()
        entry_Kd = tk.Entry(frame_pid, width=10)
        entry_Kd.insert(0, "0.0")
        entry_Kd.pack()

        # --- Frame droite : affichage graphique ---
        frame_plot = tk.LabelFrame(pid_win, text="Résultats", padx=5, pady=5)
        frame_plot.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        fig = Figure(figsize=(6,4))
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # --- Simulation PID ---
        def simulate_and_plot():
            try:
                num = [float(x) for x in entry_num.get().split(",")]
                den = [float(x) for x in entry_den.get().split(",")]
                Kp = float(entry_Kp.get())
                Ki = float(entry_Ki.get())
                Kd = float(entry_Kd.get())

                results = simulate_pid(num, den, Kp, Ki, Kd)

                # Réponse temporelle
                ax.clear()
                ax.plot(results["t"], results["y"], label="Sortie y(t)")
                ax.plot(results["t_err"], results["err"], label="Erreur e(t)", linestyle="--")
                ax.set_xlabel("Temps")
                ax.set_ylabel("Amplitude")
                ax.legend()
                ax.grid(True)
                canvas.draw()
                
                # Sauvegarde la figure PID
                img_pid = os.path.join(tempfile.gettempdir(), "pid_response.png")
                fig.savefig(img_pid)
                self.img_pid_path = img_pid
                
                self.pid_params = {
                    "num": num,
                    "den": den,
                    "Kp": Kp,
                    "Ki": Ki,
                    "Kd": Kd
                }


                # Affiche les pôles en console
                print("Pôles :", results["poles"])

            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        tk.Button(frame_pid, text="Simuler PID", command=simulate_and_plot).pack(pady=10)    

    def setup_ui(self):
        # Frame de gauche pour la saisie des matrices
        frame_gauche = tk.Frame(self.root, padx=10, pady=10)
        frame_gauche.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.entries = {}
        for label in ['A', 'B', 'C', 'D']:
            tk.Label(frame_gauche, text=f"Matrice {label} (ex: 1,2;3,4)", font=("Arial", 12)).pack(anchor='w')
            entry = tk.Entry(frame_gauche, width=60, font=("Arial", 12))
            entry.pack(pady=5, fill=tk.X)
            self.entries[label] = entry

        self.analyser_btn = tk.Button(frame_gauche, text="Analyser", command=self.lancer_analyse, font=("Arial", 12))
        self.analyser_btn.pack(pady=10)

        
        self.feedback_btn = tk.Button(frame_gauche, text="Commande par retour d'état", 
                                      command=self.open_specs_window, font=("Arial", 12))
        self.feedback_btn.pack(pady=10)
        
        self.observer_btn = tk.Button(frame_gauche, text="Commande par retour de sortie", 
                              command=self.open_observer_window, font=("Arial", 12))
        self.observer_btn.pack(pady=10)
        
        self.nonlinear_btn = tk.Button(frame_gauche, text="Analyse Non Linéaire", 
                               command=self.open_nonlinear_window, font=("Arial", 12))
        self.nonlinear_btn.pack(pady=10)
        
        btn_pid = tk.Button(self.root, text="Module PID", command=self.open_pid_window)
        btn_pid.pack(pady=10)
        
        self.export_btn = tk.Button(frame_gauche, text="Exporter PDF", command=self.export_pdf, font=("Arial", 12))
        self.export_btn.pack(pady=10)


        self.export_csv_btn = tk.Button(frame_gauche, text="Exporter CSV", command=self.export_csv, font=("Arial", 12))
        self.export_csv_btn.pack(pady=10)


        # Frame de droite pour les résultats et les graphiques
        frame_droit = tk.Frame(self.root, padx=10, pady=10)
        frame_droit.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Zone de texte pour les résultats (affiche tout sans écraser)
        self.resultats_text = tk.Text(frame_droit, height=6, font=("Courier", 11))
        self.resultats_text.pack(fill=tk.BOTH, expand=True, pady=10)

        # Figure matplotlib avec deux sous-graphiques
        self.figure = Figure(figsize=(6, 5), dpi=100)
        self.ax_impulse = self.figure.add_subplot(211)
        self.ax_bode = self.figure.add_subplot(212)

        self.canvas = FigureCanvasTkAgg(self.figure, master=frame_droit)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
   

    def export_pdf(self):
        try:
            fichier_pdf = "analyse_complete.pdf"
            doc = SimpleDocTemplate(fichier_pdf)
            styles = getSampleStyleSheet()
            contenu = []

            # Résultats Numériques
            texte_resultats = self.resultats_text.get("1.0", tk.END)
            contenu.append(Paragraph("<b>Résultats Numériques</b>", styles["Heading2"]))
            contenu.append(Paragraph(texte_resultats.replace("\n", "<br/>"), styles["Normal"]))
            contenu.append(Spacer(1, 12))

            # Section PID si disponible
            if hasattr(self, "pid_params"):
                pid = self.pid_params
                contenu.append(Paragraph("<b>Analyse PID</b>", styles["Heading2"]))
                contenu.append(Paragraph(
                    f"Fonction de transfert :<br/>"
                    f"Numérateur = {pid['num']}<br/>"
                    f"Dénominateur = {pid['den']}<br/>"
                    f"Kp = {pid['Kp']}<br/>"
                    f"Ki = {pid['Ki']}<br/>"
                    f"Kd = {pid['Kd']}",
                    styles["Normal"]
                ))
                contenu.append(Spacer(1, 12))

            images_paths = []

            # Figures classiques
            img1 = os.path.join(tempfile.gettempdir(), "impulse.png")
            self.ax_impulse.figure.savefig(img1)
            images_paths.append(img1)

            img2 = os.path.join(tempfile.gettempdir(), "bode.png")
            self.ax_bode.figure.savefig(img2)
            images_paths.append(img2)

            img3 = os.path.join(tempfile.gettempdir(), "animation.png")
            self.fig_anim.savefig(img3)
            images_paths.append(img3)

            # Figure non linéaire
            if hasattr(self, "img_nl_path") and os.path.exists(self.img_nl_path):
                images_paths.append(self.img_nl_path)

            # Figure PID
            if hasattr(self, "img_pid_path") and os.path.exists(self.img_pid_path):
                images_paths.append(self.img_pid_path)

            contenu.append(Paragraph("<b>Figures & Analyses</b>", styles["Heading2"]))
            for path in images_paths:
                contenu.append(Image(path, width=400, height=250))
                contenu.append(Spacer(1, 12))

            doc.build(contenu)
            messagebox.showinfo("Export PDF", f"✅ PDF généré : {fichier_pdf}")

        except Exception as e:
            messagebox.showerror("Erreur Export PDF", str(e))
    
    def export_csv(self):
            try:
                fichier_csv = "analyse_complete.csv"
                lignes = []

                # Résultats Numériques (depuis la zone de texte)
                texte_resultats = self.resultats_text.get("1.0", tk.END).strip()
                lignes.append(["Section", "Résultats"])
                lignes.append(["Résultats Numériques", texte_resultats])

                # Section PID si disponible
                if hasattr(self, "pid_params"):
                    pid = self.pid_params
                    lignes.append(["Analyse PID", ""])
                    lignes.append(["Numérateur", str(pid['num'])])
                    lignes.append(["Dénominateur", str(pid['den'])])
                    lignes.append(["Kp", pid['Kp']])
                    lignes.append(["Ki", pid['Ki']])
                    lignes.append(["Kd", pid['Kd']])

                # Section Analyse Non Linéaire si disponible
                if hasattr(self, "img_nl_path") and os.path.exists(self.img_nl_path):
                    lignes.append(["Analyse Non Linéaire", "Figure enregistrée : nonlinear_phase.png"])

                # Section Figures (juste les noms des fichiers)
                figures = []
                img1 = os.path.join(tempfile.gettempdir(), "impulse.png")
                img2 = os.path.join(tempfile.gettempdir(), "bode.png")
                img3 = os.path.join(tempfile.gettempdir(), "animation.png")
                if os.path.exists(img1): figures.append("impulse.png")
                if os.path.exists(img2): figures.append("bode.png")
                if os.path.exists(img3): figures.append("animation.png")
                if hasattr(self, "img_pid_path") and os.path.exists(self.img_pid_path):
                    figures.append("pid_response.png")
                if figures:
                    lignes.append(["Figures", ", ".join(figures)])

                # Écriture du CSV
                with open(fichier_csv, "w", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerows(lignes)

                messagebox.showinfo("Export CSV", f"✅ CSV généré : {fichier_csv}")

            except Exception as e:
                messagebox.showerror("Erreur Export CSV", str(e))

    def lire_matrice(self, texte):
        try:
            lignes = texte.strip().split(';')
            return np.array([[float(x) for x in ligne.split(',')] for ligne in lignes])
        except Exception:
            messagebox.showerror("Erreur", "Format de matrice incorrect")
            return None
    
    def open_specs_window(self):
        """Fenêtre secondaire pour saisir les performances désirées"""
        specs_win = tk.Toplevel(self.root)
        specs_win.title("Spécifications de performance")
        specs_win.geometry("360x330")

        # --- Champs de saisie ---
        tk.Label(specs_win, text="Temps d'établissement Ts (s) :").pack(anchor="w", padx=10, pady=4)
        entry_ts = ttk.Entry(specs_win)
        entry_ts.pack(fill="x", padx=10)

        tk.Label(specs_win, text="Dépassement OS (%) :").pack(anchor="w", padx=10, pady=4)
        entry_os = ttk.Entry(specs_win)
        entry_os.pack(fill="x", padx=10)

        tk.Label(specs_win, text="Marge de gain GM (dB) :").pack(anchor="w", padx=10, pady=4)
        entry_gm = ttk.Entry(specs_win)
        entry_gm.pack(fill="x", padx=10)

        tk.Label(specs_win, text="Marge de phase PM (°) :").pack(anchor="w", padx=10, pady=4)
        entry_pm = ttk.Entry(specs_win)
        entry_pm.pack(fill="x", padx=10)

        def _parse_float(entry, default=None):
            try:
                val = entry.get().strip()
                return float(val) if val else default
            except ValueError:
                return default

        def valider():
            import numpy as np

            # --- Récupération des matrices ---
            A = self.lire_matrice(self.entries['A'].get())
            B = self.lire_matrice(self.entries['B'].get())
            if A is None or B is None:
                return
            n = A.shape[0]

            # --- Lecture des specs ---
            Ts = float(entry_ts.get() or 2.0)
            OS_pct = float(entry_os.get() or 10.0)
            GM_db = float(entry_gm.get() or 0.0)
            PM_deg = float(entry_pm.get() or 0.0)
            OS = max(0.0, OS_pct) / 100.0

            # --- Calcul ζ et ωn ---
            if OS > 0:
                zeta = -np.log(OS) / np.sqrt(np.pi**2 + (np.log(OS))**2)
            else:
                zeta = 0.7
            wn = 4.0 / (zeta * Ts)

            if PM_deg > 0:
                pm_rad = np.deg2rad(PM_deg)
                zeta_pm = np.sin(pm_rad) / (1 + np.cos(pm_rad))
                zeta = max(zeta, zeta_pm)

            if GM_db > 0:
                wn *= 1.0 + GM_db / 20.0

            sigma = -zeta * wn
            wd = wn * np.sqrt(max(0.0, 1 - zeta**2))

            # --- Pôles désirés ---
            desired_poles = [sigma + 1j*wd, sigma - 1j*wd]
            while len(desired_poles) < n:
                desired_poles.append(sigma * (1.0 + 0.5*len(desired_poles)))
            desired_poles = np.array(desired_poles[:n], dtype=complex)

            # --- Calcul du gain K et simulation ---
            from controller.state_feedback_controller import compute_state_feedback
            x0 = np.zeros(n)
            t_end = max(10.0, 5.0*Ts)
            results = compute_state_feedback(A, B, desired_poles, x0=x0, t_span=(0.0, t_end))

            # --- Mettre à jour section "Commande État" ---
            text_content = self.resultats_text.get("1.0", tk.END)
            if "=== Commande État ===" in text_content:
                index_start = text_content.index("=== Commande État ===")
                self.resultats_text.delete(f"{index_start}.0", tk.END)

            self.resultats_text.insert(
                tk.END,
                "\n=== Commande État ===\n"
                f"Pôles désirés : {np.round(desired_poles, 3)}\n"
                f"Gain K : {np.round(results['K'], 4)}\n"
            )

            


        ttk.Button(specs_win, text="Valider", command=valider).pack(pady=12)


    def open_observer_window(self):
        """Fenêtre secondaire pour saisir les pôles de l’observateur directement"""
        obs_win = tk.Toplevel(self.root)
        obs_win.title("Spécifications Observateur")
        obs_win.geometry("360x200")

        tk.Label(obs_win, text="Pôles désirés (séparés par des virgules) :").pack(anchor="w", padx=10, pady=6)
        entry_poles = ttk.Entry(obs_win)
        entry_poles.pack(fill="x", padx=10)

        def valider():
            # Lecture des matrices
            A = self.lire_matrice(self.entries['A'].get())
            B = self.lire_matrice(self.entries['B'].get())
            C = self.lire_matrice(self.entries['C'].get())
            if A is None or B is None or C is None:
                return
            n = A.shape[0]

            # Lecture des pôles
            txt = entry_poles.get()
            try:
                desired_poles_obs = []
                for val in txt.split(","):
                    val = val.strip()
                    pole = complex(val.replace("i", "j"))  # Supporte "i" pour les complexes
                    desired_poles_obs.append(pole)
                desired_poles_obs = np.array(desired_poles_obs, dtype=complex)

                if len(desired_poles_obs) != n:
                    tk.messagebox.showerror("Erreur", f"Il faut entrer {n} pôles pour un système d’ordre {n}.")
                    return
            except Exception as e:
                tk.messagebox.showerror("Erreur", f"Format invalide : {e}")
                return

            # Import du contrôleur
            from controller.output_feedback_controller import simulate_output_feedback

            # États initiaux 1D pour solve_ivp
            x0 = np.zeros(n)       # état réel initial
            xhat0 = np.ones(n)     # estimation initiale
            t_span = (0, 10)

            try:
                results_obs = simulate_output_feedback(A, B, C, np.zeros((1, n)), desired_poles_obs, x0, xhat0, t_span)
            except Exception as e:
                tk.messagebox.showerror("Erreur", f"Simulation impossible : {e}")
                return

            # Affichage clair
            self.resultats_text.insert(
                tk.END,
                "\n=== Observateur ===\n"
                f"Pôles désirés Observateur : {np.round(desired_poles_obs, 3)}\n"
                f"Gain L : {np.round(results_obs['L'], 4)}\n"
            )

            obs_win.destroy()

        ttk.Button(obs_win, text="Valider", command=valider).pack(pady=12)


    def open_nonlinear_window(self):
            nl_win = tk.Toplevel(self.root)
            nl_win.title("Analyse Non Linéaire")
            nl_win.geometry("500x600")

            # Frame pour les entrées
            frame_inputs = tk.Frame(nl_win)
            frame_inputs.pack(fill="x", pady=5, padx=5)

            # Variables d'état
            tk.Label(frame_inputs, text="Variables d'état (ex: x1,x2) :", font=("Arial", 12)).pack(pady=2)
            entry_vars = tk.Entry(frame_inputs, width=50)
            entry_vars.pack(pady=2)

            tk.Label(frame_inputs, text="Équations dynamiques (ex: x2,-x1+(1-x1**2)*x2) :", font=("Arial", 12)).pack(pady=2)
            entry_eqs = tk.Entry(frame_inputs, width=50)
            entry_eqs.pack(pady=2)

            tk.Label(frame_inputs, text="État initial (ex: 1,0) :", font=("Arial", 12)).pack(pady=2)
            entry_x0 = tk.Entry(frame_inputs, width=50)
            entry_x0.pack(pady=2)

            tk.Label(frame_inputs, text="Point d'équilibre (ex: 0,0) :", font=("Arial", 12)).pack(pady=2)
            entry_eq = tk.Entry(frame_inputs, width=50)
            entry_eq.pack(pady=2)

            tk.Label(frame_inputs, text="Fonction de Lyapunov (ex: x1**2 + x2**2) :", font=("Arial", 12)).pack(pady=2)
            entry_V = tk.Entry(frame_inputs, width=50)
            entry_V.pack(pady=2)

            # Frame pour le canvas
            frame_canvas = tk.Frame(nl_win)
            frame_canvas.pack(fill="both", expand=False, pady=5, padx=5)

            fig = Figure(figsize=(2.5,2.5))

            ax = fig.add_subplot(111)
            canvas = FigureCanvasTkAgg(fig, master=frame_canvas)
            canvas.get_tk_widget().pack(fill="both", expand=True)

            # Bouton en bas
            def lancer_analyse_nl():
                try:
                    vars_list = [sp.symbols(v.strip()) for v in entry_vars.get().split(',')]
                    eqs_list = [sp.sympify(e.strip()) for e in entry_eqs.get().split(',')]
                    x0_vals = [float(x) for x in entry_x0.get().split(',')]
                    eq_pt = [float(x) for x in entry_eq.get().split(',')]
                    V_expr = entry_V.get()

                    results = analyze_nonlinear_system(vars_list, eqs_list, x0_vals, t_span=(0,20), eq_point=eq_pt, V_expr=V_expr)

                    # ...dans la fonction lancer_analyse_nl de open_nonlinear_window...
                    ax.clear()
                    ax.plot(results['states'][0], results['states'][1])
                    ax.set_xlabel(str(vars_list[0]))
                    ax.set_ylabel(str(vars_list[1]))
                    ax.set_title("Portrait de phase")
                    canvas.draw()

                    # Sauvegarde la figure dans un fichier temporaire
                    img_nl = os.path.join(tempfile.gettempdir(), "nonlinear_phase.png")
                    fig.savefig(img_nl)
                    self.img_nl_path = img_nl  # Stocke le chemin dans l'objet principal

                    print("V(x) =", results['lyapunov_V'])
                    print("dV/dt =", results['dVdt'])

                except Exception as e:
                    tk.messagebox.showerror("Erreur", str(e))

            tk.Button(nl_win, text="Lancer Analyse Non Linéaire", command=lancer_analyse_nl).pack(side="bottom", pady=3)


    from controller.pid_controller import simulate_pid  # <-- ton fichier

    
    
    
    def lancer_animation(self, A, B, commandes=None, dt=0.05, T=1.0, proj=(0, 1)):
        """
        Anime la dynamique ẋ = A x + B u sur l'axe self.ax_anim intégré à Tkinter.

        Paramètres
        ----------
        A : (n,n) ndarray
        B : (n,m) ndarray
        commandes : liste d'entrées constantes (scalaires si m=1, vecteurs (m,) sinon)
                    Si None : valeurs par défaut (voir plus bas)
        dt : pas de temps d’Euler
        T  : durée totale (s)
        proj : indices (i, j) des composantes d'état à projeter (par défaut x1 vs x2)
        """
        import numpy as np
        from matplotlib.animation import FuncAnimation

        # ---- 1) Validation et formes ----
        A = np.asarray(A, dtype=float)
        B = np.asarray(B, dtype=float)
        n = A.shape[0]
        if A.shape != (n, n):
            raise ValueError("A doit être carrée (n x n).")
        if B.ndim == 1:
            B = B.reshape(n, 1)
        if B.shape[0] != n:
            raise ValueError("B doit avoir n lignes (même n que A).")
        m = B.shape[1]

        i, j = proj
        if not (0 <= i < n and 0 <= j < n and i != j):
            raise ValueError("proj doit être un couple d'indices valides et distincts (ex: (0,1)).")

        # ---- 2) Commandes par défaut ----
        if commandes is None:
            if m == 1:
                # trois constantes : +1, -1, 0
                commandes = [1.0, -1.0, 0.0]
            else:
                # pour m>1 : quelques vecteurs utiles (e1, -e1, 0, ones)
                e1 = np.zeros(m); e1[0] = 1.0
                commandes = [e1, -e1, np.zeros(m), np.ones(m)]

        # Normalise en vecteurs (m,) pour le calcul B @ u
        cmds = []
        for u in commandes:
            u = np.asarray(u, dtype=float)
            if u.ndim == 0 and m == 1:
                u = np.array([float(u)])           # scalaire -> (1,)
            if u.shape != (m,):
                raise ValueError(f"Chaque commande doit avoir la forme {(m,)} (reçu {u.shape}).")
            cmds.append(u)

        # ---- 3) Préparation de la figure/axe ----
        # Important : on réutilise self.ax_anim créé dans setup_ui
        self.ax_anim.clear()
        self.ax_anim.set_xlabel(f"État x{i+1}")
        self.ax_anim.set_ylabel(f"État x{j+1}")
        self.ax_anim.set_title(f"Trajectoires (projection x{i+1}, x{j+1})")
        # Fenêtre fixe confortable (tu peux ajuster)
        self.ax_anim.set_xlim(-5, 5)
        self.ax_anim.set_ylim(-5, 5)

        # ---- 4) Objets graphiques et mémoires ----
        lines = []
        for _ in cmds:
            (line,) = self.ax_anim.plot([], [], lw=2)
            lines.append(line)

        N = int(T / dt)
        x0 = np.zeros(n)   # état initial
        trajectoires = np.zeros((len(cmds), N + 1, n))
        trajectoires[:, 0, :] = x0  # même x0 pour toutes les commandes

        # ---- 5) Fonction d'update (Euler explicite) ----
        def update(k):
            # k : indice de frame (0..N-1)
            for idx, u in enumerate(cmds):
                x_prev = trajectoires[idx, k, :]
                dx = A @ x_prev + B @ u
                x_new = x_prev + dt * dx
                trajectoires[idx, k + 1, :] = x_new

                # On trace jusqu'à la frame k+1 (trajectoire cumulée)
                data = trajectoires[idx, :k + 2, :]
                lines[idx].set_data(data[:, i], data[:, j])

                # Légende lisible
                if m == 1:
                    lines[idx].set_label(f"u = {u[0]:g}")
                else:
                    lines[idx].set_label(f"u = {np.array2string(u, precision=2)}")

            self.ax_anim.legend(loc="best")
            return lines

        # ---- 6) Lancer l’animation et garder une référence ----
        self.ani = FuncAnimation(self.fig_anim, update, frames=N, interval=50, blit=False)

        # ---- 7) Redessiner le canvas Tkinter ----
        self.canvas_anim.draw()


    def lancer_analyse(self):
        A = self.lire_matrice(self.entries['A'].get())
        B = self.lire_matrice(self.entries['B'].get())
        C = self.lire_matrice(self.entries['C'].get())
        D = self.lire_matrice(self.entries['D'].get())

        if any(x is None for x in (A, B, C, D)):
            return

        try:
            resultats = analyze_system(A, B, C, D)
            self.lancer_animation(A, B)
            control_obs = control_observ(A,B,C,D)
            
            
        except Exception as e:
            messagebox.showerror("Erreur lors de l'analyse", str(e))
            return
        
        self.resultats_text.delete("1.0", tk.END)
        self.resultats_text.insert(tk.END, f"Pôles : {np.round(resultats['poles'], 3)}\n")
        self.resultats_text.insert(tk.END, f"Stabilité : {'Stable' if resultats['stable'] else 'Instable'}\n")
        self.resultats_text.insert(tk.END, f"rang de Wc : {np.round(control_obs['rang_Wc'], 3)}\n")
        self.resultats_text.insert(tk.END, f"rang de Wo : {np.round(control_obs['rang_Wo'], 3)}\n")
        self.resultats_text.insert(tk.END, f"Verdict : {control_obs['conclusion']}\n")

        self.rafraichir_plots(resultats)
        
        
        
    def rafraichir_plots(self, resultats):
            self.ax_impulse.clear()
            self.ax_bode.clear()

            # Réponse impulsionnelle
            self.ax_impulse.plot(resultats['temps'], resultats['reponse'], lw=2)
            self.ax_impulse.set_title("Réponse impulsionnelle", fontsize=14)
            self.ax_impulse.set_xlabel("Temps", fontsize=12)
            self.ax_impulse.set_ylabel("Amplitude", fontsize=12)
            self.ax_impulse.tick_params(axis='both', labelsize=11)
            self.ax_impulse.grid(True)

            # Diagramme de Bode
            self.ax_bode.semilogx(resultats['frequence'], 20 * np.log10(resultats['gain']), lw=2)
            self.ax_bode.set_title("Diagramme de Bode (gain)", fontsize=14)
            self.ax_bode.set_xlabel("Fréquence (rad/s)", fontsize=12)
            self.ax_bode.set_ylabel("Gain (dB)", fontsize=12)
            self.ax_bode.tick_params(axis='both', labelsize=11)
            self.ax_bode.grid(True)

            # Ajuste la mise en page pour éviter le chevauchement
            self.figure.tight_layout()

            self.canvas.draw()
        
   

if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
