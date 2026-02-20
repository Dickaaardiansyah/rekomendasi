"""
SAW (Simple Additive Weighting) Calculator
Metode pengambilan keputusan multi-kriteria untuk rekomendasi mata pelajaran
"""

import numpy as np
from typing import List, Dict, Tuple, Optional


class SAWCalculator:
    """
    Implementasi Metode SAW (Simple Additive Weighting)
    
    Langkah-langkah:
    1. Tentukan kriteria dan bobot
    2. Buat matriks keputusan
    3. Normalisasi matriks
    4. Hitung nilai preferensi (weighted sum)
    5. Ranking alternatif
    """

    def __init__(self):
        self.weights: Optional[np.ndarray] = None
        self.criteria_types: Optional[List[str]] = None
        self.criteria_names: Optional[List[str]] = None

    def set_criteria(
        self,
        weights: List[float],
        types: List[str],
        names: Optional[List[str]] = None
    ):
        """
        Set kriteria, bobot, dan tipe (benefit/cost)

        Args:
            weights: Bobot tiap kriteria (total harus = 1)
            types: 'benefit' atau 'cost' per kriteria
            names: Nama kriteria (opsional, untuk laporan)
        """
        self.weights = np.array(weights, dtype=float)
        self.criteria_types = types
        self.criteria_names = names or [f"C{i+1}" for i in range(len(weights))]

        if len(weights) != len(types):
            raise ValueError("Jumlah weights harus sama dengan jumlah types")

        total = round(float(np.sum(self.weights)), 6)
        if not np.isclose(total, 1.0, atol=1e-4):
            raise ValueError(f"Total bobot harus 1.0, saat ini: {total}")

    def normalize(self, matrix: np.ndarray) -> np.ndarray:
        """
        Normalisasi matriks keputusan menggunakan metode SAW

        - Benefit: r_ij = x_ij / max(x_j)
        - Cost:    r_ij = min(x_j) / x_ij
        """
        normalized = np.zeros_like(matrix, dtype=float)

        for j in range(matrix.shape[1]):
            col = matrix[:, j].astype(float)

            if self.criteria_types[j] == 'benefit':
                max_val = np.max(col)
                if max_val != 0:
                    normalized[:, j] = col / max_val
                else:
                    normalized[:, j] = 0.0
            else:  # cost
                min_val = np.min(col)
                with np.errstate(divide='ignore', invalid='ignore'):
                    normalized[:, j] = np.where(col != 0, min_val / col, 0.0)

        return normalized

    def calculate(self, matrix: np.ndarray) -> Dict:
        """
        Hitung nilai SAW lengkap dengan detail perhitungan

        Returns:
            Dict berisi final_scores, normalized_matrix, weighted_matrix, ranks
        """
        if self.weights is None or self.criteria_types is None:
            raise RuntimeError("Kriteria belum di-set. Panggil set_criteria() terlebih dahulu.")

        matrix = np.array(matrix, dtype=float)
        normalized_matrix = self.normalize(matrix)
        weighted_matrix = normalized_matrix * self.weights
        final_scores = np.sum(weighted_matrix, axis=1)
        ranks = self._rank(final_scores)

        return {
            'raw_matrix': matrix.tolist(),
            'normalized_matrix': normalized_matrix.tolist(),
            'weighted_matrix': weighted_matrix.tolist(),
            'final_scores': final_scores.tolist(),
            'ranks': ranks.tolist(),
            'criteria_names': self.criteria_names,
            'weights': self.weights.tolist(),
        }

    def _rank(self, scores: np.ndarray) -> np.ndarray:
        """Beri peringkat: nilai tertinggi = rank 1"""
        sorted_indices = np.argsort(scores)[::-1]
        ranks = np.zeros(len(scores), dtype=int)
        for rank_pos, idx in enumerate(sorted_indices, 1):
            ranks[idx] = rank_pos
        return ranks

    def recommend_subjects(
        self,
        student_data: Dict,
        subjects_data: List[Dict],
        weights: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Rekomendasi mata pelajaran dengan kriteria multi-faktor:
        1. Nilai Akademik Rapor (C1) - Benefit
        2. Kecocokan RIASEC (C2) - Benefit
        3. Relevansi Cita-cita (C3) - Benefit [BARU]
        4. Popularitas di Sekolah (C4) - Benefit [BARU]

        Args:
            student_data: grades, riasec_scores, aspiration (cita-cita)
            subjects_data: List mata pelajaran
            weights: Custom bobot {academic, riasec, aspiration, availability}
        """
        # Default weights
        w = weights or {
            'academic': 0.40,
            'riasec': 0.30,
            'aspiration': 0.20,
            'availability': 0.10
        }

        self.set_criteria(
            weights=[w['academic'], w['riasec'], w['aspiration'], w['availability']],
            types=['benefit', 'benefit', 'benefit', 'benefit'],
            names=['Nilai Akademik', 'Kecocokan RIASEC', 'Relevansi Cita-cita', 'Ketersediaan']
        )

        grades = student_data.get('grades', {})
        riasec = student_data.get('riasec_scores', {})
        aspiration = student_data.get('aspiration', '')

        matrix = []
        alternatives = []

        for subject in subjects_data:
            name = subject['name']
            alternatives.append(name)

            # C1: Nilai akademik (0-100 -> 0-1)
            academic_score = grades.get(name, 0) / 100.0

            # C2: Kecocokan RIASEC
            riasec_match = _calculate_riasec_match(name, riasec)

            # C3: Relevansi cita-cita
            aspiration_score = _calculate_aspiration_score(name, aspiration)

            # C4: Ketersediaan di sekolah (simulasi berdasarkan kategori)
            availability = _get_subject_availability(subject)

            matrix.append([academic_score, riasec_match, aspiration_score, availability])

        result = self.calculate(np.array(matrix))

        recommendations = []
        for i, subject in enumerate(alternatives):
            cat = next((s['category'] for s in subjects_data if s['name'] == subject), '-')
            recommendations.append({
                'subject': subject,
                'category': cat,
                'rank': result['ranks'][i],
                'score': round(result['final_scores'][i], 4),
                'academic_score': round(matrix[i][0] * 100, 1),
                'riasec_match': round(matrix[i][1] * 100, 1),
                'aspiration_score': round(matrix[i][2] * 100, 1),
                'availability': round(matrix[i][3] * 100, 1),
                'normalized': {
                    'academic': round(result['normalized_matrix'][i][0], 4),
                    'riasec': round(result['normalized_matrix'][i][1], 4),
                    'aspiration': round(result['normalized_matrix'][i][2], 4),
                    'availability': round(result['normalized_matrix'][i][3], 4),
                },
                'weighted': {
                    'academic': round(result['weighted_matrix'][i][0], 4),
                    'riasec': round(result['weighted_matrix'][i][1], 4),
                    'aspiration': round(result['weighted_matrix'][i][2], 4),
                    'availability': round(result['weighted_matrix'][i][3], 4),
                }
            })

        recommendations.sort(key=lambda x: x['rank'])
        return recommendations


# ─── Helpers ─────────────────────────────────────────────────────────────────

# Pemetaan mata pelajaran -> tipe RIASEC yang cocok
SUBJECT_RIASEC_MAP = {
    'Matematika Tingkat Lanjut': ['investigative', 'conventional'],
    'Matematika': ['investigative', 'conventional'],
    'Fisika': ['investigative', 'realistic'],
    'Kimia': ['investigative', 'realistic'],
    'Biologi': ['investigative', 'social'],
    'Sejarah': ['social', 'artistic'],
    'Geografi': ['realistic', 'investigative'],
    'Ekonomi': ['enterprising', 'conventional'],
    'Sosiologi': ['social', 'artistic'],
    'Bahasa Indonesia': ['artistic', 'social'],
    'Bahasa Inggris': ['artistic', 'social'],
    'Bahasa dan Sastra Indonesia': ['artistic', 'social'],
    'Bahasa dan Sastra Inggris': ['artistic', 'social'],
    'Pendidikan Kewarganegaraan': ['social', 'enterprising'],
    'Informatika': ['investigative', 'realistic', 'conventional'],
    'Prakarya & Kewirausahaan': ['enterprising', 'realistic'],
    'Antropologi': ['social', 'investigative'],
}

# Pemetaan cita-cita -> mata pelajaran yang relevan (berdasarkan kurikulum Merdeka)
ASPIRATION_SUBJECT_MAP = {
    'dokter': ['Biologi', 'Kimia', 'Matematika Tingkat Lanjut', 'Fisika', 'Matematika'],
    'arsitek': ['Matematika Tingkat Lanjut', 'Fisika', 'Prakarya & Kewirausahaan', 'Informatika'],
    'ekonom': ['Ekonomi', 'Matematika Tingkat Lanjut', 'Sosiologi', 'Geografi'],
    'programmer': ['Informatika', 'Matematika Tingkat Lanjut', 'Fisika', 'Matematika'],
    'penulis': ['Bahasa dan Sastra Indonesia', 'Bahasa dan Sastra Inggris', 'Bahasa Indonesia', 'Sosiologi', 'Antropologi'],
    'guru': ['Sosiologi', 'Bahasa Indonesia', 'Pendidikan Kewarganegaraan', 'Biologi'],
    'psikolog': ['Biologi', 'Sosiologi', 'Antropologi', 'Bahasa Indonesia'],
    'pengusaha': ['Ekonomi', 'Prakarya & Kewirausahaan', 'Sosiologi', 'Matematika'],
    'diplomat': ['Bahasa dan Sastra Inggris', 'Bahasa Inggris', 'Pendidikan Kewarganegaraan', 'Sejarah', 'Geografi'],
    'ilmuwan': ['Fisika', 'Kimia', 'Biologi', 'Matematika Tingkat Lanjut', 'Informatika'],
    'seniman': ['Bahasa dan Sastra Indonesia', 'Sosiologi', 'Antropologi', 'Sejarah'],
    'insinyur': ['Matematika Tingkat Lanjut', 'Fisika', 'Kimia', 'Informatika'],
    'hakim': ['Pendidikan Kewarganegaraan', 'Sejarah', 'Sosiologi', 'Bahasa Indonesia'],
    'polisi': ['Pendidikan Kewarganegaraan', 'Sosiologi', 'Sejarah'],
    'apoteker': ['Kimia', 'Biologi', 'Matematika Tingkat Lanjut'],
}


def _calculate_riasec_match(subject_name: str, riasec: Dict) -> float:
    """Hitung skor kecocokan RIASEC untuk suatu mata pelajaran (0-1)"""
    types = SUBJECT_RIASEC_MAP.get(subject_name, [])
    if not types:
        return 0.3  # default

    total = sum(riasec.get(t, 0) / 5.0 for t in types)
    return min(total / len(types), 1.0)


def _calculate_aspiration_score(subject_name: str, aspiration: str) -> float:
    """Hitung relevansi mata pelajaran terhadap cita-cita siswa (0-1)"""
    if not aspiration:
        return 0.5  # netral jika tidak ada cita-cita

    aspiration_lower = aspiration.lower()
    best_score = 0.0

    for keyword, relevant_subjects in ASPIRATION_SUBJECT_MAP.items():
        if keyword in aspiration_lower:
            if subject_name in relevant_subjects:
                # Posisi di list menentukan relevansi (lebih awal = lebih relevan)
                idx = relevant_subjects.index(subject_name)
                score = max(1.0 - (idx * 0.15), 0.4)
                best_score = max(best_score, score)

    return best_score if best_score > 0 else 0.3


def _get_subject_availability(subject: Dict) -> float:
    """
    Simulasi ketersediaan mata pelajaran di sekolah
    Berdasarkan kategori (IPA lebih umum dari Bahasa Asing tertentu)
    """
    availability_map = {
        'IPA': 0.95,
        'IPS': 0.90,
        'Bahasa': 0.85,
        'Umum': 0.95,
        'Teknologi': 0.75,
        'Seni': 0.70,
        'Vokasi': 0.65,
    }
    return availability_map.get(subject.get('category', ''), 0.80)