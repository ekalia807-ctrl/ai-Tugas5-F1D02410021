import json

def load_kb(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def forward_chaining(kb):
    print(kb['judul'])
    print("Jawab y/t.\n")
    
    memori = set()
    fakta_awal = set()
    semua_syarat = set()
    hasil_aturan = set()
    
    for r in kb['aturan']:
        hasil_aturan.add(r['maka'])
        for syarat in r['jika']:
            semua_syarat.add(syarat)
            
    pertanyaan_dasar = sorted(list(semua_syarat - hasil_aturan))
    
    idx = 1
    for p in pertanyaan_dasar:
        ans = input(f"{idx}. Apakah {p}? (y/t) > ").lower()
        if ans == 'y':
            memori.add(p)
            fakta_awal.add(p)
        idx += 1
        
    print(f"\nFakta awal: {', '.join(fakta_awal) if fakta_awal else 'tidak ada'}\n")
    
    alasan = {}
    siklus = 1
    
    while True:
        aturan_baru = False
        
        for r in kb['aturan']:
            if r['maka'] not in memori:
                cocok = False
                if r['mode'] == 'dan':
                    cocok = all(syarat in memori for syarat in r['jika'])
                elif r['mode'] == 'atau':
                    cocok = any(syarat in memori for syarat in r['jika'])
                    
                if cocok:
                    memori.add(r['maka'])
                    alasan[r['maka']] = (r['id'], r['jika'])
                    print(f"Siklus {siklus}: {r['id']} -> {r['maka']}")
                    aturan_baru = True
                    
        if not aturan_baru:
            print(f"Siklus {siklus}: tidak ada aturan baru, berhenti\n")
            break
        siklus += 1
        
    kesimpulan = [k for k in memori if k in hasil_aturan and not any(k in r['jika'] for r in kb['aturan'])]
    
    if not kesimpulan:
        print("Kesimpulan: tidak ada (kasus negatif / tidak ada pemicu marah yang valid sesuai sistem)")
    else:
        print(f"Kesimpulan: {', '.join(kesimpulan)}")
        print("Alasan:")
        for k in kesimpulan:
            cetak_alasan(k, alasan, 1)
            
    print(f"\nCatatan: {kb['batas']}")

def cetak_alasan(maka, alasan_dict, level):
    if maka in alasan_dict:
        r_id, r_jika = alasan_dict[maka]
        indent = "  " * level
        print(f"{indent}{maka}  <- {r_id} ({', '.join(r_jika)})")
        for syarat in r_jika:
            cetak_alasan(syarat, alasan_dict, level + 1)

if __name__ == "__main__":
    kb = load_kb('kb_perempuan.json')
    forward_chaining(kb)