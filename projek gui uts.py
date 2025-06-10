import tkinter as tk
from tkinter import messagebox
import random

# =======================
# FUNGSI DASHBOARD
# =======================
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
            tk.Label(content_frame, text="Daftar Tagihan", font=("Helvetica", 14, "bold")).pack(pady=10)
            invoice_no = f"INV-{random.randint(100000, 999999)}"
            tk.Label(content_frame, text=f"Nomor Invoice: {invoice_no}", font=("Helvetica", 11, "bold"), fg="#cc0000").pack(pady=5)

            tagihan = [
                ("UKT Semester 4", 350000),
                ("Dana Kegiatan", 100000),
                ("Asuransi Mahasiswa", 50000)
            ]

            total = 0
            for nama, jumlah in tagihan:
                tk.Label(content_frame, text=f"{nama}: Rp {jumlah:,}").pack(anchor="w", padx=20)
                total += jumlah

            tk.Label(content_frame, text=f"\nJumlah Tagihan: Rp {total:,}", font=("Helvetica", 12, "bold"), fg="#cc0000").pack(pady=10)

            tk.Label(content_frame, text="Metode Pembayaran:", font=("Helvetica", 12)).pack(pady=5)
            metode_var = tk.StringVar(value="Bank Aceh")

            metode_frame = tk.Frame(content_frame)
            metode_frame.pack(pady=5)

            tk.Radiobutton(metode_frame, text="Bank Aceh", variable=metode_var, value="Bank Aceh").pack(side="left", padx=10)
            tk.Radiobutton(metode_frame, text="Bank Syariah Indonesia", variable=metode_var, value="Bank Syariah Indonesia").pack(side="left", padx=10)

            def bayar():
                metode = metode_var.get()
                messagebox.showinfo("Pembayaran", f"Pembayaran invoice {invoice_no} berhasil melalui {metode}!")
                lanjut_btn.pack(pady=10)

            tk.Button(content_frame, text="Bayar Sekarang", bg="#007acc", fg="white", padx=20, pady=5, command=bayar).pack(pady=10)
            lanjut_btn = tk.Button(content_frame, text="Lanjut Pilih KRS", bg="#28a745", fg="white", padx=20, pady=5, command=lambda: show_content("KRS"))

        elif content == "KRS":
            tk.Label(content_frame, text="Pemilihan Mata Kuliah (KRS)", font=("Helvetica", 14, "bold")).pack(pady=20)
            matkul_list = [
                "Basis Data Lanjut",
                "Pemrograman Web",
                "Jaringan Komputer",
                "Kecerdasan Buatan",
                "Sistem Informasi Akuntansi"
            ]
            selected_matkul = []

            def simpan_krs():
                dipilih = [matkul for var, matkul in selected_matkul if var.get()]
                if not dipilih:
                    messagebox.showwarning("KRS", "Silakan pilih minimal 1 mata kuliah!")
                else:
                    messagebox.showinfo("KRS", f"Mata kuliah yang dipilih:\n{', '.join(dipilih)}")

            for matkul in matkul_list:
                var = tk.BooleanVar()
                tk.Checkbutton(content_frame, text=matkul, variable=var).pack(anchor="w", padx=20)
                selected_matkul.append((var, matkul))

            tk.Button(content_frame, text="Simpan KRS", bg="#007acc", fg="white", padx=20, pady=5, command=simpan_krs).pack(pady=20)

        elif content == "Profil":
            tk.Label(content_frame, text="Profil Mahasiswa", font=("Helvetica", 14, "bold")).pack(pady=20)
            tk.Label(content_frame, text="Nama     : Melvi Anggraini").pack(anchor="w", padx=20)
            tk.Label(content_frame, text="NIM      : 200511050").pack(anchor="w", padx=20)
            tk.Label(content_frame, text="Program  : Sistem Informasi").pack(anchor="w", padx=20)
            tk.Label(content_frame, text="Semester : 4").pack(anchor="w", padx=20)

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


# =======================
# FUNGSI LOGIN + LUPA PASSWORD
# =======================
def start_login():
    login = tk.Tk()
    login.title("Login Sistem Akademik")
    login.geometry("400x550")
    login.configure(bg="white")

    tk.Label(login, text="Masuk dan Verifikasi", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
    tk.Label(login, text="Nikmati kemudahan autentikasi layanan kampus", font=("Helvetica", 9), bg="white").pack(pady=5)

    tk.Label(login, text="Email/NIM/Username", bg="white").pack(anchor="w", padx=40)
    email_entry = tk.Entry(login, width=30, relief="solid")
    email_entry.pack(pady=5)

    
    tk.Label(login, text="Password", bg="white").pack(anchor="w", padx=40)
    password_entry = tk.Entry(login, width=30, show="*", relief="solid")
    password_entry.pack(pady=5)


    # Tombol Lupa Password
    def lupa_password():
        messagebox.showinfo("Lupa Password", "Silakan hubungi admin akademik untuk reset password atau cek email Anda.")

    tk.Button(login, text="Lupa kata sandi?", bg="white", fg="#007acc", borderwidth=0, command=lupa_password).pack(anchor="e", padx=40, pady=5)

    def proses_login():
        if email_entry.get() and password_entry.get():
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {email_entry.get()}!")
            login.destroy()
            show_dashboard()
        else:
            messagebox.showerror("Login Gagal", "Silakan isi email dan password.")

    tk.Button(login, text="Masuk", bg="#007acc", fg="white", width=30, command=proses_login).pack(pady=20)
    login.mainloop()


# =======================
# RUN APLIKASI
# =======================
start_login()
