"""
API Routes untuk SPK Pemilihan Mata Pelajaran
Blueprint: /api/v1/...
"""

from flask import Blueprint, request, jsonify
from models.data import RIASEC_QUESTIONS, SUBJECTS, RIASEC_DESCRIPTIONS, CAREER_PACKAGES
from models.saw_calculator import SAWCalculator
import datetime

api = Blueprint('api', __name__, url_prefix='/api/v1')
saw = SAWCalculator()


# ─── Health Check ─────────────────────────────────────────────────────────────

@api.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'version': '2.0.0',
        'timestamp': datetime.datetime.utcnow().isoformat()
    })


# ─── RIASEC ───────────────────────────────────────────────────────────────────

@api.route('/questions', methods=['GET'])
def get_questions():
    """Ambil semua soal RIASEC"""
    return jsonify({'success': True, 'data': RIASEC_QUESTIONS, 'total': len(RIASEC_QUESTIONS)})


@api.route('/riasec/descriptions', methods=['GET'])
def get_riasec_descriptions():
    """Ambil deskripsi tiap dimensi RIASEC"""
    return jsonify({'success': True, 'data': RIASEC_DESCRIPTIONS})


@api.route('/riasec/calculate', methods=['POST'])
def calculate_riasec():
    """
    Hitung skor RIASEC dari jawaban siswa.

    Body JSON:
        answers: List[int] (length = jumlah soal, nilai 1-5)
    """
    try:
        data = request.get_json(force=True)
        answers = data.get('answers', [])
        expected = len(RIASEC_QUESTIONS)

        if len(answers) != expected:
            return jsonify({'success': False, 'message': f'Jawaban harus berjumlah {expected} soal'}), 400

        if not all(isinstance(a, (int, float)) and 1 <= a <= 5 for a in answers):
            return jsonify({'success': False, 'message': 'Nilai jawaban harus antara 1 dan 5'}), 400

        # Inisialisasi skor per dimensi
        totals = {d: [] for d in ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']}

        for i, answer in enumerate(answers):
            q_type = RIASEC_QUESTIONS[i]['type']
            totals[q_type].append(answer)

        scores = {}
        for dim, vals in totals.items():
            scores[dim] = round(sum(vals) / len(vals), 2) if vals else 0.0

        # Holland Code: 3 dimensi tertinggi
        sorted_dims = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        holland_code = ''.join(d[0][0].upper() for d in sorted_dims[:3])
        top_type = sorted_dims[0][0]

        # Saran paket karir berdasarkan Holland Code
        suggested_packages = _suggest_career_packages(holland_code, scores)

        return jsonify({
            'success': True,
            'data': {
                'scores': scores,
                'holland_code': holland_code,
                'top_type': top_type,
                'top_description': RIASEC_DESCRIPTIONS.get(top_type, {}),
                'sorted_dimensions': [{'type': d, 'score': s} for d, s in sorted_dims],
                'suggested_packages': suggested_packages,
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ─── Mata Pelajaran ───────────────────────────────────────────────────────────

@api.route('/subjects', methods=['GET'])
def get_subjects():
    """Ambil semua mata pelajaran pilihan"""
    group_filter = request.args.get('group')
    result = SUBJECTS if not group_filter else [s for s in SUBJECTS if s['group'] == group_filter]
    return jsonify({'success': True, 'data': result, 'total': len(result)})


@api.route('/career-packages', methods=['GET'])
def get_career_packages():
    """Ambil semua paket rekomendasi karir"""
    return jsonify({'success': True, 'data': CAREER_PACKAGES})


# ─── SAW Recommendation ───────────────────────────────────────────────────────

@api.route('/recommend', methods=['POST'])
def recommend():
    """
    Hitung rekomendasi mata pelajaran dengan metode SAW.

    Body JSON:
        student_name: str
        student_class: str
        grades: Dict[str, float]          # nama mapel -> nilai 0-100
        riasec_scores: Dict[str, float]   # dimensi -> rata-rata 1-5
        aspiration: str                   # cita-cita/jurusan yang diminati
        custom_weights: Dict (opsional)   # bobot kustom

    Returns:
        recommendations: List (diurutkan berdasarkan rank SAW)
        saw_summary: Detail perhitungan SAW
        career_match: Kecocokan dengan paket karir
    """
    try:
        body = request.get_json(force=True)

        student_name = body.get('student_name', 'Siswa')
        student_class = body.get('student_class', '')
        grades = body.get('grades', {})
        riasec_scores = body.get('riasec_scores', {})
        aspiration = body.get('aspiration', '')
        custom_weights = body.get('custom_weights', None)

        # Validasi minimal
        if not grades:
            return jsonify({'success': False, 'message': 'Data nilai (grades) tidak boleh kosong'}), 400

        student_data = {
            'grades': grades,
            'riasec_scores': riasec_scores,
            'aspiration': aspiration,
        }

        recommendations = saw.recommend_subjects(student_data, SUBJECTS, weights=custom_weights)

        # Identifikasi mata pelajaran wajib vs tidak tersedia
        for rec in recommendations:
            subject = next((s for s in SUBJECTS if s['name'] == rec['subject']), {})
            min_grade = subject.get('min_grade', 0)
            rec['meets_minimum'] = rec['academic_score'] >= min_grade
            rec['min_grade'] = min_grade

        # Kecocokan dengan paket karir
        career_match = _match_career_packages(aspiration, recommendations)

        # Summary SAW
        top5 = [r['subject'] for r in recommendations[:5]]
        saw_summary = {
            'method': 'Simple Additive Weighting (SAW)',
            'criteria': [
                {'name': 'Nilai Akademik Rapor', 'weight': '40%', 'type': 'benefit'},
                {'name': 'Kecocokan RIASEC',     'weight': '30%', 'type': 'benefit'},
                {'name': 'Relevansi Cita-cita',  'weight': '20%', 'type': 'benefit'},
                {'name': 'Ketersediaan di Sekolah', 'weight': '10%', 'type': 'benefit'},
            ],
            'total_alternatives': len(recommendations),
            'top5': top5,
        }

        return jsonify({
            'success': True,
            'data': {
                'student_name': student_name,
                'student_class': student_class,
                'aspiration': aspiration,
                'recommendations': recommendations,
                'saw_summary': saw_summary,
                'career_match': career_match,
                'generated_at': datetime.datetime.utcnow().isoformat(),
            }
        })

    except Exception as e:
        import traceback
        return jsonify({'success': False, 'message': str(e), 'trace': traceback.format_exc()}), 500


# ─── BK Consultation Simulation ───────────────────────────────────────────────

@api.route('/bk-advice', methods=['POST'])
def bk_advice():
    """
    Simulasi saran guru BK berdasarkan profil siswa.
    Mengemulasi proses konsultasi akhir semester 2 kelas 10.
    """
    try:
        body = request.get_json(force=True)
        holland_code = body.get('holland_code', 'RIA')
        top_recommendations = body.get('top_recommendations', [])
        aspiration = body.get('aspiration', '')
        meets_minimum = body.get('meets_minimum', True)

        advice_points = []

        # Saran berdasarkan Holland Code
        hc_advice = {
            'R': 'Pertimbangkan jurusan teknik atau sains terapan.',
            'I': 'Kamu cocok di bidang riset, MIPA, atau teknologi.',
            'A': 'Eksplorasi jurusan seni, desain, sastra, atau komunikasi.',
            'S': 'Pertimbangkan pendidikan, psikologi, atau kesehatan.',
            'E': 'Bisnis, manajemen, hukum, atau kepemimpinan sangat cocok untukmu.',
            'C': 'Akuntansi, keuangan, statistika, atau administrasi bisnis bisa jadi pilihan tepat.',
        }
        for c in holland_code[:2]:
            if c in hc_advice:
                advice_points.append(hc_advice[c])

        if not meets_minimum:
            advice_points.append('⚠️ Beberapa mata pelajaran pilihanmu mensyaratkan nilai minimum tertentu. Diskusikan dengan guru BK dan wali kelas.')

        if aspiration:
            advice_points.append(f'Cita-citamu sebagai {aspiration} sudah terefleksi dalam rekomendasi sistem. Konfirmasikan pilihan ini bersama orang tua.')

        advice_points.append('Proses pemilihan ini dilakukan pada akhir semester 2 kelas 10, dengan bimbingan guru BK dan wali kelas.')
        advice_points.append('Keputusan akhir tetap ada pada siswa, orang tua, dan pihak sekolah setelah melalui sesi konsultasi.')

        return jsonify({
            'success': True,
            'data': {
                'advice': advice_points,
                'next_steps': [
                    'Diskusikan hasil ini dengan guru BK',
                    'Konsultasikan dengan orang tua',
                    'Cek ketersediaan guru dan kelas peminatan di sekolah',
                    'Pertimbangkan beban belajar dan kemampuan akademik',
                    'Konfirmasi pilihan sebelum akhir semester 2 kelas 10',
                ],
                'reminder': 'Sistem ini bersifat pendukung, bukan penentu. Keputusan terbaik lahir dari diskusi yang komprehensif.'
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _suggest_career_packages(holland_code: str, scores: dict) -> list:
    """Rekomendasikan paket karir berdasarkan Holland Code"""
    suggestions = []
    for key, pkg in CAREER_PACKAGES.items():
        # Hitung kecocokan sederhana berdasarkan top dimensi
        match_score = 0
        for c in holland_code:
            dim_map = {'R': 'realistic', 'I': 'investigative', 'A': 'artistic',
                       'S': 'social', 'E': 'enterprising', 'C': 'conventional'}
            dim = dim_map.get(c)
            if dim:
                match_score += scores.get(dim, 0)
        suggestions.append({'key': key, 'label': pkg['label'], 'icon': pkg['icon'], 'match': round(match_score, 2)})
    suggestions.sort(key=lambda x: x['match'], reverse=True)
    return suggestions[:3]


def _match_career_packages(aspiration: str, recommendations: list) -> dict:
    """Cocokkan rekomendasi dengan paket karir berdasarkan cita-cita"""
    if not aspiration:
        return {}

    aspiration_lower = aspiration.lower()
    best_match = None
    best_score = 0

    keyword_map = {
        'dokter': 'kedokteran', 'medis': 'kedokteran', 'kesehatan': 'kedokteran',
        'teknik': 'teknik', 'insinyur': 'teknik', 'arsitek': 'teknik',
        'ekonomi': 'ekonomi_bisnis', 'bisnis': 'ekonomi_bisnis', 'akuntansi': 'ekonomi_bisnis',
        'sosial': 'sosial_humaniora', 'hukum': 'sosial_humaniora',
        'bahasa': 'bahasa_sastra', 'penulis': 'bahasa_sastra', 'jurnalis': 'bahasa_sastra',
        'sains': 'sains_murni', 'peneliti': 'sains_murni', 'ilmuwan': 'sains_murni',
        'it': 'teknologi_informasi', 'programmer': 'teknologi_informasi', 'komputer': 'teknologi_informasi',
    }

    for keyword, pkg_key in keyword_map.items():
        if keyword in aspiration_lower:
            pkg = CAREER_PACKAGES.get(pkg_key, {})
            rec_subjects = [r['subject'] for r in recommendations[:5]]
            match = sum(1 for s in pkg.get('subjects', []) if s in rec_subjects)
            if match > best_score:
                best_score = match
                best_match = {'key': pkg_key, **pkg, 'match_count': match}

    return best_match or {}