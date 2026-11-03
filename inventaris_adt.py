import time

class Product:
    """Kelas merepresentasikan entitas Produk dalam inventaris (ADT)."""
    def __init__(self, product_id, name, category, price, stock):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        
    def __str__(self):
        return f"ID: {self.product_id} | Nama: {self.name} | Kategori: {self.category} | Harga: Rp{self.price:,.2f} | Stok: {self.stock}"


class Node:
    """Node untuk implementasi Linked List kustom."""
    def __init__(self, product):
        self.product = product
        self.next = None


class InventoryManagementSystem:
    """Sistem Manajemen Inventaris Utama menggunakan Hash Table"""
    def __init__(self):
        # Struktur data utama tunggal untuk operasional sistem sehari-hari
        self.inventory = {}

    def add_product(self, product):
        """Penyisipan produk baru menggunakan Hash Table."""
        if product.product_id in self.inventory:
            return False, "Produk dengan ID tersebut sudah ada."
        self.inventory[product.product_id] = product
        return True, "Produk berhasil ditambahkan."

    def search_product(self, product_id):
        """Pencarian produk berdasarkan ID menggunakan Hash Table."""
        return self.inventory.get(product_id, None)

    def delete_product(self, product_id):
        """Penghapusan produk berdasarkan ID menggunakan Hash Table."""
        if product_id not in self.inventory:
            return False, "Produk tidak ditemukan dalam sistem."
        del self.inventory[product_id]
        return True, "Produk berhasil dihapus."

    def display_all(self, limit=10):
        """Traversal / Tampilan data inventaris."""
        items = list(self.inventory.values())
        if not items:
            print("Inventaris kosong.")
            return
        print(f"--- Menampilkan {min(limit, len(items))} dari total {len(items)} produk ---")
        for prod in items[:limit]:
            print(prod)


def run_benchmark():
    """Fungsi benchmark untuk menguji operasi utama"""
    print("\n==================================================================")
    print("=== BENCHMARK PERBANDINGAN STRUKTUR DATA AWAL VS ALTERNATIF ===")
    print("==================================================================")
    
    n_items = 2000
    print(f"Menyiapkan {n_items} data dummy untuk pengujian...")
    test_ids = [f"P{i:05d}" for i in range(n_items)]
    
    # -------------------------------------------------------------------------
    # OPERASI 1: PENYISIPAN (INSERTION)
    # -------------------------------------------------------------------------
    print("\n[1] Pengujian Operasi Penyisipan (Insertion):")
    
    # Hash Table
    dict_store = {}
    t0 = time.perf_counter()
    for pid in test_ids:
        p = Product(pid, f"Produk {pid}", "Elektronik", 100000.0, 50)
        dict_store[pid] = p
    t_dict_ins = time.perf_counter() - t0
    print(f"  - Hash Table [O(1) rata-rata] : {t_dict_ins:.6f} detik")
    
    # Python List
    list_store = []
    t0 = time.perf_counter()
    for pid in test_ids:
        p = Product(pid, f"Produk {pid}", "Elektronik", 100000.0, 50)
        list_store.append(p)
    t_list_ins = time.perf_counter() - t0
    print(f"  - Python List [O(1) append]: {t_list_ins:.6f} detik")

    # Linked List
    ll_head = None
    t0 = time.perf_counter()
    for pid in test_ids:
        p = Product(pid, f"Produk {pid}", "Elektronik", 100000.0, 50)
        new_node = Node(p)
        new_node.next = ll_head
        ll_head = new_node
    t_ll_ins = time.perf_counter() - t0
    print(f"  - Linked List [O(1) head] : {t_ll_ins:.6f} detik")

    # -------------------------------------------------------------------------
    # OPERASI 2: PENCARIAN (SEARCH)
    # -------------------------------------------------------------------------
    print("\n[2] Pengujian Operasi Pencarian (Search - Kasus Terburuk / Elemen Terakhir):")
    target_id = test_ids[-1]
    n_iter = 500
    
    # Hash Table Search
    t0 = time.perf_counter()
    for _ in range(n_iter):
        _ = dict_store.get(target_id)
    t_dict_search = time.perf_counter() - t0
    print(f"  - Hash Table Search ({n_iter}x) [O(1)]   : {t_dict_search:.6f} detik")
    
    # Python List Search
    t0 = time.perf_counter()
    for _ in range(n_iter):
        found = None
        for item in list_store:
            if item.product_id == target_id:
                found = item
                break
    t_list_search = time.perf_counter() - t0
    print(f"  - Python List Search ({n_iter}x) [O(N)] : {t_list_search:.6f} detik")
    
    # Linked List Search
    t0 = time.perf_counter()
    for _ in range(n_iter):
        curr = ll_head
        found = None
        while curr:
            if curr.product.product_id == target_id:
                found = curr.product
                break
            curr = curr.next
    t_ll_search = time.perf_counter() - t0
    print(f"  - Linked List Search ({n_iter}x) [O(N)]: {t_ll_search:.6f} detik")

    # -------------------------------------------------------------------------
    # OPERASI 3: PENGHAPUSAN (DELETION)
    # -------------------------------------------------------------------------
    print("\n[3] Pengujian Operasi Penghapusan (Deletion):")
    del_target = test_ids[100]
    
    d_dict = dict_store.copy()
    d_list = list(list_store)
    
    # Hash Table Delete
    t0 = time.perf_counter()
    if del_target in d_dict:
        del d_dict[del_target]
    t_dict_del = time.perf_counter() - t0
    print(f"  - Hash Table Delete [O(1)]          : {t_dict_del:.6f} detik")
    
    # Python List Delete
    t0 = time.perf_counter()
    d_list = [p for p in d_list if p.product_id != del_target]
    t_list_del = time.perf_counter() - t0
    print(f"  - Python List Delete [O(N)]         : {t_list_del:.6f} detik")
    
    # Linked List Delete
    t0 = time.perf_counter()
    curr = ll_head
    prev = None
    while curr:
        if curr.product.product_id == del_target:
            if prev is None:
                ll_head = curr.next
            else:
                prev.next = curr.next
            break
        prev = curr
        curr = curr.next
    t_ll_del = time.perf_counter() - t0
    print(f"  - Linked List Delete [O(N)]         : {t_ll_del:.6f} detik")

    # -------------------------------------------------------------------------
    # OPERASI 4: TAMPILAN DATA / TRAVERSAL (DISPLAY ALL)
    # -------------------------------------------------------------------------
    print("\n[4] Pengujian Operasi Tampilan Data / Traversal (Display All):")
    
    # Hash Table Traversal
    t0 = time.perf_counter()
    _ = list(dict_store.values())
    t_dict_disp = time.perf_counter() - t0
    print(f"  - Hash Table Traversal [O(N)]       : {t_dict_disp:.6f} detik")
    
    # Python List Traversal
    t0 = time.perf_counter()
    _ = [str(p) for p in list_store]
    t_list_disp = time.perf_counter() - t0
    print(f"  - Python List Traversal [O(N)]      : {t_list_disp:.6f} detik")
    
    # Linked List Traversal
    t0 = time.perf_counter()
    curr = ll_head
    while curr:
        _ = str(curr.product)
        curr = curr.next
    t_ll_disp = time.perf_counter() - t0
    print(f"  - Linked List Traversal [O(N)]     : {t_ll_disp:.6f} detik")
    print("==================================================================")


def main():
    ims = InventoryManagementSystem()
    
    initial_products = [
        Product("P0001", "Laptop ASUS ROG", "Komputer", 15000000.0, 10),
        Product("P0002", "Smartphone Samsung S24", "Handphone", 12000000.0, 25),
        Product("P0003", "Mechanical Keyboard Keychron", "Aksesoris", 1200000.0, 40),
        Product("P0004", "Mouse Gaming Logitech", "Aksesoris", 650000.0, 60),
        Product("P0005", "Monitor LG UltraWide", "Komputer", 3500000.0, 15)
    ]
    for p in initial_products:
        ims.add_product(p)

    while True:
        print("\n==============================================")
        print("   SISTEM MANAJEMEN INVENTARIS E-COMMERCE     ")
        print("==============================================")
        print("1. Tambah Produk Baru")
        print("2. Cari Detail Produk (Berdasarkan ID)")
        print("3. Hapus Produk")
        print("4. Tampilkan Daftar Produk")
        print("5. Jalankan Benchmark 4 Operasi (Hash Table vs Alternatif)")
        print("0. Keluar")
        
        choice = input("Pilih menu (0-5): ").strip()
        
        if choice == '1':
            pid = input("Masukkan ID Produk (contoh: P006): ").strip()
            name = input("Masukkan Nama Produk: ").strip()
            cat = input("Masukkan Kategori: ").strip()
            try:
                price = float(input("Masukkan Harga (Rp): "))
                stock = int(input("Masukkan Jumlah Stok: "))
            except ValueError:
                print("Error: Harga dan stok harus berupa angka.")
                continue
            
            new_prod = Product(pid, name, cat, price, stock)
            success, msg = ims.add_product(new_prod)
            print(f">> {msg}")
            
        elif choice == '2':
            pid = input("Masukkan ID Produk yang dicari: ").strip()
            t0 = time.perf_counter()
            res = ims.search_product(pid)
            t_exec = time.perf_counter() - t0
            
            if res:
                print(f"Produk Ditemukan: {res}")
                print(f"[Waktu Eksekusi Hash Table] {t_exec:.8f} detik")
            else:
                print("Produk tidak ditemukan dalam sistem.")
                
        elif choice == '3':
            pid = input("Masukkan ID Produk yang akan dihapus: ").strip()
            success, msg = ims.delete_product(pid)
            print(f">> {msg}")
            
        elif choice == '4':
            ims.display_all()
            
        elif choice == '5':
            run_benchmark()
            
        elif choice == '0':
            print("Terima kasih telah menggunakan Sistem Manajemen Inventaris.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()