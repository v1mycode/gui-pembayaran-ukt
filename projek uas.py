import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import random

# ========================
# Koneksi Database SQLite
# ========================
conn = sqlite3.connect("ukt_database.db")
cursor = conn.cursor()

# Buat tabel kalau belum ada
cursor.execute('''CREATE TABLE IF NOT EXISTS pembayaran (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT,
                    nim TEXT,
                    semester TEXT,
                    nominal INTEGER,
                    metode TEXT,
                    invoice TEXT)''')
conn.commit()

# Variabel status bayar
status_bayar = False

# Fungsi Simpan Pembayaran ke Database
def simpan_pembayaran(nama, nim, semester, nominal, metode, invoice):
    cursor.execute("INSERT INTO pembayaran (nama, nim, semester, nominal, metode, invoice) VALUES (?, ?, ?, ?, ?, ?)",
                   (nama, nim, semester, nominal, metode, invoice))
    conn.commit()

# Fungsi Tampilkan Histori Pembayaran
def lihat_histori():
    histori = tk.Toplevel()
    histori.title("Histori Pembayaran UKT")

    tree = ttk.Treeview(histori, columns=('Nama', 'NIM', 'Semester', 'Nominal', 'Metode', 'Invoice'), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    cursor.execute("SELECT nama, nim, semester, nominal, metode, invoice FROM pembayaran")
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

# ========================
# FUNGSI DASHBOARD
# ========================
def show_dashboard():
    dashboard = tk.Tk()
    dashboard.title("Sistem Akademik Mahasiswa")
    dashboard.geometry("800x500")
    dashboard.configure(bg="white")

    def show_content(content):
        for widget in content_frame.winfo_children():
            widget.destroy()

        if content == "Beranda":
            tk.Label(content_frame, text="Selamat Datang di Portal Mahasiswa!", font=("Helvetica", 16, "bold")).pack(pady=20)

        elif content == "Pembayaran":
            tk.Label(content_frame, text="Form Pembayaran UKT", font=("Helvetica", 14, "bold")).pack(pady=10)

            tk.Label(content_frame, text="Nama").pack()
            nama_entry = tk.Entry(content_frame)
            nama_entry.pack()

            tk.Label(content_frame, text="NIM").pack()
            nim_entry = tk.Entry(content_frame)
            nim_entry.pack()

            tk.Label(content_frame, text="Semester").pack()
            semester_entry = tk.Entry(content_frame)
            semester_entry.pack()

            total_tagihan = 500000
            tk.Label(content_frame, text=f"Jumlah Tagihan : Rp {total_tagihan:,}").pack(pady=5)

            metode_var = tk.StringVar(value="Bank Aceh")
            tk.Label(content_frame, text="Metode Pembayaran:").pack()
            metode_frame = tk.Frame(content_frame)
            metode_frame.pack()
            tk.Radiobutton(metode_frame, text="Bank Aceh", variable=metode_var, value="Bank Aceh").pack(side="left", padx=10)
            tk.Radiobutton(metode_frame, text="BSI", variable=metode_var, value="BSI").pack(side="left", padx=10)

            invoice_no = f"INV-{random.randint(100000, 999999)}"
            tk.Label(content_frame, text=f"Nomor Invoice: {invoice_no}").pack(pady=5)

            def bayar():
                global status_bayar
                nama = nama_entry.get()
                nim = nim_entry.get()
                semester = semester_entry.get()
                metode = metode_var.get()

                if nama and nim and semester:
                    simpan_pembayaran(nama, nim, semester, total_tagihan, metode, invoice_no)
                    status_bayar = True
                    messagebox.showinfo("Sukses", f"Pembayaran berhasil!\nNomor Invoice: {invoice_no}")
                else:
                    messagebox.showerror("Error", "Mohon lengkapi semua data!")

            tk.Button(content_frame, text="Bayar", bg="#007acc", fg="white", command=bayar).pack(pady=10)
            tk.Button(content_frame, text="Lihat Histori Pembayaran", bg="#28a745", fg="white", command=lihat_histori).pack(pady=5)

        elif content == "KRS":
            if not status_bayar:
                messagebox.showwarning("KRS", "Silakan lakukan pembayaran terlebih dahulu!")
                return

            tk.Label(content_frame, text="Pemilihan Mata Kuliah (KRS)", font=("Helvetica", 14, "bold")).pack(pady=20)
            matkul_list = [
                "Basis Data Lanjut", "Pemrograman Web",
                "Jaringan Komputer", "Kecerdasan Buatan",
                "Sistem Informasi Akuntansi"
            ]
            selected_matkul = []

            def simpan_krs():
                dipilih = [matkul for var, matkul in selected_matkul if var.get()]
                if not dipilih:
                    messagebox.showwarning("KRS", "Pilih minimal 1 mata kuliah!")
                else:
                    messagebox.showinfo("KRS", f"Mata kuliah yang dipilih:\n{', '.join(dipilih)}")

            for matkul in matkul_list:
                var = tk.BooleanVar()
                tk.Checkbutton(content_frame, text=matkul, variable=var).pack(anchor="w", padx=20)
                selected_matkul.append((var, matkul))

            tk.Button(content_frame, text="Simpan KRS", bg="#007acc", fg="white", command=simpan_krs).pack(pady=20)

        elif content == "Profil":
            tk.Label(content_frame, text="Profil Mahasiswa", font=("Helvetica", 14, "bold")).pack(pady=20)
            tk.Label(content_frame, text="Nama     : Melvi Anggraini").pack(anchor="w", padx=20)
            tk.Label(content_frame, text="NIM      : 200511050").pack(anchor="w", padx=20)
            tk.Label(content_frame, text="Program  : Sistem Informasi").pack(anchor="w", padx=20)
            tk.Label(content_frame, text="Semester : 4").pack(anchor="w", padx=20)

    # Layout Header & Menu
    header = tk.Frame(dashboard, bg="#003366", height=60)
    header.pack(fill="x")
    tk.Label(header, text="UIN Ar-Raniry Banda Aceh", bg="#003366", fg="white", font=("Helvetica", 14, "bold")).place(x=20, y=15)

    menu_frame = tk.Frame(dashboard, bg="#004080", width=180)
    menu_frame.pack(side="left", fill="y")
    tk.Label(menu_frame, text="MENU", bg="#004080", fg="white", font=("Helvetica", 12, "bold")).pack(pady=20)

    menus = ["Beranda", "Pembayaran", "KRS", "Profil"]
    for item in menus:
        tk.Button(menu_frame, text=item, width=20, pady=8, bg="#0059b3", fg="white",
                  command=lambda name=item: show_content(name)).pack(pady=5)

    content_frame = tk.Frame(dashboard, bg="white")
    content_frame.pack(side="right", expand=True, fill="both")

    show_content("Beranda")
    dashboard.mainloop()

# ========================
# FUNGSI LOGIN + LUPA PASSWORD
# ========================
def start_login():
    login = tk.Tk()
    login.title("Login Sistem Akademik")
    login.geometry("400x500")
    login.configure(bg="white")

    tk.Label(login, text="Masuk Portal Mahasiswa", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
    tk.Label(login, text="Email/NIM/Username", bg="white").pack(anchor="w", padx=40)
    email_entry = tk.Entry(login, width=30, relief="solid")
    email_entry.pack(pady=5)

    tk.Label(login, text="Password", bg="white").pack(anchor="w", padx=40)
    password_entry = tk.Entry(login, width=30, show="*", relief="solid")
    password_entry.pack(pady=5)

    def lupa_password():
        messagebox.showinfo("Lupa Password", "Silakan hubungi admin akademik.")

    tk.Button(login, text="Lupa Password?", bg="white", fg="#007acc", borderwidth=0, command=lupa_password).pack(anchor="e", padx=40, pady=5)

    def proses_login():
        if email_entry.get() and password_entry.get():
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {email_entry.get()}!")
            login.destroy()
            show_dashboard()
        else:
            messagebox.showerror("Login Gagal", "Mohon isi email dan password.")

    tk.Button(login, text="Masuk", bg="#007acc", fg="white", width=30, command=proses_login).pack(pady=20)
    login.mainloop()

# ========================
# RUN APLIKASI
# ========================
start_login()
