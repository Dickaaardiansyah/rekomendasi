"""
Data statis: mata pelajaran, soal RIASEC, dan konfigurasi kurikulum
Berdasarkan Kurikulum Merdeka (Permendikbudristek No. 12 Tahun 2024)
"""

# ─── Mata Pelajaran Pilihan (Kurikulum Merdeka) ───────────────────────────────
SUBJECTS = [
    # Kelompok MIPA
    {'id': 1,  'name': 'Matematika Tingkat Lanjut', 'category': 'IPA',      'group': 'MIPA',   'icon': '📐', 'min_grade': 75},
    {'id': 2,  'name': 'Fisika',                    'category': 'IPA',      'group': 'MIPA',   'icon': '⚛️', 'min_grade': 70},
    {'id': 3,  'name': 'Kimia',                     'category': 'IPA',      'group': 'MIPA',   'icon': '🧪', 'min_grade': 70},
    {'id': 4,  'name': 'Biologi',                   'category': 'IPA',      'group': 'MIPA',   'icon': '🔬', 'min_grade': 70},
    # Kelompok IPS
    {'id': 5,  'name': 'Ekonomi',                   'category': 'IPS',      'group': 'IPS',    'icon': '💹', 'min_grade': 65},
    {'id': 6,  'name': 'Sosiologi',                 'category': 'IPS',      'group': 'IPS',    'icon': '👥', 'min_grade': 65},
    {'id': 7,  'name': 'Geografi',                  'category': 'IPS',      'group': 'IPS',    'icon': '🗺️', 'min_grade': 65},
    {'id': 8,  'name': 'Sejarah',                   'category': 'IPS',      'group': 'IPS',    'icon': '📜', 'min_grade': 65},
    {'id': 9,  'name': 'Antropologi',               'category': 'IPS',      'group': 'IPS',    'icon': '🏛️', 'min_grade': 65},
    # Kelompok Bahasa
    {'id': 10, 'name': 'Bahasa dan Sastra Indonesia','category': 'Bahasa',  'group': 'Bahasa', 'icon': '📝', 'min_grade': 70},
    {'id': 11, 'name': 'Bahasa dan Sastra Inggris', 'category': 'Bahasa',   'group': 'Bahasa', 'icon': '🌐', 'min_grade': 70},
    # Kelompok Vokasi & Teknologi
    {'id': 12, 'name': 'Informatika',               'category': 'Teknologi','group': 'Vokasi', 'icon': '💻', 'min_grade': 70},
    {'id': 13, 'name': 'Prakarya & Kewirausahaan',  'category': 'Vokasi',   'group': 'Vokasi', 'icon': '🛠️', 'min_grade': 60},
    # Kelompok Umum (wajib, untuk referensi)
    {'id': 14, 'name': 'Pendidikan Kewarganegaraan','category': 'Umum',     'group': 'Wajib',  'icon': '🏛️', 'min_grade': 65},
]

# ─── Paket Rekomendasi berdasarkan Jalur Karir ────────────────────────────────
CAREER_PACKAGES = {
    'kedokteran': {
        'label': 'Kedokteran & Kesehatan',
        'icon': '🩺',
        'subjects': ['Biologi', 'Kimia', 'Matematika Tingkat Lanjut'],
        'optional': ['Fisika'],
        'description': 'Cocok untuk calon dokter, dokter gigi, apoteker, perawat, dan tenaga kesehatan lainnya.',
        'universities': ['FK UI', 'FK UGM', 'FK UNAIR', 'FK UNDIP'],
    },
    'teknik': {
        'label': 'Teknik & Rekayasa',
        'icon': '⚙️',
        'subjects': ['Matematika Tingkat Lanjut', 'Fisika', 'Informatika'],
        'optional': ['Kimia'],
        'description': 'Untuk calon insinyur, arsitek, dan profesional di bidang teknik.',
        'universities': ['FT UI', 'FT ITS', 'FT ITB', 'FT UGM'],
    },
    'ekonomi_bisnis': {
        'label': 'Ekonomi & Bisnis',
        'icon': '💼',
        'subjects': ['Ekonomi', 'Matematika Tingkat Lanjut', 'Sosiologi'],
        'optional': ['Geografi'],
        'description': 'Persiapan untuk studi manajemen, akuntansi, keuangan, dan bisnis.',
        'universities': ['FEB UI', 'FEB UGM', 'FEB UNAIR'],
    },
    'sosial_humaniora': {
        'label': 'Ilmu Sosial & Humaniora',
        'icon': '🌏',
        'subjects': ['Sosiologi', 'Sejarah', 'Antropologi'],
        'optional': ['Geografi', 'Bahasa dan Sastra Indonesia'],
        'description': 'Untuk calon ilmuwan sosial, peneliti, dan pegiat humaniora.',
        'universities': ['FISIP UI', 'FISIPOL UGM', 'Fak. Hukum'],
    },
    'bahasa_sastra': {
        'label': 'Bahasa, Sastra & Komunikasi',
        'icon': '✍️',
        'subjects': ['Bahasa dan Sastra Indonesia', 'Bahasa dan Sastra Inggris', 'Sosiologi'],
        'optional': ['Sejarah', 'Antropologi'],
        'description': 'Untuk calon penulis, jurnalis, penerjemah, dan diplomat.',
        'universities': ['FIB UI', 'FIB UGM', 'Fak. Komunikasi'],
    },
    'sains_murni': {
        'label': 'Sains & Penelitian',
        'icon': '🔭',
        'subjects': ['Fisika', 'Kimia', 'Biologi', 'Matematika Tingkat Lanjut'],
        'optional': ['Informatika'],
        'description': 'Untuk calon peneliti, ilmuwan, dan akademisi di bidang sains.',
        'universities': ['FMIPA UI', 'FMIPA UGM', 'FMIPA ITB'],
    },
    'teknologi_informasi': {
        'label': 'Teknologi Informasi',
        'icon': '🖥️',
        'subjects': ['Informatika', 'Matematika Tingkat Lanjut', 'Fisika'],
        'optional': ['Kimia'],
        'description': 'Untuk calon programmer, data scientist, dan profesional IT.',
        'universities': ['FILKOM UB', 'IF ITS', 'Fasilkom UI'],
    },
}

# ─── Soal Tes RIASEC (30 soal, 5 per dimensi) ─────────────────────────────────
RIASEC_QUESTIONS = [
    # Realistic (R)
    {"id": 1,  "text": "Saya suka bekerja dengan mesin, alat, atau peralatan teknis",            "type": "realistic",      "dimension": "R"},
    {"id": 2,  "text": "Saya menikmati kegiatan yang bersifat fisik atau manual",                "type": "realistic",      "dimension": "R"},
    {"id": 3,  "text": "Saya lebih suka bekerja di luar ruangan daripada di balik meja",         "type": "realistic",      "dimension": "R"},
    {"id": 4,  "text": "Saya suka memperbaiki barang yang rusak atau membuat sesuatu dari awal", "type": "realistic",      "dimension": "R"},
    {"id": 5,  "text": "Saya tertarik pada bidang pertanian, kehutanan, atau lingkungan hidup",  "type": "realistic",      "dimension": "R"},
    # Investigative (I)
    {"id": 6,  "text": "Saya suka memecahkan masalah yang kompleks dan membutuhkan analisis",    "type": "investigative",  "dimension": "I"},
    {"id": 7,  "text": "Saya tertarik melakukan eksperimen atau penelitian ilmiah",              "type": "investigative",  "dimension": "I"},
    {"id": 8,  "text": "Saya suka membaca artikel ilmiah atau buku-buku pengetahuan",            "type": "investigative",  "dimension": "I"},
    {"id": 9,  "text": "Saya suka menganalisis data dan mencari pola di dalamnya",               "type": "investigative",  "dimension": "I"},
    {"id": 10, "text": "Saya senang berpikir kritis dan mengevaluasi suatu pernyataan",          "type": "investigative",  "dimension": "I"},
    # Artistic (A)
    {"id": 11, "text": "Saya suka menulis cerita, puisi, atau karya sastra",                    "type": "artistic",       "dimension": "A"},
    {"id": 12, "text": "Saya menikmati melukis, menggambar, atau kegiatan seni visual lainnya", "type": "artistic",       "dimension": "A"},
    {"id": 13, "text": "Saya suka bermain musik atau menyanyi",                                 "type": "artistic",       "dimension": "A"},
    {"id": 14, "text": "Saya tertarik pada desain grafis, fashion, atau arsitektur",             "type": "artistic",       "dimension": "A"},
    {"id": 15, "text": "Saya suka berekspresi dan berkreasi tanpa batas aturan yang ketat",     "type": "artistic",       "dimension": "A"},
    # Social (S)
    {"id": 16, "text": "Saya senang membantu orang lain yang sedang mengalami kesulitan",       "type": "social",         "dimension": "S"},
    {"id": 17, "text": "Saya menikmati mengajar, melatih, atau membimbing orang lain",          "type": "social",         "dimension": "S"},
    {"id": 18, "text": "Saya merasa puas saat bekerja dalam tim dan berkolaborasi",              "type": "social",         "dimension": "S"},
    {"id": 19, "text": "Saya tertarik pada isu sosial, kemanusiaan, dan lingkungan",             "type": "social",         "dimension": "S"},
    {"id": 20, "text": "Saya suka mendengarkan cerita dan masalah orang lain",                  "type": "social",         "dimension": "S"},
    # Enterprising (E)
    {"id": 21, "text": "Saya suka memimpin kelompok atau organisasi",                           "type": "enterprising",   "dimension": "E"},
    {"id": 22, "text": "Saya tertarik pada dunia bisnis, investasi, dan kewirausahaan",         "type": "enterprising",   "dimension": "E"},
    {"id": 23, "text": "Saya menikmati berbicara di depan umum atau presentasi",                "type": "enterprising",   "dimension": "E"},
    {"id": 24, "text": "Saya suka meyakinkan dan mempengaruhi orang lain",                      "type": "enterprising",   "dimension": "E"},
    {"id": 25, "text": "Saya termotivasi oleh tantangan, persaingan, dan pencapaian",           "type": "enterprising",   "dimension": "E"},
    # Conventional (C)
    {"id": 26, "text": "Saya suka bekerja dengan data, angka, dan spreadsheet",                 "type": "conventional",   "dimension": "C"},
    {"id": 27, "text": "Saya menyukai pekerjaan yang terstruktur dengan prosedur yang jelas",   "type": "conventional",   "dimension": "C"},
    {"id": 28, "text": "Saya teliti dalam mengikuti instruksi dan aturan",                      "type": "conventional",   "dimension": "C"},
    {"id": 29, "text": "Saya suka mengelola arsip, dokumen, atau administrasi",                 "type": "conventional",   "dimension": "C"},
    {"id": 30, "text": "Saya lebih suka tugas yang terorganisir daripada yang terbuka",         "type": "conventional",   "dimension": "C"},
]

# ─── Deskripsi Tipe RIASEC ────────────────────────────────────────────────────
RIASEC_DESCRIPTIONS = {
    'realistic': {
        'label': 'Realistic (R)',
        'title': 'Si Praktis',
        'color': '#2ecc71',
        'description': 'Kamu menyukai pekerjaan konkret, teknis, dan berbasis keterampilan tangan. Kamu cenderung langsung dan to-the-point.',
        'careers': ['Insinyur', 'Teknisi', 'Petani', 'Militer', 'Mekanik'],
    },
    'investigative': {
        'label': 'Investigative (I)',
        'title': 'Si Peneliti',
        'color': '#3498db',
        'description': 'Kamu analitis, intelektual, dan penasaran. Kamu suka memecahkan masalah kompleks dan berpikir mendalam.',
        'careers': ['Ilmuwan', 'Dokter', 'Analis Data', 'Programmer', 'Peneliti'],
    },
    'artistic': {
        'label': 'Artistic (A)',
        'title': 'Si Kreatif',
        'color': '#9b59b6',
        'description': 'Kamu imajinatif, ekspresif, dan orisinal. Kamu menyukai kebebasan berkreasi dan menghindari rutinitas.',
        'careers': ['Desainer', 'Penulis', 'Musisi', 'Fotografer', 'Seniman'],
    },
    'social': {
        'label': 'Social (S)',
        'title': 'Si Penolong',
        'color': '#e67e22',
        'description': 'Kamu peduli, kooperatif, dan berorientasi pada orang. Kamu senang membantu dan berinteraksi dengan orang lain.',
        'careers': ['Guru', 'Psikolog', 'Dokter', 'Konselor', 'Pekerja Sosial'],
    },
    'enterprising': {
        'label': 'Enterprising (E)',
        'title': 'Si Pemimpin',
        'color': '#e74c3c',
        'description': 'Kamu percaya diri, ambisius, dan suka memimpin. Kamu termotivasi oleh pencapaian dan pengakuan.',
        'careers': ['Pengusaha', 'Manajer', 'Politisi', 'Pengacara', 'Sales'],
    },
    'conventional': {
        'label': 'Conventional (C)',
        'title': 'Si Teratur',
        'color': '#1abc9c',
        'description': 'Kamu teliti, terorganisir, dan efisien. Kamu menyukai struktur, rutinitas, dan kejelasan tugas.',
        'careers': ['Akuntan', 'Admin', 'Bankir', 'Arsiparis', 'Analis Keuangan'],
    },
}