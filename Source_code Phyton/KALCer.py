import os
import json
import sys
from datetime import datetime


# Aktifkan ANSI dan Unicode untuk Windows
if sys.platform == "win32":
    os.system("")
    # Set console encoding ke UTF-8
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    # Set code page ke UTF-8
    os.system('chcp 65001 > nul')

class Colors:
    """
    Kelas untuk menyimpan kode warna ANSI yang digunakan untuk pewarnaan output terminal.
    
    Atribut:
        HEADER: Warna ungu untuk header
        BLUE: Warna biru untuk informasi
        CYAN: Warna cyan untuk aksen
        GREEN: Warna hijau untuk sukses/positif
        YELLOW: Warna kuning untuk peringatan
        RED: Warna merah untuk error/negatif
        END: Reset warna ke default
        BOLD: Tebal
        UNDERLINE: Garis bawah
        WHITE: Putih terang
        GRAY: Abu-abu untuk teks sekunder
        BG_BLUE, BG_GREEN, BG_YELLOW, BG_RED: Warna background
    """
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BG_BLUE = '\033[44m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_RED = '\033[41m'

class KasKelas:
    """
    Kelas utama untuk sistem manajemen kas kelas.
    
    Mengelola data siswa, transaksi pemasukan dan pengeluaran,
    serta menyediakan berbagai laporan keuangan kelas.
    """
    
    def __init__(self):
        """
        Inisialisasi sistem kas kelas.
        
        Menentukan lokasi penyimpanan database, menampilkan welcome screen,
        dan memuat data yang sudah ada atau membuat data baru.
        """
        # Dapatkan folder dimana script Python berada
        if getattr(sys, 'frozen', False):
            # Jika dijalankan sebagai .exe
            app_path = os.path.dirname(sys.executable)
        else:
            # Jika dijalankan sebagai .py
            app_path = os.path.dirname(os.path.abspath(__file__))
        
        # Jika tidak bisa tulis di folder script, gunakan Documents
        try:
            test_file = os.path.join(app_path, '.test_write')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            # Bisa menulis di folder script
            self.data_dir = app_path
        except:
            # Tidak bisa menulis, gunakan Documents
            self.data_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'KasKelas')
            
            # Buat folder jika belum ada
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
        
        self.filename = os.path.join(self.data_dir, 'kas_kelas_database.json')
        
        self.print_welcome_screen()
        self.load_data()
    
    def print_welcome_screen(self):
        """
        Menampilkan layar selamat datang dengan desain box yang menarik.
        
        Menampilkan judul sistem dan lokasi penyimpanan database.
        """
        print(f"\n{Colors.CYAN}╔{'═'*88}╗{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END}{Colors.BOLD}{Colors.WHITE}{'KALCer':^88}{Colors.END}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END}{Colors.BOLD}{Colors.WHITE}{'Kas Kelas Cerdas':^88}{Colors.END}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END}{Colors.GRAY}{'Kelola Keuangan Kelas dengan Mudah':^88}{Colors.END}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}╠{'═'*88}╣{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END} {Colors.YELLOW}📁 Database:{Colors.END} {self.filename:<73} {Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}╚{'═'*88}╝{Colors.END}\n")
    
    def load_data(self):
        """
        Memuat data dari file JSON.
        
        Membaca data siswa dan pengeluaran umum dari file database.
        Jika file tidak ada atau rusak, akan membuat data baru.
        Menampilkan ringkasan data yang berhasil dimuat.
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.data_siswa = data.get('data_siswa', [])
                    self.pengeluaran_umum = data.get('pengeluaran_umum', [])
                
                print(f"{Colors.GREEN}✓ Data berhasil dimuat{Colors.END}")
                print(f"  {Colors.GRAY}• Jumlah siswa: {Colors.WHITE}{len(self.data_siswa)} orang{Colors.END}")
                
                total_transaksi = sum(len(s['transaksi']) for s in self.data_siswa) + len(self.pengeluaran_umum)
                print(f"  {Colors.GRAY}• Total transaksi: {Colors.WHITE}{total_transaksi}{Colors.END}")
                
            except json.JSONDecodeError:
                print(f"{Colors.RED}⚠ File JSON rusak! Membuat data baru...{Colors.END}")
                self.buat_data_baru()
            except Exception as e:
                print(f"{Colors.RED}⚠ Error: {e}{Colors.END}")
                self.buat_data_baru()
        else:
            print(f"{Colors.YELLOW}⚠ File tidak ditemukan{Colors.END}")
            print(f"{Colors.GREEN}✓ Membuat file baru...{Colors.END}")
            self.buat_data_baru()
            self.save_data()
    
    def buat_data_baru(self):
        """
        Membuat struktur data baru dengan daftar siswa default.
        
        Menginisialisasi data_siswa dengan daftar nama siswa yang sudah ditentukan,
        dan mengosongkan daftar pengeluaran_umum.
        """
        nama_list = [
            'Lutfi', 'Kevin', 'Bagus', 'Darel', 'Desi', 'Riski', 'Ridho', 'Rafa', 
            'Habib', 'Zumar', 'Zhen', 'Afan', 'Andi', 'Hafizd', 'Naufal', 'Nofal', 
            'Galih', 'Rafi', 'Rafif', 'Fadhil', 'Rakha', 'Arka', 'Reyhan', 'Reyza', 
            'Lucky', 'Riska', 'Safa', 'Aulyau', 'Mia', 'Tyas', 'Sulis', 'Ria', 
            'Usnia', 'Yoga'
        ]
        
        self.data_siswa = [
            {
                "nama": nama,
                "transaksi": [],
                "saldo": 0
            }
            for nama in nama_list
        ]
        
        self.pengeluaran_umum = []
    
    def save_data(self):
        """
        Menyimpan semua data ke file JSON.
        
        Menyimpan data_siswa dan pengeluaran_umum beserta timestamp
        terakhir update ke dalam file database JSON.
        
        Returns:
            bool: True jika berhasil menyimpan, False jika gagal
        """
        try:
            data = {
                'data_siswa': self.data_siswa,
                'pengeluaran_umum': self.pengeluaran_umum,
                'terakhir_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"{Colors.GREEN}✓ Data tersimpan{Colors.END}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}⚠ Gagal menyimpan!{Colors.END}")
            print(f"  {Colors.GRAY}Error: {e}{Colors.END}")
            return False
    
    def clear_screen(self):
        """
        Membersihkan layar terminal.
        
        Menggunakan perintah 'cls' untuk Windows dan 'clear' untuk Unix/Linux.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_box_header(self, title, icon=""):
        """
        Menampilkan header dengan desain box.
        
        Args:
            title (str): Judul yang akan ditampilkan
            icon (str): Emoji atau icon yang ditampilkan sebelum judul
        """
        print(f"\n{Colors.CYAN}╔{'═'*88}╗{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END}{Colors.BOLD}{Colors.WHITE} {icon} {title:<84}{Colors.END}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}╚{'═'*88}╝{Colors.END}")
    
    def print_section_header(self, title):
        """
        Menampilkan header section yang lebih kecil dari box header.
        
        Args:
            title (str): Judul section yang akan ditampilkan
        """
        print(f"\n{Colors.YELLOW}┌{'─'*88}┐{Colors.END}")
        print(f"{Colors.YELLOW}│{Colors.END}{Colors.BOLD} {title:<87}{Colors.END}{Colors.YELLOW}│{Colors.END}")
        print(f"{Colors.YELLOW}└{'─'*88}┘{Colors.END}")
    
    def print_separator(self, color=Colors.GRAY):
        """
        Menampilkan garis pemisah horizontal.
        
        Args:
            color (str): Kode warna ANSI untuk garis pemisah (default: GRAY)
        """
        print(f"{color}{'─'*90}{Colors.END}")
    
    def print_menu_item(self, number, title, icon="•"):
        """
        Menampilkan item menu dengan format yang konsisten.
        
        Args:
            number (str): Nomor menu
            title (str): Judul menu
            icon (str): Icon atau emoji untuk menu (default: "•")
        """
        print(f"  {Colors.CYAN}{icon}{Colors.END} {Colors.WHITE}{number}.{Colors.END} {title}")
    
    def pause(self):
        """
        Menghentikan eksekusi sementara dan menunggu user menekan Enter.
        
        Digunakan untuk memberi user waktu membaca output sebelum layar dibersihkan.
        """
        print(f"\n{Colors.GRAY}[Tekan Enter untuk lanjut]{Colors.END}", end="")
        input()
    
    def format_rupiah(self, nominal):
        """
        Memformat angka menjadi format mata uang Rupiah.
        
        Args:
            nominal (float): Nilai nominal yang akan diformat
            
        Returns:
            str: String dengan format "Rp X.XXX.XXX"
        """
        return f"Rp {nominal:,.0f}".replace(',', '.')
    
    def buat_tabel_dinamis(self, data_rows, headers=None, border_color=Colors.CYAN, text_color=Colors.WHITE):
        """
        Membuat tabel dengan lebar kolom yang menyesuaikan otomatis berdasarkan konten.
        
        Fungsi universal untuk membuat tabel yang rapi dengan:
        - Auto-sizing setiap kolom berdasarkan konten terpanjang
        - Border box yang rapi
        - Support untuk warna custom
        - Header opsional
        
        Args:
            data_rows (list): List of lists/tuples berisi data untuk setiap baris
                            Contoh: [['Lutfi', '5', 'Rp 50.000'], ['Kevin', '3', 'Rp 30.000']]
            headers (list): List berisi nama kolom header (opsional)
                            Contoh: ['Nama', 'Transaksi', 'Saldo']
            border_color (str): Warna untuk border tabel (default: CYAN)
            text_color (str): Warna untuk teks (default: WHITE)
        
        Returns:
            None (langsung print ke terminal)
        
        Example:
            >>> data = [
                    ['Total Siswa', ':', '34 orang'],
                    ['Sudah Bayar', ':', '0 orang (0%)'],
                    ['Belum Bayar', ':', '34 orang (100%)'],
                    ['Total Pemasukan', ':', 'Rp 0']
                ]
            >>> self.buat_tabel_dinamis(data, headers=['Keterangan', '', 'Nilai'])
        """
        if not data_rows:
            print(f"{Colors.YELLOW}⚠ Tidak ada data untuk ditampilkan{Colors.END}")
            return
        
        # Hitung jumlah kolom
        num_cols = len(data_rows[0]) if data_rows else 0
        if headers and len(headers) != num_cols:
            print(f"{Colors.RED}⚠ Jumlah header tidak sesuai dengan jumlah kolom!{Colors.END}")
            return
        
        # Hitung lebar maksimal untuk setiap kolom
        col_widths = [0] * num_cols
        
        # Cek lebar dari header
        if headers:
            for i, header in enumerate(headers):
                col_widths[i] = len(str(header))
        
        # Cek lebar dari setiap data row
        for row in data_rows:
            for i, cell in enumerate(row):
                # Hapus kode warna ANSI untuk menghitung panjang sebenarnya
                cell_str = str(cell)
                # Remove ANSI codes untuk perhitungan panjang
                import re
                clean_cell = re.sub(r'\033\[[0-9;]*m', '', cell_str)
                col_widths[i] = max(col_widths[i], len(clean_cell))
        
        # Tambah padding (2 spasi per sisi)
        col_widths = [w + 2 for w in col_widths]
        
        # Fungsi helper untuk membuat separator
        def buat_border(left, mid, right, line='─'):
            return f"{border_color}{left}{mid.join([line * w for w in col_widths])}{right}{Colors.END}"
        
        # Print border atas
        print(f"\n{buat_border('┌', '┬', '┐')}")
        
        # Print header jika ada
        if headers:
            header_cells = []
            for i, header in enumerate(headers):
                padded_header = f" {str(header):<{col_widths[i]-1}}"
                header_cells.append(f"{Colors.BOLD}{text_color}{padded_header}{Colors.END}")
            
            print(f"{border_color}│{Colors.END}" + f"{border_color}│{Colors.END}".join(header_cells) + f"{border_color}│{Colors.END}")
            print(buat_border('├', '┼', '┤'))
        
        # Print data rows
        for row in data_rows:
            row_cells = []
            for i, cell in enumerate(row):
                cell_str = str(cell)
                # Hitung panjang tanpa ANSI codes
                import re
                clean_cell = re.sub(r'\033\[[0-9;]*m', '', cell_str)
                
                # Hitung padding yang dibutuhkan
                padding_needed = col_widths[i] - len(clean_cell) - 1
                
                # Tambahkan padding
                if '\033[' in cell_str:  # Jika ada warna
                    padded_cell = f" {cell_str}{' ' * padding_needed}"
                else:
                    padded_cell = f" {text_color}{cell_str}{' ' * padding_needed}{Colors.END}"
                
                row_cells.append(padded_cell)
            
            print(f"{border_color}│{Colors.END}" + f"{border_color}│{Colors.END}".join(row_cells) + f"{border_color}│{Colors.END}")
        
        # Print border bawah
        print(buat_border('└', '┴', '┘'))
    
    def hitung_total_saldo(self):
        """
        Menghitung total saldo kas kelas saat ini.
        
        Total saldo = (Total pemasukan dari semua siswa) - (Total pengeluaran umum)
        
        Returns:
            float: Total saldo kas kelas
        """
        total = sum(siswa['saldo'] for siswa in self.data_siswa)
        return total - sum(p['jumlah'] for p in self.pengeluaran_umum)
    
    # ========== KELOLA SISWA ==========
    
    def tampilkan_daftar_siswa(self):
        """
        Menampilkan daftar semua siswa dalam format tabel multi-kolom.
        
        Menampilkan maksimal 10 siswa per kolom untuk readability yang lebih baik.
        Jika tidak ada siswa, menampilkan pesan peringatan.
        """
        self.print_box_header("DAFTAR SISWA", "👥")
        
        if not self.data_siswa:
            print(f"\n{Colors.YELLOW}⚠ Belum ada data siswa{Colors.END}")
            return
        
        # Tentukan jumlah baris per kolom (maksimal 10)
        rows_per_column = 10
        total_siswa = len(self.data_siswa)
        
        # Hitung jumlah kolom yang dibutuhkan
        num_columns = (total_siswa + rows_per_column - 1) // rows_per_column
        
        # Lebar setiap kolom
        col_width = 22
        
        # Print border atas
        border_top = "┌" + "┬".join(["─" * col_width for _ in range(num_columns)]) + "┐"
        print(f"\n{Colors.GRAY}{border_top}{Colors.END}")
        
        # Print data per baris
        for row in range(rows_per_column):
            row_data = []
            for col in range(num_columns):
                idx = col * rows_per_column + row
                if idx < total_siswa:
                    siswa_text = f"{Colors.CYAN}{idx+1:2}.{Colors.END} {self.data_siswa[idx]['nama']:<15}"
                    row_data.append(siswa_text)
                else:
                    row_data.append(" " * col_width)
            
            # Print baris dengan separator
            line = f"{Colors.GRAY}│{Colors.END} " + f" {Colors.GRAY}│{Colors.END} ".join(row_data) + f" {Colors.GRAY}│{Colors.END}"
            print(line)
        
        # Print border bawah
        border_bottom = "└" + "┴".join(["─" * col_width for _ in range(num_columns)]) + "┘"
        print(f"{Colors.GRAY}{border_bottom}{Colors.END}")
        
        print(f"\n{Colors.GREEN}Total: {len(self.data_siswa)} siswa{Colors.END}")
    
    def tambah_siswa(self):
        """
        Menambahkan siswa baru ke dalam sistem.
        
        Meminta input nama siswa dari user, melakukan validasi:
        - Nama tidak boleh kosong
        - Nama tidak boleh duplikat (case-insensitive)
        
        Jika valid, siswa baru ditambahkan dan daftar diurutkan alfabetis.
        """
        self.print_section_header("TAMBAH SISWA BARU")
        
        nama = input(f"\n{Colors.CYAN}→{Colors.END} Nama siswa: ").strip().title()
        
        if not nama:
            print(f"{Colors.RED}⚠ Nama tidak boleh kosong!{Colors.END}")
            return
        
        for siswa in self.data_siswa:
            if siswa['nama'].lower() == nama.lower():
                print(f"{Colors.RED}⚠ Nama '{nama}' sudah ada!{Colors.END}")
                return
        
        siswa_baru = {"nama": nama, "transaksi": [], "saldo": 0}
        self.data_siswa.append(siswa_baru)
        self.data_siswa.sort(key=lambda x: x['nama'])
        
        if self.save_data():
            print(f"\n{Colors.GREEN}✓ Siswa '{nama}' berhasil ditambahkan!{Colors.END}")
            print(f"  {Colors.GRAY}Total siswa: {len(self.data_siswa)} orang{Colors.END}")
    
    def edit_siswa(self):
        """
        Mengedit nama siswa yang sudah ada.
        
        Proses:
        1. Menampilkan daftar siswa untuk dipilih
        2. Meminta input nomor siswa yang akan diedit
        3. Menampilkan data siswa saat ini
        4. Meminta nama baru (dengan validasi duplikasi)
        5. Mengupdate nama dan mengurutkan ulang daftar
        
        User bisa membatalkan dengan memasukkan 0 atau string kosong.
        """
        if not self.data_siswa:
            print(f"\n{Colors.YELLOW}⚠ Belum ada siswa{Colors.END}")
            return
        
        self.tampilkan_daftar_siswa()
        
        try:
            nomor = int(input(f"\n{Colors.CYAN}→{Colors.END} Pilih nomor siswa (1-{len(self.data_siswa)}), 0=batal: "))
            
            if nomor == 0:
                return
            
            if nomor < 1 or nomor > len(self.data_siswa):
                print(f"{Colors.RED}⚠ Nomor tidak valid!{Colors.END}")
                return
            
            siswa = self.data_siswa[nomor - 1]
            nama_lama = siswa['nama']
            
            self.print_section_header("EDIT DATA SISWA")
            print(f"\n{Colors.GRAY}Nama saat ini:{Colors.END} {Colors.WHITE}{nama_lama}{Colors.END}")
            print(f"{Colors.GRAY}Transaksi:{Colors.END} {len(siswa['transaksi'])}")
            print(f"{Colors.GRAY}Saldo:{Colors.END} {Colors.GREEN}{self.format_rupiah(siswa['saldo'])}{Colors.END}")
            
            nama_baru = input(f"\n{Colors.CYAN}→{Colors.END} Nama baru (kosongkan jika batal): ").strip().title()
            
            if not nama_baru:
                print(f"{Colors.YELLOW}✓ Batal edit{Colors.END}")
                return
            
            # Cek duplikat nama (kecuali nama sendiri)
            for i, s in enumerate(self.data_siswa):
                if i != nomor - 1 and s['nama'].lower() == nama_baru.lower():
                    print(f"{Colors.RED}⚠ Nama '{nama_baru}' sudah digunakan siswa lain!{Colors.END}")
                    return
            
            # Update nama
            siswa['nama'] = nama_baru
            
            # Sort ulang berdasarkan nama
            self.data_siswa.sort(key=lambda x: x['nama'])
            
            if self.save_data():
                print(f"\n{Colors.GREEN}✓ Nama berhasil diubah!{Colors.END}")
                print(f"  {Colors.GRAY}Dari: {nama_lama}{Colors.END}")
                print(f"  {Colors.GRAY}Ke  : {nama_baru}{Colors.END}")
        
        except ValueError:
            print(f"{Colors.RED}⚠ Input tidak valid!{Colors.END}")
    
    def hapus_siswa(self):
        """
        Menghapus siswa dari sistem.
        
        Proses:
        1. Menampilkan daftar siswa
        2. Meminta input nomor siswa yang akan dihapus
        3. Jika siswa memiliki transaksi, meminta konfirmasi tambahan
        4. Menghapus siswa dari daftar
        
        Peringatan khusus diberikan jika siswa yang dihapus memiliki transaksi.
        """
        if not self.data_siswa:
            print(f"\n{Colors.YELLOW}⚠ Belum ada siswa{Colors.END}")
            return
        
        self.tampilkan_daftar_siswa()
        
        try:
            nomor = int(input(f"\n{Colors.CYAN}→{Colors.END} Pilih nomor (1-{len(self.data_siswa)}), 0=batal: "))
            
            if nomor == 0:
                return
            
            if nomor < 1 or nomor > len(self.data_siswa):
                print(f"{Colors.RED}⚠ Nomor tidak valid!{Colors.END}")
                return
            
            siswa = self.data_siswa[nomor - 1]
            
            if siswa['transaksi']:
                print(f"\n{Colors.YELLOW}⚠ '{siswa['nama']}' punya {len(siswa['transaksi'])} transaksi!{Colors.END}")
                print(f"  {Colors.GRAY}Saldo: {self.format_rupiah(siswa['saldo'])}{Colors.END}")
                konfirm = input(f"\n{Colors.RED}Tetap hapus? (y/n):{Colors.END} ")
                if konfirm.lower() != 'y':
                    return
            
            self.data_siswa.pop(nomor - 1)
            
            if self.save_data():
                print(f"\n{Colors.GREEN}✓ Siswa '{siswa['nama']}' dihapus!{Colors.END}")
        
        except ValueError:
            print(f"{Colors.RED}⚠ Input tidak valid!{Colors.END}")
    
    def kelola_siswa(self):
        """
        Menu utama untuk pengelolaan data siswa.
        
        Menyediakan submenu untuk:
        1. Lihat daftar siswa
        2. Tambah siswa baru
        3. Edit data siswa
        4. Hapus siswa
        
        Loop terus berjalan sampai user memilih untuk kembali.
        """
        while True:
            self.clear_screen()
            self.print_box_header("KELOLA DATA SISWA", "⚙️")
            
            print(f"\n{Colors.BOLD}Menu:{Colors.END}")
            self.print_menu_item("1", "Lihat Daftar Siswa", "👁️")
            self.print_menu_item("2", "Tambah Siswa", "➕")
            self.print_menu_item("3", "Edit Siswa", "✏️")
            self.print_menu_item("4", "Hapus Siswa", "🗑️")
            self.print_menu_item("0", "Kembali", "◀️")
            
            self.print_separator()
            
            pilihan = input(f"\n{Colors.CYAN}→{Colors.END} Pilih menu: ")
            
            if pilihan == '1':
                self.tampilkan_daftar_siswa()
                self.pause()
            elif pilihan == '2':
                self.tambah_siswa()
                self.pause()
            elif pilihan == '3':
                self.edit_siswa()
                self.pause()
            elif pilihan == '4':
                self.hapus_siswa()
                self.pause()
            elif pilihan == '0':
                break
            else:
                print(f"{Colors.RED}⚠ Pilihan tidak valid!{Colors.END}")
                self.pause()
    
    # ========== PILIH SISWA ==========
    
    def pilih_siswa(self):
        """
        Menampilkan daftar siswa dan meminta user memilih salah satu.
        
        Menampilkan siswa dalam format tabel multi-kolom untuk memudahkan pemilihan.
        
        Returns:
            int: Index siswa yang dipilih (0-based), atau None jika dibatalkan
        """
        self.print_section_header("PILIH SISWA")
        
        if not self.data_siswa:
            print(f"\n{Colors.RED}⚠ Belum ada data siswa!{Colors.END}")
            return None
        
        # Tentukan jumlah baris per kolom (maksimal 10)
        rows_per_column = 10
        total_siswa = len(self.data_siswa)
        
        # Hitung jumlah kolom yang dibutuhkan
        num_columns = (total_siswa + rows_per_column - 1) // rows_per_column
        
        # Lebar setiap kolom
        col_width = 22
        
        # Print border atas
        border_top = "┌" + "┬".join(["─" * col_width for _ in range(num_columns)]) + "┐"
        print(f"\n{Colors.GRAY}{border_top}{Colors.END}")
        
        # Print data per baris
        for row in range(rows_per_column):
            row_data = []
            for col in range(num_columns):
                idx = col * rows_per_column + row
                if idx < total_siswa:
                    siswa_text = f"{Colors.CYAN}{idx+1:2}.{Colors.END} {self.data_siswa[idx]['nama']:<15}"
                    row_data.append(siswa_text)
                else:
                    row_data.append(" " * col_width)
            
            # Print baris dengan separator
            line = f"{Colors.GRAY}│{Colors.END} " + f" {Colors.GRAY}│{Colors.END} ".join(row_data) + f" {Colors.GRAY}│{Colors.END}"
            print(line)
        
        # Print border bawah
        border_bottom = "└" + "┴".join(["─" * col_width for _ in range(num_columns)]) + "┘"
        print(f"{Colors.GRAY}{border_bottom}{Colors.END}")
        
        print(f"\n  {Colors.GRAY}0. Batal{Colors.END}")
        
        try:
            pilih = int(input(f"\n{Colors.CYAN}→{Colors.END} Pilih nomor siswa: "))
            if pilih == 0:
                return None
            if 1 <= pilih <= len(self.data_siswa):
                return pilih - 1
            print(f"{Colors.RED}⚠ Nomor tidak valid!{Colors.END}")
            return None
        except:
            print(f"{Colors.RED}⚠ Input tidak valid!{Colors.END}")
            return None
    
    # ========== TRANSAKSI ==========
    
    def setor_iuran(self):
        """
        Mencatat transaksi pemasukan (setoran) dari siswa.
        
        Proses:
        1. Memilih siswa yang akan menyetor
        2. Memasukkan jumlah setoran (harus > 0)
        3. Memilih jenis setoran dari menu atau input manual
        4. Menyimpan transaksi dan mengupdate saldo siswa
        
        Transaksi akan dicatat dengan timestamp saat ini.
        """
        self.clear_screen()
        self.print_box_header("SETOR IURAN", "💰")
        
        idx = self.pilih_siswa()
        if idx is None:
            print(f"{Colors.YELLOW}⚠ Batal{Colors.END}")
            return
        
        siswa = self.data_siswa[idx]
        
        print(f"\n{Colors.GRAY}┌{'─'*88}┐{Colors.END}")
        print(f"{Colors.GRAY}│{Colors.END} {Colors.BOLD}Siswa:{Colors.END} {siswa['nama']:<80} {Colors.GRAY}│{Colors.END}")
        print(f"{Colors.GRAY}│{Colors.END} {Colors.GRAY}Saldo:{Colors.END} {Colors.GREEN}{self.format_rupiah(siswa['saldo']):<80}{Colors.END} {Colors.GRAY}│{Colors.END}")
        print(f"{Colors.GRAY}└{'─'*88}┘{Colors.END}")
        
        try:
            jumlah = float(input(f"\n{Colors.CYAN}→{Colors.END} Jumlah (Rp): "))
            
            if jumlah <= 0:
                print(f"{Colors.RED}⚠ Jumlah harus > 0!{Colors.END}")
                return
            
            print(f"\n{Colors.BOLD}Jenis Setoran:{Colors.END}")
            print(f"  {Colors.CYAN}1.{Colors.END} Setoran Kas")
            print(f"  {Colors.CYAN}2.{Colors.END} Setoran Bulanan")
            print(f"  {Colors.CYAN}3.{Colors.END} Iuran Kegiatan")
            print(f"  {Colors.CYAN}4.{Colors.END} Donasi")
            print(f"  {Colors.CYAN}5.{Colors.END} Lainnya (isi manual)")
            
            pilih_ket = input(f"\n{Colors.CYAN}→{Colors.END} Pilih jenis (1-5, Enter=Setoran Tunai): ").strip()
            
            if pilih_ket == '2':
                keterangan = "Iuran Bulanan"
            elif pilih_ket == '3':
                keterangan = "Iuran Kegiatan"
            elif pilih_ket == '4':
                keterangan = "Donasi"
            elif pilih_ket == '5':
                keterangan = input(f"{Colors.CYAN}→{Colors.END} Keterangan: ").strip()
                if not keterangan:
                    keterangan = "Setoran Tunai"
            else:
                keterangan = "Setoran Tunai"
            
            transaksi = {
                "tanggal": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "jenis": "setor",
                "jumlah": jumlah,
                "keterangan": keterangan
            }
            
            siswa['transaksi'].append(transaksi)
            siswa['saldo'] += jumlah
            
            if self.save_data():
                print(f"\n{Colors.GREEN}╔{'═'*88}╗{Colors.END}")
                print(f"{Colors.GREEN}║{Colors.END} {Colors.BOLD}✓ PEMASUKAN BERHASIL DICATAT{Colors.END}{' '*59} {Colors.GREEN}║{Colors.END}")
                print(f"{Colors.GREEN}╠{'═'*88}╣{Colors.END}")
                print(f"{Colors.GREEN}║{Colors.END} {Colors.GRAY}Dari:{Colors.END} {siswa['nama']:<80} {Colors.GREEN}║{Colors.END}")
                print(f"{Colors.GREEN}║{Colors.END} {Colors.GRAY}Keterangan:{Colors.END} {keterangan:<75} {Colors.GREEN}║{Colors.END}")
                print(f"{Colors.GREEN}║{Colors.END} {Colors.GRAY}Jumlah:{Colors.END} {Colors.WHITE}{self.format_rupiah(jumlah):<79}{Colors.END} {Colors.GREEN}║{Colors.END}")
                print(f"{Colors.GREEN}║{Colors.END} {Colors.GRAY}Saldo {siswa['nama']}:{Colors.END} {Colors.WHITE}{self.format_rupiah(siswa['saldo']):<66}{Colors.END} {Colors.GREEN}║{Colors.END}")
                print(f"{Colors.GREEN}║{Colors.END} {Colors.GRAY}Total Kas:{Colors.END} {Colors.BOLD}{Colors.WHITE}{self.format_rupiah(self.hitung_total_saldo()):<74}{Colors.END} {Colors.GREEN}║{Colors.END}")
                print(f"{Colors.GREEN}╚{'═'*88}╝{Colors.END}")
        
        except ValueError:
            print(f"{Colors.RED}⚠ Input tidak valid!{Colors.END}")
    
    def tambah_pengeluaran(self):
        """
        Mencatat transaksi pengeluaran kas kelas.
        
        Proses:
        1. Menampilkan total saldo kas saat ini
        2. Memasukkan jumlah pengeluaran
        3. Memvalidasi apakah saldo cukup (dengan opsi lanjut jika minus)
        4. Memilih jenis pengeluaran dari menu atau input manual
        5. Menambahkan detail tambahan (opsional)
        6. Menyimpan transaksi pengeluaran
        
        Jika saldo tidak cukup, sistem akan memberi peringatan dan meminta konfirmasi.
        """
        self.clear_screen()
        self.print_box_header("TAMBAH PENGELUARAN", "💸")
        
        total_saldo = self.hitung_total_saldo()
        print(f"\n{Colors.GRAY}Total saldo kas:{Colors.END} {Colors.GREEN}{self.format_rupiah(total_saldo)}{Colors.END}")
        
        try:
            jumlah = float(input(f"\n{Colors.CYAN}→{Colors.END} Jumlah pengeluaran (Rp): "))
            
            if jumlah <= 0:
                print(f"{Colors.RED}⚠ Jumlah harus > 0!{Colors.END}")
                return
            
            if jumlah > total_saldo:
                print(f"\n{Colors.RED}⚠ Saldo tidak cukup!{Colors.END}")
                print(f"  {Colors.GRAY}Saldo: {self.format_rupiah(total_saldo)}{Colors.END}")
                print(f"  {Colors.GRAY}Kurang: {self.format_rupiah(jumlah - total_saldo)}{Colors.END}")
                konfirm = input(f"\n{Colors.YELLOW}Tetap lanjut (saldo minus)? (y/n):{Colors.END} ")
                if konfirm.lower() != 'y':
                    return
            
            print(f"\n{Colors.BOLD}Jenis Pengeluaran:{Colors.END}")
            print(f"  {Colors.CYAN}1.{Colors.END} Pembelian Alat Tulis")
            print(f"  {Colors.CYAN}2.{Colors.END} Biaya Kegiatan")
            print(f"  {Colors.CYAN}3.{Colors.END} Kebersihan Kelas")
            print(f"  {Colors.CYAN}4.{Colors.END} Biaya Administrasi")
            print(f"  {Colors.CYAN}5.{Colors.END} Biaya Fotokopi")
            print(f"  {Colors.CYAN}6.{Colors.END} Konsumsi")
            print(f"  {Colors.CYAN}7.{Colors.END} Lainnya (isi manual)")
            
            pilih_ket = input(f"\n{Colors.CYAN}→{Colors.END} Pilih jenis (1-7): ").strip()
            
            if pilih_ket == '1':
                ket = "Pembelian Alat Tulis"
            elif pilih_ket == '2':
                ket = "Biaya Kegiatan"
            elif pilih_ket == '3':
                ket = "Kebersihan Kelas"
            elif pilih_ket == '4':
                ket = "Biaya Administrasi"
            elif pilih_ket == '5':
                ket = "Biaya Fotokopi"
            elif pilih_ket == '6':
                ket = "Konsumsi"
            elif pilih_ket == '7':
                ket = input(f"{Colors.CYAN}→{Colors.END} Keterangan: ").strip()
                if not ket:
                    print(f"{Colors.RED}⚠ Keterangan wajib diisi!{Colors.END}")
                    return
            else:
                print(f"{Colors.RED}⚠ Pilihan tidak valid!{Colors.END}")
                return
            
            # Tambahan detail (opsional)
            detail = input(f"{Colors.CYAN}→{Colors.END} Detail tambahan (opsional, Enter=skip): ").strip()
            if detail:
                ket = f"{ket} - {detail}"
            
            pengeluaran = {
                "tanggal": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "keterangan": ket,
                "jumlah": jumlah
            }
            
            self.pengeluaran_umum.append(pengeluaran)
            
            if self.save_data():
                print(f"\n{Colors.RED}╔{'═'*88}╗{Colors.END}")
                print(f"{Colors.RED}║{Colors.END} {Colors.BOLD}✓ PENGELUARAN BERHASIL DICATAT{Colors.END}{' '*57} {Colors.RED}║{Colors.END}")
                print(f"{Colors.RED}╠{'═'*88}╣{Colors.END}")
                print(f"{Colors.RED}║{Colors.END} {Colors.GRAY}Keterangan:{Colors.END} {ket:<75} {Colors.RED}║{Colors.END}")
                print(f"{Colors.RED}║{Colors.END} {Colors.GRAY}Jumlah:{Colors.END} {Colors.WHITE}{self.format_rupiah(jumlah):<79}{Colors.END} {Colors.RED}║{Colors.END}")
                print(f"{Colors.RED}║{Colors.END} {Colors.GRAY}Saldo Kas:{Colors.END} {Colors.BOLD}{Colors.WHITE}{self.format_rupiah(self.hitung_total_saldo()):<76}{Colors.END} {Colors.RED}║{Colors.END}")
                print(f"{Colors.RED}╚{'═'*88}╝{Colors.END}")
        
        except ValueError:
            print(f"{Colors.RED}⚠ Input tidak valid!{Colors.END}")
    
    # ========== LAPORAN ==========
    def lihat_saldo(self):
        """
        Menampilkan ringkasan saldo kas kelas.
        
        Menampilkan:
        - Total pemasukan dari semua siswa
        - Total pengeluaran umum
        - Saldo akhir kas kelas
        - Detail saldo per siswa dalam format tabel
        - Statistik jumlah siswa dan total transaksi
        """
        self.clear_screen()
        self.print_box_header("RINGKASAN SALDO", "💵")
        
        total_pemasukan = sum(siswa['saldo'] for siswa in self.data_siswa)
        total_pengeluaran = sum(p['jumlah'] for p in self.pengeluaran_umum)
        saldo_akhir = total_pemasukan - total_pengeluaran
        
        # Data ringkasan utama
        ringkasan_utama = [
            [f"{Colors.GRAY}Total Pemasukan{Colors.END}", ":", f"{Colors.GREEN}{self.format_rupiah(total_pemasukan)}{Colors.END}"],
            [f"{Colors.GRAY}Total Pengeluaran{Colors.END}", ":", f"{Colors.RED}{self.format_rupiah(total_pengeluaran)}{Colors.END}"],
        ]
        
        # Tampilkan ringkasan utama
        self.buat_tabel_dinamis(ringkasan_utama, border_color=Colors.CYAN)
        
        # Detail saldo per siswa
        print(f"\n{Colors.BOLD}DETAIL SALDO PER SISWA{Colors.END}")
        
        siswa_data = []
        for i, siswa in enumerate(self.data_siswa, 1):
            saldo_color = Colors.GREEN if siswa['saldo'] > 0 else Colors.GRAY
            siswa_data.append([
                f"{Colors.CYAN}{i}{Colors.END}",
                siswa['nama'],
                f"{saldo_color}{self.format_rupiah(siswa['saldo'])}{Colors.END}"
            ])
        
        self.buat_tabel_dinamis(
            siswa_data,
            headers=['No', 'Nama', 'Saldo'],
            border_color=Colors.GRAY
        )
        
        # Saldo akhir dengan border lebih teb
        saldo_color = Colors.GREEN if saldo_akhir >= 0 else Colors.RED
        saldo_data = [
            [f"{Colors.BOLD}{Colors.WHITE}SALDO AKHIR{Colors.END}", ":", f"{saldo_color}{Colors.BOLD}{self.format_rupiah(saldo_akhir)}{Colors.END}"]
        ]
        
        print()  # Spasi
        self.buat_tabel_dinamis(saldo_data, border_color=Colors.GREEN if saldo_akhir >= 0 else Colors.RED)
        
        # Footer statistik
        print(f"\n{Colors.GRAY}• Jumlah Siswa: {Colors.WHITE}{len(self.data_siswa)} orang{Colors.END}")
        total_transaksi = sum(len(siswa['transaksi']) for siswa in self.data_siswa) + len(self.pengeluaran_umum)
        print(f"{Colors.GRAY}• Total Transaksi: {Colors.WHITE}{total_transaksi}{Colors.END}")


    def lihat_transaksi_siswa(self):
        """
        Menampilkan riwayat transaksi untuk siswa tertentu.
        
        Proses:
        1. Memilih siswa dari daftar
        2. Menampilkan informasi siswa (nama dan saldo)
        3. Menampilkan semua transaksi dalam format buku tabungan
            dengan kolom Debet (pengeluaran) dan Kredit (pemasukan)
        4. Menampilkan ringkasan total transaksi dan saldo akhir
        """
        self.clear_screen()
        self.print_box_header("TRANSAKSI PER SISWA", "📋")
        
        idx = self.pilih_siswa()
        if idx is None:
            return
        
        siswa = self.data_siswa[idx]
        
        print(f"\n{Colors.CYAN}╔{'═'*88}╗{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END} {Colors.BOLD}Nama:{Colors.END} {siswa['nama']:<81} {Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END} {Colors.BOLD}Saldo Akhir:{Colors.END} {Colors.GREEN}{self.format_rupiah(siswa['saldo']):<73}{Colors.END} {Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}╚{'═'*88}╝{Colors.END}")
        
        if not siswa['transaksi']:
            print(f"\n{Colors.YELLOW}⚠ Belum ada transaksi{Colors.END}")
            return
        
        # Header seperti buku tabungan
        print(f"\n{Colors.GRAY}{'No':<4} {'Tanggal':<20} {'Keterangan/Uraian':<30} {'Debet (DB)':<18} {'Kredit (KR)':<18}{Colors.END}")
        self.print_separator()
        
        saldo_berjalan = 0
        
        for i, t in enumerate(siswa['transaksi'], 1):
            tanggal = t['tanggal']
            jenis = t['jenis']
            jumlah = t['jumlah']
            ket = t.get('keterangan', 'Setoran Tunai' if jenis == 'setor' else 'Penarikan')
            
            # Tentukan Debet atau Kredit
            if jenis == 'setor':
                debet = '-'
                kredit = f"{Colors.GREEN}{self.format_rupiah(jumlah)}{Colors.END}"
                saldo_berjalan += jumlah
            else:
                debet = f"{Colors.RED}{self.format_rupiah(jumlah)}{Colors.END}"
                kredit = '-'
                saldo_berjalan -= jumlah
            
            print(f"{Colors.CYAN}{i:<4}{Colors.END} {tanggal:<20} {ket:<30} {debet:<28} {kredit:<28}")
        
        self.print_separator()
        print(f"\n{Colors.GRAY}• Total Transaksi: {Colors.WHITE}{len(siswa['transaksi'])}{Colors.END}")
        print(f"{Colors.GRAY}• Saldo Akhir: {Colors.GREEN}{self.format_rupiah(siswa['saldo'])}{Colors.END}")
    
    def lihat_semua_transaksi(self):
        """
        Menampilkan semua transaksi (pemasukan dan pengeluaran) dalam satu laporan.
        
        Menggabungkan:
        - Semua transaksi siswa (pemasukan)
        - Semua pengeluaran umum
        
        Transaksi diurutkan berdasarkan waktu (chronological order).
        Menampilkan tanggal, jam, nama, jenis, dan keterangan setiap transaksi.
        """
        self.clear_screen()
        self.print_box_header("SEMUA TRANSAKSI", "📊")
        
        # Kumpulkan semua transaksi dengan info lengkap
        semua_transaksi = []
        
        # Transaksi siswa
        for siswa in self.data_siswa:
            for t in siswa['transaksi']:
                semua_transaksi.append({
                    'tanggal': t['tanggal'],
                    'nama': siswa['nama'],
                    'jenis': 'Pemasukan',
                    'keterangan': t.get('keterangan', 'Setoran Tunai'),
                    'debet': '-',
                    'kredit': self.format_rupiah(t['jumlah']),
                    'is_income': True
                })
        
        # Pengeluaran umum
        for p in self.pengeluaran_umum:
            semua_transaksi.append({
                'tanggal': p['tanggal'],
                'nama': 'KAS UMUM',
                'jenis': 'Pengeluaran',
                'keterangan': p['keterangan'],
                'debet': self.format_rupiah(p['jumlah']),
                'kredit': '-',
                'is_income': False
            })
        
        # Urutkan berdasarkan tanggal (terlama ke terbaru)
        semua_transaksi.sort(key=lambda x: x['tanggal'])
        
        print(f"\n{Colors.GRAY}{'No':<4} {'Tanggal':<12} {'Jam':<10} {'Nama':<12} {'Jenis':<12} {'Keterangan':<25}{Colors.END}")
        self.print_separator()
        
        for no, t in enumerate(semua_transaksi, 1):
            # Pisahkan tanggal dan jam
            tanggal_obj = datetime.strptime(t['tanggal'], '%Y-%m-%d %H:%M:%S')
            tanggal = tanggal_obj.strftime('%d/%m/%Y')
            jam = tanggal_obj.strftime('%H:%M:%S')
            
            jenis_color = Colors.GREEN if t['is_income'] else Colors.RED
            
            print(f"{Colors.CYAN}{no:<4}{Colors.END} {tanggal:<12} {jam:<10} {t['nama']:<12} {jenis_color}{t['jenis']:<12}{Colors.END} {t['keterangan']:<25}")
        
        self.print_separator()
        print(f"\n{Colors.GRAY}• Total Transaksi: {Colors.WHITE}{len(semua_transaksi)}{Colors.END}")
        print(f"{Colors.GRAY}• Saldo Kas: {Colors.GREEN}{self.format_rupiah(self.hitung_total_saldo())}{Colors.END}")
    
    def lihat_laporan_siswa(self):
        """
        Menampilkan laporan status pembayaran semua siswa.
        
        Untuk setiap siswa menampilkan:
        - Nomor urut
        - Nama siswa
        - Jumlah transaksi
        - Saldo
        - Status (Sudah Bayar/Belum Bayar)
        
        Menampilkan ringkasan:
        - Total siswa
        - Jumlah dan persentase yang sudah bayar
        - Jumlah dan persentase yang belum bayar
        - Total pemasukan
        - Rata-rata iuran per siswa yang sudah bayar
        """
        self.clear_screen()
        self.print_box_header("LAPORAN STATUS SISWA", "📈")
        
        if not self.data_siswa:
            print(f"\n{Colors.YELLOW}⚠ Belum ada siswa{Colors.END}")
            return
        
        # Hitung statistik
        sudah_bayar = 0
        belum_bayar = 0
        total_kas = 0
        
        for siswa in self.data_siswa:
            if siswa['saldo'] > 0:
                sudah_bayar += 1
            else:
                belum_bayar += 1
            total_kas += siswa['saldo']
        
        # Hitung persentase
        persen_sudah = (sudah_bayar / len(self.data_siswa) * 100) if len(self.data_siswa) > 0 else 0
        persen_belum = (belum_bayar / len(self.data_siswa) * 100) if len(self.data_siswa) > 0 else 0
        
        # Data untuk tabel ringkasan
        ringkasan_data = [
            [f"{Colors.GRAY}Total Siswa{Colors.END}", ":", f"{Colors.WHITE}{len(self.data_siswa)} orang{Colors.END}"],
            [f"{Colors.GRAY}Sudah Bayar{Colors.END}", ":", f"{Colors.GREEN}{sudah_bayar} orang ({persen_sudah:.0f}%){Colors.END}"],
            [f"{Colors.GRAY}Belum Bayar{Colors.END}", ":", f"{Colors.YELLOW}{belum_bayar} orang ({persen_belum:.0f}%){Colors.END}"],
            [f"{Colors.GRAY}Total Pemasukan{Colors.END}", ":", f"{Colors.GREEN}{self.format_rupiah(total_kas)}{Colors.END}"]
        ]
        
        if sudah_bayar > 0:
            rata_rata = total_kas / sudah_bayar
            ringkasan_data.append([
                f"{Colors.GRAY}Rata-rata Iuran{Colors.END}", 
                ":", 
                f"{Colors.WHITE}{self.format_rupiah(rata_rata)}{Colors.END}"
            ])
        
        # Tampilkan tabel ringkasan dengan border cyan
        print(f"\n{Colors.BOLD}RINGKASAN{Colors.END}")
        self.buat_tabel_dinamis(ringkasan_data, border_color=Colors.CYAN)
        
        # Tampilkan detail per siswa
        print(f"\n{Colors.BOLD}DETAIL PER SISWA{Colors.END}")
        
        siswa_data = []
        for i, siswa in enumerate(self.data_siswa, 1):
            jml_transaksi = len(siswa['transaksi'])
            
            if siswa['saldo'] > 0:
                status = f"{Colors.GREEN}✓ Sudah Bayar{Colors.END}"
                saldo_display = f"{Colors.GREEN}{self.format_rupiah(siswa['saldo'])}{Colors.END}"
            else:
                status = f"{Colors.YELLOW}⚠ Belum Bayar{Colors.END}"
                saldo_display = f"{Colors.GRAY}{self.format_rupiah(siswa['saldo'])}{Colors.END}"
            
            siswa_data.append([
                f"{Colors.CYAN}{i}{Colors.END}",
                siswa['nama'],
                str(jml_transaksi),
                saldo_display,
                status
            ])
        
        # Tampilkan tabel siswa dengan header
        self.buat_tabel_dinamis(
            siswa_data, 
            headers=['No', 'Nama', 'Transaksi', 'Saldo', 'Status'],
            border_color=Colors.GRAY
        )
    
    # ========== RESET ==========
    
    def reset_transaksi(self):
        """
        Menghapus transaksi (pilihan: semua atau per siswa).
        
        Fungsi ini akan:
        - Pilihan 1: Hapus semua transaksi (reset total)
        - Pilihan 2: Hapus transaksi siswa tertentu
        - Data siswa TIDAK dihapus, hanya transaksinya
        
        Memerlukan konfirmasi untuk penghapusan.
        PERINGATAN: Proses ini tidak dapat dibatalkan!
        """
        self.clear_screen()
        print(f"\n{Colors.RED}╔{'═'*88}╗{Colors.END}")
        print(f"{Colors.RED}║{Colors.END}{Colors.BOLD}{Colors.RED} ⚠ RESET TRANSAKSI ⚠{Colors.END}{' '*66} {Colors.RED}║{Colors.END}")
        print(f"{Colors.RED}╚{'═'*88}╝{Colors.END}")
        
        print(f"\n{Colors.BOLD}PILIH JENIS RESET:{Colors.END}")
        print(f"{Colors.CYAN}1.{Colors.END} Hapus SEMUA transaksi")
        print(f"{Colors.CYAN}2.{Colors.END} Hapus transaksi SISWA TERTENTU")
        print(f"{Colors.CYAN}0.{Colors.END} Batal")
        
        pilihan = input(f"\n{Colors.YELLOW}Pilih [0-2]:{Colors.END} ")
        
        if pilihan == '1':
            self._reset_semua_transaksi()
        elif pilihan == '2':
            self._reset_transaksi_siswa()
        else:
            print(f"{Colors.GREEN}✓ Batal{Colors.END}")
    
    def _reset_semua_transaksi(self):
        """Helper: Reset semua transaksi"""
        self.clear_screen()
        print(f"\n{Colors.RED}╔{'═'*88}╗{Colors.END}")
        print(f"{Colors.RED}║{Colors.END}{Colors.BOLD}{Colors.RED} ⚠ RESET SEMUA TRANSAKSI ⚠{Colors.END}{' '*60} {Colors.RED}║{Colors.END}")
        print(f"{Colors.RED}╚{'═'*88}╝{Colors.END}")
        
        total_transaksi = sum(len(s['transaksi']) for s in self.data_siswa) + len(self.pengeluaran_umum)
        
        print(f"\n{Colors.YELLOW}Menghapus SEMUA transaksi!{Colors.END}")
        print(f"{Colors.GRAY}• Total transaksi: {Colors.WHITE}{total_transaksi}{Colors.END}")
        print(f"{Colors.GRAY}• Saldo: {Colors.WHITE}{self.format_rupiah(self.hitung_total_saldo())}{Colors.END}")
        print(f"\n{Colors.GREEN}⚠ Data siswa TIDAK dihapus{Colors.END}")
        print(f"{Colors.RED}⚠⚠⚠ TIDAK BISA dikembalikan! ⚠⚠⚠{Colors.END}")
        
        konfirm1 = input(f"\n{Colors.RED}Ketik 'RESET' untuk lanjut:{Colors.END} ")
        
        if konfirm1.upper() == 'RESET':
            konfirm2 = input(f"{Colors.RED}Ketik 'YAKIN' untuk konfirmasi:{Colors.END} ")
            
            if konfirm2.upper() == 'YAKIN':
                for siswa in self.data_siswa:
                    siswa['transaksi'] = []
                    siswa['saldo'] = 0
                
                self.pengeluaran_umum = []
                
                if self.save_data():
                    print(f"\n{Colors.RED}╔{'═'*88}╗{Colors.END}")
                    print(f"{Colors.RED}║{Colors.END} {Colors.BOLD}✓✓✓ SEMUA TRANSAKSI DIHAPUS! ✓✓✓{Colors.END}{' '*53} {Colors.RED}║{Colors.END}")
                    print(f"{Colors.RED}╚{'═'*88}╝{Colors.END}")
            else:
                print(f"{Colors.GREEN}✓ Batal{Colors.END}")
        else:
            print(f"{Colors.GREEN}✓ Batal{Colors.END}")
    
    def _reset_transaksi_siswa(self):
        """Helper: Reset transaksi siswa tertentu"""
        self.clear_screen()
        print(f"\n{Colors.YELLOW}╔{'═'*88}╗{Colors.END}")
        print(f"{Colors.YELLOW}║{Colors.END}{Colors.BOLD} 🗑 HAPUS TRANSAKSI SISWA{Colors.END}{' '*61} {Colors.YELLOW}║{Colors.END}")
        print(f"{Colors.YELLOW}╚{'═'*88}╝{Colors.END}")
        
        # Tampilkan daftar siswa
        print(f"\n{Colors.BOLD}DAFTAR SISWA:{Colors.END}")
        siswa_data = []
        for i, siswa in enumerate(self.data_siswa, 1):
            jumlah_transaksi = len(siswa['transaksi'])
            siswa_data.append([
                f"{Colors.CYAN}{i}{Colors.END}",
                siswa['nama'],
                f"{Colors.GRAY}{jumlah_transaksi} transaksi{Colors.END}",
                f"{Colors.GREEN if siswa['saldo'] > 0 else Colors.GRAY}{self.format_rupiah(siswa['saldo'])}{Colors.END}"
            ])
        
        self.buat_tabel_dinamis(
            siswa_data,
            headers=['No', 'Nama', 'Transaksi', 'Saldo'],
            border_color=Colors.GRAY
        )
        
        try:
            nomor = int(input(f"\n{Colors.YELLOW}Pilih nomor siswa [0=batal]:{Colors.END} "))
            
            if nomor == 0:
                print(f"{Colors.GREEN}✓ Batal{Colors.END}")
                return
            
            if 1 <= nomor <= len(self.data_siswa):
                siswa = self.data_siswa[nomor - 1]
                
                print(f"\n{Colors.RED}⚠ Akan menghapus transaksi:{Colors.END}")
                print(f"{Colors.GRAY}• Nama: {Colors.WHITE}{siswa['nama']}{Colors.END}")
                print(f"{Colors.GRAY}• Jumlah transaksi: {Colors.WHITE}{len(siswa['transaksi'])}{Colors.END}")
                print(f"{Colors.GRAY}• Saldo saat ini: {Colors.WHITE}{self.format_rupiah(siswa['saldo'])}{Colors.END}")
                print(f"{Colors.RED}• Saldo akan direset ke: Rp 0{Colors.END}")
                
                konfirm = input(f"\n{Colors.RED}Ketik 'HAPUS' untuk konfirmasi:{Colors.END} ")
                
                if konfirm.upper() == 'HAPUS':
                    siswa['transaksi'] = []
                    siswa['saldo'] = 0
                    
                    if self.save_data():
                        print(f"\n{Colors.GREEN}✓ Transaksi {siswa['nama']} berhasil dihapus!{Colors.END}")
                else:
                    print(f"{Colors.GREEN}✓ Batal{Colors.END}")
            else:
                print(f"{Colors.RED}✗ Nomor tidak valid{Colors.END}")
                
        except ValueError:
            print(f"{Colors.RED}✗ Input tidak valid{Colors.END}")
    
    # ========== MENU ==========
    
    def menu_utama(self):
        """
        Menampilkan dan mengelola menu utama aplikasi.
        
        Menu dibagi menjadi beberapa kategori:
        1. TRANSAKSI: Setor iuran dan tambah pengeluaran
        2. LAPORAN: Berbagai jenis laporan keuangan
        3. PENGATURAN: Kelola data siswa dan reset transaksi
        
        Loop akan terus berjalan hingga user memilih untuk keluar (0).
        Menampilkan informasi saldo kas dan lokasi database di footer.
        """
        input(f"\n{Colors.GRAY}[Tekan Enter untuk mulai]{Colors.END}")
        
        while True:
            self.clear_screen()
            
            # Header dengan box
            print(f"\n{Colors.CYAN}╔{'═'*88}╗{Colors.END}")
            print(f"{Colors.CYAN}║{Colors.END}{Colors.BOLD}{Colors.WHITE} 🏛️  KALCer - MENU UTAMA{Colors.END}{' '*59} {Colors.CYAN}║{Colors.END}")
            print(f"{Colors.CYAN}╚{'═'*88}╝{Colors.END}")
            
            # Menu Transaksi
            print(f"\n{Colors.YELLOW}┌─ TRANSAKSI {'─'*74}┐{Colors.END}")
            self.print_menu_item("1", "Setor Iuran", "💰")
            self.print_menu_item("2", "Tambah Pengeluaran", "💸")
            print(f"{Colors.YELLOW}└{'─'*88}┘{Colors.END}")
            
            # Menu Laporan
            print(f"\n{Colors.BLUE}┌─ LAPORAN {'─'*76}┐{Colors.END}")
            self.print_menu_item("3", "Lihat Saldo", "💵")
            self.print_menu_item("4", "Transaksi Per Siswa", "📋")
            self.print_menu_item("5", "Semua Transaksi", "📊")
            self.print_menu_item("6", "Laporan Status Siswa", "📈")
            print(f"{Colors.BLUE}└{'─'*88}┘{Colors.END}")
            
            # Menu Pengaturan
            print(f"\n{Colors.GRAY}┌─ PENGATURAN {'─'*73}┐{Colors.END}")
            self.print_menu_item("7", "Kelola Data Siswa", "⚙️")
            self.print_menu_item("8", "Reset Transaksi", "🗑️")
            print(f"{Colors.GRAY}└{'─'*88}┘{Colors.END}")
            
            # Exit
            print(f"\n  {Colors.RED}•{Colors.END} {Colors.WHITE}0.{Colors.END} Keluar")
            
            # Info Footer
            self.print_separator()
            saldo = self.hitung_total_saldo()
            saldo_color = Colors.GREEN if saldo >= 0 else Colors.RED
            print(f"{Colors.GRAY}Saldo Kas:{Colors.END} {saldo_color}{Colors.BOLD}{self.format_rupiah(saldo)}{Colors.END}")
            print(f"{Colors.GRAY}Database:{Colors.END} {self.filename}")
            self.print_separator()
            
            pilihan = input(f"\n{Colors.CYAN}→{Colors.END} Pilih menu: ")
            
            if pilihan == '1':
                self.setor_iuran()
                self.pause()
            elif pilihan == '2':
                self.tambah_pengeluaran()
                self.pause()
            elif pilihan == '3':
                self.lihat_saldo()
                self.pause()
            elif pilihan == '4':
                self.lihat_transaksi_siswa()
                self.pause()
            elif pilihan == '5':
                self.lihat_semua_transaksi()
                self.pause()
            elif pilihan == '6':
                self.lihat_laporan_siswa()
                self.pause()
            elif pilihan == '7':
                self.kelola_siswa()
            elif pilihan == '8':
                self.reset_transaksi()
                self.pause()
            elif pilihan == '0':
                self.clear_screen()
                print(f"\n{Colors.GREEN}╔{'═'*88}╗{Colors.END}")
                print(f"{Colors.GREEN}║{Colors.END} {Colors.BOLD}✓ Terima kasih telah menggunakan KALCer!{Colors.END}{' '*36} {Colors.GREEN}║{Colors.END}")
                print(f"{Colors.GREEN}║{Colors.END} {Colors.BOLD}by Team Persian SMKN 2 Bojonegoro{Colors.END}{' '*36} {Colors.GREEN}║{Colors.END}")
                print(f"{Colors.GREEN}╠{'═'*88}╣{Colors.END}")
                print(f"{Colors.GREEN}║{Colors.END} {Colors.GRAY}Data tersimpan di:{Colors.END}{' '*69} {Colors.GREEN}║{Colors.END}")
                print(f"{Colors.GREEN}║{Colors.END} {Colors.WHITE}{self.filename:<86}{Colors.END} {Colors.GREEN}║{Colors.END}")
                print(f"{Colors.GREEN}╚{'═'*88}╝{Colors.END}\n")
                break
            else:
                print(f"{Colors.RED}⚠ Pilihan tidak valid!{Colors.END}")
                self.pause()


def main():
    """
    Fungsi utama untuk menjalankan aplikasi.
    
    Menangani:
    - Inisialisasi objek KasKelas
    - Menjalankan menu utama
    - Exception handling untuk KeyboardInterrupt (Ctrl+C)
    - Exception handling untuk error umum lainnya
    
    Aplikasi akan terus berjalan hingga user memilih keluar atau menekan Ctrl+C.
    """
    try:
        kas = KasKelas()
        kas.menu_utama()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}✓ Program ditutup{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}⚠ Error: {e}{Colors.END}")
        input(f"\n{Colors.GRAY}[Tekan Enter untuk keluar]{Colors.END}")


if __name__ == "__main__":
    main()