import json
import math
from collections import defaultdict, deque
from datetime import datetime
import statistics


class CareerPathAdvisor:
    def __init__(self):
        self.skill_graph = self.build_skill_graph()
        self.job_market = self.initialize_comprehensive_market_data()
        self.industry_trends = self.load_industry_trends()
        self.skill_synonyms = self.build_skill_synonyms()
        self.skill_level_mapping = self.build_skill_level_mapping()
        self.indonesian_universities = self.load_indonesian_universities()
        self.education_costs_idr = self.load_education_costs_idr()

    def build_skill_synonyms(self):
        """Build a mapping of synonyms to standard skill names"""
        return {
            # Programming related
            'coding': 'programming', 'code': 'programming', 'software_development': 'programming',
            'developing': 'programming', 'web_development': 'programming', 'app_development': 'programming',
            'kode': 'programming', 'koding': 'programming',
            # Python related
            'py': 'python', 'python_programming': 'python', 'python_code': 'python',
            'code_python': 'python', 'kode_python': 'python', 'koding_python': 'python',
            # Data related
            'data_science': 'data_analysis', 'analytics': 'data_analysis', 'big_data': 'data_analysis',
            'data_analytics': 'data_analysis', 'analisis_data': 'data_analysis', 'data_analisis': 'data_analysis',
            # Machine Learning
            'ml': 'machine_learning', 'ai': 'machine_learning', 'artificial_intelligence': 'machine_learning',
            'deep_learning': 'machine_learning',
            # Management
            'managing': 'project_management', 'team_lead': 'project_management', 'coordination': 'project_management',
            'manager': 'project_management', 'management': 'project_management', 'pemimpin': 'project_management',
            # Communication
            'speaking': 'communication', 'presentation': 'communication', 'public_speaking': 'communication',
            'writing': 'communication', 'berbicara': 'communication', 'publik_speaking': 'communication',
            # Problem Solving
            'troubleshooting': 'problem_solving', 'debugging': 'problem_solving', 'critical_thinking': 'problem_solving',
            'analytical_thinking': 'problem_solving', 'memecahkan_masalah': 'problem_solving', 'pemecahan_masalah': 'problem_solving',
            # Technical skills
            'cloud': 'cloud_computing', 'aws': 'cloud_computing', 'azure': 'cloud_computing',
            'security': 'cybersecurity', 'cyber_security': 'cybersecurity', 'netsec': 'cybersecurity',
            # Healthcare
            'nursing': 'patient_care', 'medical': 'medical_knowledge', 'healthcare': 'medical_knowledge',
            'clinical_skills': 'patient_care', 'pharmacy': 'medical_knowledge',
            # Electricity
            'electrical': 'electrical_systems', 'wiring': 'electrical_systems', 'construction': 'electrical_systems',
            'technical_drawing': 'blueprint_reading',
            # Creative
            'design': 'design_software', 'graphic_design': 'design_software', 'adobe': 'design_software', 'photoshop': 'design_software',
            # Education
            'teaching': 'classroom_management', 'instruction': 'classroom_management', 'pedagogy': 'classroom_management',
            'mengajar': 'classroom_management', 'guru': 'classroom_management',
            # Business
            'finance': 'financial_analysis', 'accounting': 'financial_analysis', 'excel_skills': 'excel', 'spreadsheets': 'excel',
            # Green energy
            'solar': 'solar_technology', 'renewable': 'solar_technology', 'green_energy': 'solar_technology',
            # Legal skills
            'law': 'legal_research', 'litigation': 'legal_writing', 'court': 'legal_procedures',
            'attorney': 'legal_analysis', 'advocacy': 'legal_writing',
            # Law enforcement
            'policing': 'law_enforcement', 'patrol': 'law_enforcement', 'investigation': 'criminal_investigation',
            'detective': 'criminal_investigation', 'enforcement': 'law_enforcement',
            # Military
            'soldier': 'military_operations', 'combat': 'military_training', 'defense': 'national_security', 'tactical': 'military_strategy',
            # Culinary
            'cooking': 'culinary_skills', 'baking': 'culinary_skills', 'food_preparation': 'culinary_skills', 'kitchen': 'culinary_management',
            # Agriculture
            'farming': 'agricultural_production', 'crop': 'crop_management', 'livestock': 'animal_husbandry',
            'harvest': 'agricultural_production'
        }

    def build_skill_level_mapping(self):
        """Map text skill levels to numerical values"""
        return {
            'beginner': 0.3, 'low': 0.3, 'basic': 0.3, 'novice': 0.3,
            'intermediate': 0.6, 'medium': 0.6, 'average': 0.6, 'competent': 0.6,
            'advanced': 0.9, 'high': 0.9, 'expert': 0.9, 'proficient': 0.9, 'excellent': 0.9,
            'master': 1.0, 'professional': 0.8
        }

    def normalize_skill_name(self, skill_name):
        """Convert synonym to standard skill name"""
        skill_name_lower = skill_name.lower().strip().replace(' ', '_')
        return self.skill_synonyms.get(skill_name_lower, skill_name_lower)

    def normalize_skill_level(self, level_input):
        """Convert text level to numerical value"""
        if isinstance(level_input, (int, float)):
            return min(max(level_input, 0.0), 1.0)
        level_str = str(level_input).lower().strip()
        return self.skill_level_mapping.get(level_str, 0.5)

    def load_education_costs_idr(self):
        """Realistic education costs in Indonesian Rupiah for different career paths"""
        return {
            # Formal University Education (per semester)
            'negeri_bachelor_semester': 5000000,      # 5 juta per semester PTN
            'swasta_bachelor_semester': 15000000,     # 15 juta per semester PTS
            'kedinasan_semester': 2000000,           # 2 juta per semester sekolah kedinasan

            # Bootcamps & Intensive Courses
            'programming_bootcamp': 25000000,        # 25 juta untuk bootcamp programming
            'digital_marketing_course': 5000000,     # 5 juta kursus digital marketing
            'design_course': 8000000,                # 8 juta kursus design

            # Certification Costs
            'professional_certification': 3000000,   # 3 juta untuk sertifikasi profesional
            'technical_certification': 1500000,      # 1.5 juta sertifikasi teknis
            'language_certification': 1000000,       # 1 juta sertifikasi bahasa

            # Vocational Training
            'vocational_course': 5000000,           # 5 juta kursus vokasi
            'apprenticeship_fee': 2000000,          # 2 juta biaya magang/pemagangan

            # Online Courses & Self-Study
            'online_course_basic': 500000,          # 500rb kursus online dasar
            'online_course_advanced': 2000000,      # 2 juta kursus online lanjutan
            'book_materials': 500000,               # 500rb untuk buku & materi

            # Specific Career Training
            'culinary_school': 15000000,            # 15 juta sekolah masak
            # Gratis (dibiayai pemerintah)
            'police_academy': 0,
            # Gratis (dibiayai pemerintah)
            'military_academy': 0,
            'teacher_certification': 5000000,       # 5 juta sertifikasi guru
            'nursing_school': 8000000,              # 8 juta sekolah perawat
        }

    def load_indonesian_universities(self):
        """Database of Indonesian universities and their strengths"""
        return {
            # Top Public Universities
            'universitas_indonesia': {
                'name': 'Universitas Indonesia (UI)',
                'location': 'Depok & Jakarta',
                'strengths': ['medicine', 'law', 'engineering', 'computer_science', 'business'],
                'ranking': 'QS World: 237',
                'website': 'ui.ac.id',
                'cost_per_semester': 7500000,  # 7.5 juta
                'type': 'negeri'
            },
            'institut_teknologi_bandung': {
                'name': 'Institut Teknologi Bandung (ITB)',
                'location': 'Bandung',
                'strengths': ['engineering', 'architecture', 'computer_science', 'physics', 'mathematics'],
                'ranking': 'QS World: 235',
                'website': 'itb.ac.id',
                'cost_per_semester': 8000000,  # 8 juta
                'type': 'negeri'
            },
            'universitas_gadjah_mada': {
                'name': 'Universitas Gadjah Mada (UGM)',
                'location': 'Yogyakarta',
                'strengths': ['medicine', 'law', 'engineering', 'agriculture', 'social_sciences'],
                'ranking': 'QS World: 254',
                'website': 'ugm.ac.id',
                'cost_per_semester': 5000000,  # 5 juta
                'type': 'negeri'
            },
            'institut_pertanian_bogor': {
                'name': 'Institut Pertanian Bogor (IPB)',
                'location': 'Bogor',
                'strengths': ['agriculture', 'veterinary', 'food_science', 'forestry', 'marine_science'],
                'ranking': 'QS World: 374',
                'website': 'ipb.ac.id',
                'cost_per_semester': 6000000,  # 6 juta
                'type': 'negeri'
            },
            'universitas_airlangga': {
                'name': 'Universitas Airlangga (UNAIR)',
                'location': 'Surabaya',
                'strengths': ['medicine', 'dentistry', 'pharmacy', 'public_health', 'law'],
                'ranking': 'QS World: 465',
                'website': 'unair.ac.id',
                'cost_per_semester': 5500000,  # 5.5 juta
                'type': 'negeri'
            },

            # Technology & Engineering Focus
            'universitas_telkom': {
                'name': 'Universitas Telkom',
                'location': 'Bandung',
                'strengths': ['telecommunications', 'computer_science', 'electrical_engineering', 'business_digital'],
                'ranking': 'QS Asia: 301-350',
                'website': 'telkomuniversity.ac.id',
                'cost_per_semester': 15000000,  # 15 juta
                'type': 'swasta'
            },
            'institut_teknologi_sepuluh_nopember': {
                'name': 'Institut Teknologi Sepuluh Nopember (ITS)',
                'location': 'Surabaya',
                'strengths': ['engineering', 'maritime_technology', 'computer_science', 'robotics'],
                'ranking': 'QS World: 800-1000',
                'website': 'its.ac.id',
                'cost_per_semester': 6500000,  # 6.5 juta
                'type': 'negeri'
            },

            # Business & Management
            'prasetya_mulya_business_school': {
                'name': 'Universitas Prasetya Mulya',
                'location': 'Jakarta',
                'strengths': ['business_administration', 'marketing', 'finance', 'entrepreneurship'],
                'ranking': 'Top Business School in Indonesia',
                'website': 'prasetiyamulya.ac.id',
                'cost_per_semester': 25000000,  # 25 juta
                'type': 'swasta'
            },
            'universitas_bina_nusantara': {
                'name': 'Bina Nusantara University (BINUS)',
                'location': 'Jakarta',
                'strengths': ['computer_science', 'business', 'design', 'communication'],
                'ranking': 'QS World: 1001-1200',
                'website': 'binus.ac.id',
                'cost_per_semester': 20000000,  # 20 juta
                'type': 'swasta'
            },

            # Creative & Design
            'institut_seni_indonesia': {
                'name': 'Institut Seni Indonesia (ISI)',
                'location': 'Yogyakarta, Denpasar, Surakarta',
                'strengths': ['fine_arts', 'design', 'performing_arts', 'music', 'dance'],
                'ranking': 'Top Arts University',
                'website': 'isi.ac.id',
                'cost_per_semester': 4500000,  # 4.5 juta
                'type': 'negeri'
            },

            # Education & Teaching
            'universitas_pendidikan_indonesia': {
                'name': 'Universitas Pendidikan Indonesia (UPI)',
                'location': 'Bandung',
                'strengths': ['education', 'teaching', 'educational_technology', 'curriculum_development'],
                'ranking': 'Top Education University',
                'website': 'upi.edu',
                'cost_per_semester': 4000000,  # 4 juta
                'type': 'negeri'
            },

            # Law & Legal Studies
            'universitas_padjadjaran': {
                'name': 'Universitas Padjadjaran (UNPAD)',
                'location': 'Bandung',
                'strengths': ['law', 'medicine', 'social_sciences', 'communication'],
                'ranking': 'QS World: 601-650',
                'website': 'unpad.ac.id',
                'cost_per_semester': 7000000,  # 7 juta
                'type': 'negeri'
            },

            # Health & Medical
            'universitas_hasanuddin': {
                'name': 'Universitas Hasanuddin (UNHAS)',
                'location': 'Makassar',
                'strengths': ['medicine', 'public_health', 'engineering', 'agriculture'],
                'ranking': 'QS World: 800-1000',
                'website': 'unhas.ac.id',
                'cost_per_semester': 3500000,  # 3.5 juta
                'type': 'negeri'
            },

            # Agriculture & Environmental
            'universitas_brawijaya': {
                'name': 'Universitas Brawijaya (UB)',
                'location': 'Malang',
                'strengths': ['agriculture', 'animal_husbandry', 'engineering', 'economics'],
                'ranking': 'QS World: 801-1000',
                'website': 'ub.ac.id',
                'cost_per_semester': 4800000,  # 4.8 juta
                'type': 'negeri'
            },

            # Kedinasan (Government Schools)
            'akademi_kepolisian': {
                'name': 'Akademi Kepolisian (AKPOL)',
                'location': 'Semarang',
                'strengths': ['law_enforcement', 'criminal_investigation', 'leadership', 'public_safety'],
                'ranking': 'Top Police Academy',
                'website': 'akpol.ac.id',
                'cost_per_semester': 0,  # Gratis + dapat gaji
                'type': 'kedinasan'
            },
            'akademi_militer': {
                'name': 'Akademi Militer (AKMIL)',
                'location': 'Magelang',
                'strengths': ['military_operations', 'leadership', 'strategy', 'national_security'],
                'ranking': 'Top Military Academy',
                'website': 'akmil.ac.id',
                'cost_per_semester': 0,  # Gratis + dapat gaji
                'type': 'kedinasan'
            },
            'universitas_pertahanan': {
                'name': 'Universitas Pertahanan',
                'location': 'Bogor',
                'strengths': ['national_security', 'defense_studies', 'military_strategy', 'intelligence'],
                'ranking': 'Specialized Defense University',
                'website': 'idu.ac.id',
                'cost_per_semester': 0,  # Gratis
                'type': 'kedinasan'
            }
        }

    def build_skill_graph(self):
        """Create a graph of skills and their relationships"""
        base_graph = {
            'programming': {'related_skills': ['python', 'javascript', 'java', 'problem_solving', 'algorithms'], 'prerequisites': ['logic', 'mathematics'], 'weight': 0.9},
            'data_analysis': {'related_skills': ['statistics', 'python', 'sql', 'excel', 'visualization'], 'prerequisites': ['mathematics', 'critical_thinking'], 'weight': 0.85},
            'project_management': {'related_skills': ['leadership', 'communication', 'planning', 'agile'], 'prerequisites': ['organization', 'communication'], 'weight': 0.8},
            'digital_marketing': {'related_skills': ['seo', 'content_creation', 'analytics', 'social_media'], 'prerequisites': ['creativity', 'communication'], 'weight': 0.75},
            'python': {'related_skills': ['programming', 'data_analysis', 'machine_learning'], 'prerequisites': ['logic'], 'weight': 0.85},
            'machine_learning': {'related_skills': ['python', 'statistics', 'linear_algebra'], 'prerequisites': ['python', 'statistics'], 'weight': 0.9},
            'patient_care': {'related_skills': ['empathy', 'communication', 'medical_knowledge'], 'prerequisites': ['biology', 'communication'], 'weight': 0.8},
            'electrical_systems': {'related_skills': ['safety_protocols', 'troubleshooting', 'blueprint_reading'], 'prerequisites': ['mathematics', 'physics'], 'weight': 0.75},
            'design_software': {'related_skills': ['creativity', 'visual_communication', 'typography'], 'prerequisites': ['artistic_skills', 'computer_literacy'], 'weight': 0.7},
            'classroom_management': {'related_skills': ['communication', 'patience', 'organization'], 'prerequisites': ['communication', 'subject_knowledge'], 'weight': 0.8},
            'financial_analysis': {'related_skills': ['excel', 'data_interpretation', 'reporting'], 'prerequisites': ['mathematics', 'analytical_thinking'], 'weight': 0.85},
            'solar_technology': {'related_skills': ['electrical_systems', 'safety_protocols', 'installation'], 'prerequisites': ['electrical_systems', 'physics'], 'weight': 0.8},
            # Legal skills - ADDED
            'legal_research': {'related_skills': ['legal_writing', 'case_analysis', 'legal_analysis'], 'prerequisites': ['critical_thinking', 'research_skills'], 'weight': 0.85},
            'legal_writing': {'related_skills': ['legal_research', 'communication', 'litigation'], 'prerequisites': ['writing_skills', 'legal_research'], 'weight': 0.8},
            'legal_analysis': {'related_skills': ['critical_thinking', 'case_analysis', 'legal_research'], 'prerequisites': ['analytical_thinking', 'legal_research'], 'weight': 0.85},
            'litigation': {'related_skills': ['trial_advocacy', 'evidence_law', 'legal_writing'], 'prerequisites': ['legal_research', 'public_speaking'], 'weight': 0.9},
            'contract_law': {'related_skills': ['negotiation', 'business_law', 'legal_writing'], 'prerequisites': ['legal_research'], 'weight': 0.8},
            'legal_procedures': {'related_skills': ['court_procedures', 'document_filing', 'legal_research'], 'prerequisites': ['attention_to_detail', 'organization'], 'weight': 0.75},
            # Law enforcement skills - ADDED
            'law_enforcement': {'related_skills': ['criminal_investigation', 'public_safety', 'criminal_law'], 'prerequisites': ['physical_fitness', 'communication'], 'weight': 0.8},
            'criminal_investigation': {'related_skills': ['forensics', 'evidence_collection', 'interview_techniques'], 'prerequisites': ['analytical_thinking', 'attention_to_detail'], 'weight': 0.85},
            # Military skills - ADDED
            'military_operations': {'related_skills': ['military_strategy', 'physical_fitness', 'teamwork'], 'prerequisites': ['discipline', 'physical_fitness'], 'weight': 0.85},
            'military_training': {'related_skills': ['physical_fitness', 'weapons_training', 'first_aid'], 'prerequisites': ['discipline', 'physical_fitness'], 'weight': 0.8},
            'military_strategy': {'related_skills': ['tactical_planning', 'risk_assessment', 'leadership'], 'prerequisites': ['critical_thinking', 'decision_making'], 'weight': 0.9},
            'national_security': {'related_skills': ['intelligence_analysis', 'risk_assessment', 'security_protocols'], 'prerequisites': ['analytical_thinking', 'attention_to_detail'], 'weight': 0.85},
            # Culinary skills - EXPANDED
            'culinary_skills': {'related_skills': ['food_safety', 'knife_skills', 'menu_planning'], 'prerequisites': ['creativity', 'attention_to_detail'], 'weight': 0.7},
            'menu_planning': {'related_skills': ['nutrition', 'cost_control', 'culinary_skills'], 'prerequisites': ['culinary_skills'], 'weight': 0.75},
            'food_safety': {'related_skills': ['sanitation_procedures', 'temperature_control', 'hygiene_practices'], 'prerequisites': ['attention_to_detail'], 'weight': 0.9},
            'culinary_management': {'related_skills': ['team_management', 'inventory_control', 'cost_management'], 'prerequisites': ['culinary_skills', 'leadership'], 'weight': 0.8},
            # Agriculture skills - ADDED
            'agricultural_production': {'related_skills': ['crop_management', 'soil_science', 'harvest_techniques'], 'prerequisites': ['biology', 'problem_solving'], 'weight': 0.75},
            'crop_management': {'related_skills': ['pest_control', 'irrigation_systems', 'soil_fertility'], 'prerequisites': ['biology', 'analytical_thinking'], 'weight': 0.7},
            'animal_husbandry': {'related_skills': ['livestock_management', 'veterinary_care', 'breeding_techniques'], 'prerequisites': ['biology', 'empathy'], 'weight': 0.75},
            # Additional foundational skills
            'physical_fitness': {'related_skills': ['endurance', 'strength_training', 'discipline'], 'prerequisites': [], 'weight': 0.6},
            'discipline': {'related_skills': ['self_control', 'focus', 'reliability'], 'prerequisites': [], 'weight': 0.7},
            'research_skills': {'related_skills': ['information_gathering', 'analysis', 'documentation'], 'prerequisites': ['critical_thinking'], 'weight': 0.7},
            'forensics': {'related_skills': ['evidence_analysis', 'crime_scene_management', 'scientific_methods'], 'prerequisites': ['attention_to_detail', 'analytical_thinking'], 'weight': 0.85}
        }
        return base_graph

    def initialize_comprehensive_market_data(self):
        """Comprehensive career database across multiple industries"""
        base_market = {
            'software_developer': {
                'demand_score': 0.9, 'growth_rate': 0.22, 'avg_salary': 85000,
                'required_skills': ['programming', 'algorithms', 'problem_solving'],
                'emerging_skills': ['cloud_computing', 'ai_ml'],
                'industries': ['tech', 'finance'], 'education_required': 'bachelor_degree',
                'certification_required': False, 'work_environment': ['office', 'remote'],
                'indonesian_universities': ['institut_teknologi_bandung', 'universitas_indonesia', 'universitas_telkom', 'institut_teknologi_sepuluh_nopember', 'universitas_gadjah_mada']
            },
            'data_scientist': {
                'demand_score': 0.95, 'growth_rate': 0.31, 'avg_salary': 95000,
                'required_skills': ['python', 'statistics', 'machine_learning'],
                'emerging_skills': ['deep_learning', 'big_data'],
                'industries': ['tech', 'research'], 'education_required': 'bachelor_degree',
                'certification_required': False, 'work_environment': ['office', 'remote'],
                'indonesian_universities': ['institut_teknologi_bandung', 'universitas_indonesia', 'universitas_gadjah_mada', 'universitas_bina_nusantara', 'universitas_telkom']
            },
            'product_manager': {
                'demand_score': 0.85, 'growth_rate': 0.18, 'avg_salary': 105000,
                'required_skills': ['project_management', 'communication', 'strategy'],
                'emerging_skills': ['product_analytics', 'user_research'],
                'industries': ['tech'], 'education_required': 'bachelor_degree',
                'certification_required': False, 'work_environment': ['office', 'remote'],
                'indonesian_universities': ['universitas_indonesia', 'universitas_gadjah_mada', 'prasetya_mulya_business_school', 'universitas_bina_nusantara', 'institut_teknologi_bandung']
            },
            'digital_marketer': {
                'demand_score': 0.8, 'growth_rate': 0.15, 'avg_salary': 65000,
                'required_skills': ['digital_marketing', 'analytics', 'content_creation'],
                'emerging_skills': ['ai_marketing', 'video_content'],
                'industries': ['marketing'], 'education_required': 'bachelor_degree',
                'certification_required': False, 'work_environment': ['office', 'remote'],
                'indonesian_universities': ['universitas_indonesia', 'prasetya_mulya_business_school', 'universitas_padjadjaran', 'universitas_bina_nusantara', 'universitas_gadjah_mada']
            },
            'registered_nurse': {
                'demand_score': 0.92, 'growth_rate': 0.09, 'avg_salary': 75000,
                'required_skills': ['patient_care', 'medical_knowledge', 'communication', 'empathy'],
                'emerging_skills': ['telehealth', 'data_analysis'],
                'industries': ['healthcare'], 'education_required': 'associate_degree',
                'certification_required': True, 'work_environment': ['hospital', 'clinic'],
                'indonesian_universities': ['universitas_indonesia', 'universitas_airlangga', 'universitas_gadjah_mada', 'universitas_hasanuddin', 'universitas_padjadjaran']
            },
            'electrician': {
                'demand_score': 0.85, 'growth_rate': 0.10, 'avg_salary': 56000,
                'required_skills': ['electrical_systems', 'safety_protocols', 'blueprint_reading', 'troubleshooting'],
                'emerging_skills': ['smart_home_technology', 'renewable_energy_systems'],
                'industries': ['construction', 'energy'], 'education_required': 'apprenticeship',
                'certification_required': True, 'work_environment': ['construction_sites', 'residential'],
                'indonesian_universities': ['institut_teknologi_bandung', 'institut_teknologi_sepuluh_nopember', 'universitas_gadjah_mada', 'universitas_indonesia', 'universitas_brawijaya']
            },
            'graphic_designer': {
                'demand_score': 0.75, 'growth_rate': 0.05, 'avg_salary': 52000,
                'required_skills': ['design_software', 'creativity', 'visual_communication'],
                'emerging_skills': ['ui_ux_design', 'motion_graphics'],
                'industries': ['advertising', 'media'], 'education_required': 'bachelor_degree',
                'certification_required': False, 'work_environment': ['agency', 'freelance'],
                'indonesian_universities': ['institut_seni_indonesia', 'institut_teknologi_bandung', 'universitas_bina_nusantara', 'universitas_indonesia', 'universitas_pendidikan_indonesia']
            },
            'secondary_teacher': {
                'demand_score': 0.78, 'growth_rate': 0.07, 'avg_salary': 62000,
                'required_skills': ['subject_knowledge', 'classroom_management', 'lesson_planning'],
                'emerging_skills': ['digital_learning_tools', 'inclusive_education'],
                'industries': ['education'], 'education_required': 'bachelor_degree',
                'certification_required': True, 'work_environment': ['school'],
                'indonesian_universities': ['universitas_pendidikan_indonesia', 'universitas_negeri_jakarta', 'universitas_negeri_yogyakarta', 'universitas_negeri_surabaya', 'universitas_pendidikan_ganesha']
            },
            'financial_analyst': {
                'demand_score': 0.80, 'growth_rate': 0.11, 'avg_salary': 85000,
                'required_skills': ['financial_analysis', 'excel', 'data_interpretation'],
                'emerging_skills': ['fintech', 'predictive_analytics'],
                'industries': ['finance'], 'education_required': 'bachelor_degree',
                'certification_required': False, 'work_environment': ['office', 'corporate'],
                'indonesian_universities': ['universitas_indonesia', 'universitas_gadjah_mada', 'prasetya_mulya_business_school', 'universitas_airlangga', 'universitas_padjadjaran']
            },
            'sustainability_specialist': {
                'demand_score': 0.85, 'growth_rate': 0.28, 'avg_salary': 72000,
                'required_skills': ['environmental_regulations', 'sustainability_principles', 'data_analysis', 'project_management'],
                'emerging_skills': ['carbon_accounting', 'circular_economy', 'esg_reporting'],
                'industries': ['corporate', 'government', 'consulting'], 'education_required': 'bachelor_degree',
                'certification_required': False, 'work_environment': ['office', 'field_work'],
                'indonesian_universities': ['institut_pertanian_bogor', 'universitas_gadjah_mada', 'universitas_indonesia', 'institut_teknologi_bandung', 'universitas_brawijaya']
            },
            'legal_consultant': {
                'demand_score': 0.75, 'growth_rate': 0.08, 'avg_salary': 95000,
                'required_skills': ['legal_research', 'contract_law', 'communication'],
                'emerging_skills': ['legal_tech', 'privacy_law'],
                'industries': ['legal', 'corporate'], 'education_required': 'law_degree',
                'certification_required': True, 'work_environment': ['office', 'court'],
                'indonesian_universities': ['universitas_indonesia', 'universitas_gadjah_mada', 'universitas_padjadjaran', 'universitas_airlangga', 'universitas_hasanuddin']
            },
            'chef': {
                'demand_score': 0.70, 'growth_rate': 0.10, 'avg_salary': 50000,
                'required_skills': ['culinary_skills', 'menu_planning', 'food_safety'],
                'emerging_skills': ['sustainable_cooking', 'dietary_specialization'],
                'industries': ['hospitality', 'tourism'], 'education_required': 'culinary_school',
                'certification_required': False, 'work_environment': ['kitchen', 'restaurant'],
                'indonesian_universities': ['akademi_kuliner_indonesia', 'sekolah_tinggi_parawisata', 'universitas_pelita_harapan', 'universitas_bina_nusantara']
            },
            # NEW CAREERS ADDED:
            'police_officer': {
                'demand_score': 0.80, 'growth_rate': 0.07, 'avg_salary': 65000,
                'required_skills': ['law_enforcement', 'communication', 'physical_fitness', 'problem_solving'],
                'emerging_skills': ['community_policing', 'digital_forensics'],
                'industries': ['law_enforcement', 'public_safety'], 'education_required': 'kedinasan',
                'certification_required': True, 'work_environment': ['field_work', 'patrol'],
                'indonesian_universities': ['akademi_kepolisian', 'universitas_indonesia', 'universitas_gadjah_mada', 'universitas_padjadjaran']
            },
            'detective': {
                'demand_score': 0.75, 'growth_rate': 0.05, 'avg_salary': 83000,
                'required_skills': ['criminal_investigation', 'analytical_thinking', 'communication', 'attention_to_detail'],
                'emerging_skills': ['digital_investigation', 'behavioral_analysis'],
                'industries': ['law_enforcement'], 'education_required': 'kedinasan',
                'certification_required': True, 'work_environment': ['field_work', 'office'],
                'indonesian_universities': ['akademi_kepolisian', 'universitas_indonesia', 'universitas_gadjah_mada', 'universitas_padjadjaran', 'universitas_airlangga']
            },
            'military_officer': {
                'demand_score': 0.85, 'growth_rate': 0.08, 'avg_salary': 70000,
                'required_skills': ['military_operations', 'leadership', 'physical_fitness', 'discipline'],
                'emerging_skills': ['cyber_warfare', 'drone_operations'],
                'industries': ['military', 'defense'], 'education_required': 'kedinasan',
                'certification_required': True, 'work_environment': ['military_base', 'field_operations'],
                'indonesian_universities': ['akademi_militer', 'universitas_pertahanan', 'institut_teknologi_bandung', 'universitas_gadjah_mada']
            },
            'intelligence_analyst': {
                'demand_score': 0.82, 'growth_rate': 0.12, 'avg_salary': 78000,
                'required_skills': ['national_security', 'analytical_thinking', 'research_skills', 'attention_to_detail'],
                'emerging_skills': ['data_mining', 'threat_assessment'],
                'industries': ['military', 'government'], 'education_required': 'kedinasan',
                'certification_required': True, 'work_environment': ['office', 'secure_facility'],
                'indonesian_universities': ['universitas_pertahanan', 'universitas_indonesia', 'institut_teknologi_bandung', 'universitas_gadjah_mada', 'universitas_airlangga']
            },
            'attorney': {
                'demand_score': 0.78, 'growth_rate': 0.06, 'avg_salary': 120000,
                'required_skills': ['legal_research', 'legal_writing', 'litigation', 'communication'],
                'emerging_skills': ['legal_technology', 'esg_law'],
                'industries': ['legal', 'corporate'], 'education_required': 'law_degree',
                'certification_required': True, 'work_environment': ['office', 'court'],
                'indonesian_universities': ['universitas_indonesia', 'universitas_gadjah_mada', 'universitas_padjadjaran', 'universitas_airlangga', 'universitas_hasanuddin']
            },
            'paralegal': {
                'demand_score': 0.80, 'growth_rate': 0.10, 'avg_salary': 55000,
                'required_skills': ['legal_research', 'legal_writing', 'organization', 'attention_to_detail'],
                'emerging_skills': ['e_discovery', 'legal_software'],
                'industries': ['legal'], 'education_required': 'associate_degree',
                'certification_required': False, 'work_environment': ['office'],
                'indonesian_universities': ['universitas_indonesia', 'universitas_gadjah_mada', 'universitas_padjadjaran', 'universitas_airlangga']
            },
            'farm_manager': {
                'demand_score': 0.75, 'growth_rate': 0.04, 'avg_salary': 68000,
                'required_skills': ['agricultural_production', 'crop_management', 'problem_solving', 'business_management'],
                'emerging_skills': ['precision_agriculture', 'sustainable_farming'],
                'industries': ['agriculture'], 'education_required': 'bachelor_degree',
                'certification_required': False, 'work_environment': ['farm', 'field_work'],
                'indonesian_universities': ['institut_pertanian_bogor', 'universitas_brawijaya', 'universitas_gadjah_mada', 'universitas_hasanuddin', 'universitas_lampung']
            },
            'agricultural_specialist': {
                'demand_score': 0.72, 'growth_rate': 0.08, 'avg_salary': 52000,
                'required_skills': ['crop_management', 'soil_science', 'problem_solving'],
                'emerging_skills': ['organic_farming', 'agritech'],
                'industries': ['agriculture', 'research'], 'education_required': 'bachelor_degree',
                'certification_required': False, 'work_environment': ['field_work', 'lab'],
                'indonesian_universities': ['institut_pertanian_bogor', 'universitas_brawijaya', 'universitas_gadjah_mada', 'universitas_hasanuddin', 'universitas_sriwijaya']
            },
            'livestock_manager': {
                'demand_score': 0.70, 'growth_rate': 0.03, 'avg_salary': 48000,
                'required_skills': ['animal_husbandry', 'veterinary_care', 'problem_solving'],
                'emerging_skills': ['animal_welfare', 'sustainable_practices'],
                'industries': ['agriculture'], 'education_required': 'associate_degree',
                'certification_required': False, 'work_environment': ['farm', 'field_work'],
                'indonesian_universities': ['institut_pertanian_bogor', 'universitas_brawijaya', 'universitas_gadjah_mada', 'universitas_hasanuddin', 'universitas_mataram']
            },
            'restaurant_manager': {
                'demand_score': 0.75, 'growth_rate': 0.09, 'avg_salary': 58000,
                'required_skills': ['culinary_management', 'communication', 'leadership', 'customer_service'],
                'emerging_skills': ['digital_ordering', 'sustainability'],
                'industries': ['hospitality'], 'education_required': 'associate_degree',
                'certification_required': False, 'work_environment': ['restaurant'],
                'indonesian_universities': ['universitas_pelita_harapan', 'universitas_bina_nusantara', 'sekolah_tinggi_parawisata', 'universitas_pancasila']
            }
        }
        return base_market

    def load_industry_trends(self):
        return {
            'tech': {'trend': 'up', 'hot_topics': ['AI', 'Blockchain']},
            'healthcare': {'trend': 'stable', 'hot_topics': ['Telehealth']},
            'green_energy': {'trend': 'up', 'hot_topics': ['Solar', 'Wind']},
            'law_enforcement': {'trend': 'stable', 'hot_topics': ['Community Policing', 'Technology Integration']},
            'military': {'trend': 'stable', 'hot_topics': ['Cybersecurity', 'Drone Technology']},
            'legal': {'trend': 'stable', 'hot_topics': ['Legal Tech', 'Remote Law']},
            'agriculture': {'trend': 'up', 'hot_topics': ['Precision Farming', 'Sustainable Practices']},
            'hospitality': {'trend': 'stable', 'hot_topics': ['Sustainability', 'Digital Ordering']}
        }

    def get_user_input(self):
        """Interactive user input system - UPDATED FOR INDONESIA"""
        print("=== 🎯 CAREER PATH ADVISOR - USER PROFILE ===")
        print("Let's build your career profile step by step!\n")

        user_data = {
            'skills': {}, 'experience': {}, 'interests': [],
            'career_goals': [], 'constraints': {}, 'preferences': {}
        }

        # Skills input
        print("\n📊 SKILLS ASSESSMENT")
        print("Enter your skills and their levels ('beginner', 'intermediate', 'advanced') (type 'done' when finished)")
        while True:
            skill_input = input(
                "\nEnter skill and level (e.g. 'python advanced'): ").strip()
            if skill_input.lower() == 'done':
                break
            if not skill_input:
                continue
            parts = skill_input.split()
            if len(parts) < 2:
                print("Please enter both skill and level")
                continue
            skill_name = ' '.join(parts[:-1])
            level_input = parts[-1]
            normalized_skill = self.normalize_skill_name(skill_name)
            normalized_level = self.normalize_skill_level(level_input)
            user_data['skills'][normalized_skill] = normalized_level
            print(
                f"✓ Added: {normalized_skill} (level: {normalized_level:.1f})")

        # Experience input
        print("\n💼 WORK EXPERIENCE")
        while True:
            exp_input = input(
                "\nEnter skill and years (e.g. 'python 2'): ").strip()
            if exp_input.lower() == 'done':
                break
            if not exp_input:
                continue
            parts = exp_input.split()
            if len(parts) < 2:
                print("Please enter both skill and years")
                continue
            skill_name = ' '.join(parts[:-1])
            try:
                years = float(parts[-1])
                normalized_skill = self.normalize_skill_name(skill_name)
                user_data['experience'][normalized_skill] = years
                print(f"✓ Added: {normalized_skill} ({years} years)")
            except ValueError:
                print("Please enter a valid number for years")

        # Constraints input - UPDATED FOR INDONESIA
        print("\n⏰ CONSTRAINTS (Dalam Rupiah)")
        while True:
            try:
                user_data['constraints']['time_availability'] = float(
                    input("Hours/week available (e.g. 10): "))
                break
            except ValueError:
                print("Invalid number.")
        while True:
            try:
                budget_input = input("Budget dalam Rupiah (e.g. 5000000 untuk 5 juta): ").replace(
                    '.', '').replace(',', '')
                user_data['constraints']['financial_investment'] = float(
                    budget_input)
                break
            except ValueError:
                print("Invalid number. Masukkan angka tanpa titik/koma.")
        while True:
            try:
                user_data['constraints']['timeline_months'] = int(
                    input("Timeline dalam bulan (e.g. 24): "))
                break
            except ValueError:
                print("Invalid number.")

        # Preferences
        print("\n⚙️ PREFERENCES")
        envs = []
        print("Environments: office, remote, hybrid, flexible, field_work")
        while True:
            env = input("Enter environment (or 'done'): ").strip(
            ).lower().replace(' ', '_')
            if env == 'done':
                break
            if env:
                envs.append(env)
        user_data['preferences']['work_environment'] = envs

        return user_data

    def display_user_profile_summary(self, user_data):
        """Show a summary of the user's input - UPDATED FOR INDONESIA"""
        print("\n" + "="*50)
        print("📋 YOUR PROFILE SUMMARY")
        print("="*50)
        print(f"\n📊 Skills ({len(user_data['skills'])}):")
        for skill, level in user_data['skills'].items():
            print(f"   • {skill.replace('_', ' ').title()}: {level:.1f}")

        budget_idr = user_data['constraints']['financial_investment']
        budget_formatted = f"Rp {budget_idr:,.0f}".replace(',', '.')
        print(f"\n⏰ Constraints: Budget {budget_formatted}, "
              f"Timeline {user_data['constraints']['timeline_months']} bulan")

    def _calculate_score(self, user_data, job_key, job_details):
        """Calculates compatibility score (0-100) based on skills, preferences, constraints - INDONESIA CONTEXT"""
        score = 0.0

        # --- 1. Skill Match (Weight: 60%) ---
        required_skills = set(job_details['required_skills'])
        user_skills = set(user_data['skills'].keys())
        matching_skills = required_skills.intersection(user_skills)

        if not required_skills:
            skill_score = 1.0
        else:
            skill_score = len(matching_skills) / len(required_skills)
            # Check Skill Levels penalty
            level_penalty = 0
            for skill in matching_skills:
                user_level = user_data['skills'][skill]
                if user_level < 0.5:
                    level_penalty += 0.1
            skill_score = max(0, skill_score - (level_penalty * 0.2))
        score += skill_score * 60

        # --- 2. Constraint Match (Weight: 20%) - UPDATED FOR INDONESIA ---
        user_budget_idr = user_data['constraints'].get(
            'financial_investment', float('inf'))

        # Estimate realistic costs in Indonesian Rupiah
        if job_details.get('education_required') == 'kedinasan':
            # Government schools - free or very low cost
            estimated_cost_idr = 0
        elif job_details.get('education_required') == 'doctorate':
            estimated_cost_idr = 150000000  # 150 juta untuk S3
        elif job_details.get('education_required') == 'law_degree':
            estimated_cost_idr = 80000000   # 80 juta untuk pendidikan hukum
        elif job_details.get('education_required') == 'bachelor_degree':
            estimated_cost_idr = 50000000   # 50 juta untuk S1
        elif job_details.get('education_required') == 'associate_degree':
            estimated_cost_idr = 25000000   # 25 juta untuk D3
        elif job_details.get('education_required') == 'culinary_school':
            estimated_cost_idr = 30000000   # 30 juta untuk sekolah kuliner
        elif job_details.get('education_required') == 'apprenticeship':
            estimated_cost_idr = 5000000    # 5 juta untuk pemagangan
        else:
            estimated_cost_idr = 10000000   # 10 juta default

        # Add certification costs if required
        if job_details.get('certification_required'):
            estimated_cost_idr += 5000000  # +5 juta untuk sertifikasi

        # Budget scoring logic
        if estimated_cost_idr == 0:
            # Free education path - perfect for any budget
            score += 10
        elif user_budget_idr >= estimated_cost_idr:
            # Can afford the full path
            score += 10
        elif user_budget_idr >= estimated_cost_idr * 0.5:
            # Can afford at least half - partial points
            score += 5
        elif user_budget_idr >= estimated_cost_idr * 0.25:
            # Can afford at least quarter - minimal points
            score += 2
        else:
            # Cannot afford - no points
            score += 0

        # --- 3. Timeline Match (Weight: 10%) ---
        user_timeline = user_data['constraints'].get('timeline_months', 24)

        if job_details.get('education_required') == 'doctorate' and user_timeline < 60:
            score -= 5
        elif job_details.get('education_required') == 'law_degree' and user_timeline < 48:
            score -= 3
        elif job_details.get('education_required') == 'bachelor_degree' and user_timeline < 36:
            score -= 2
        elif job_details.get('education_required') == 'associate_degree' and user_timeline < 24:
            score -= 1
        else:
            score += 5

        # --- 4. Preference Match (Weight: 10%) ---
        user_envs = set(user_data['preferences'].get('work_environment', []))
        job_envs = set(job_details.get('work_environment', []))
        if user_envs.intersection(job_envs) or not user_envs:
            score += 10

        return round(max(0, min(score, 100)), 1)

    def recommend_paths(self, user_data, top_n=3):
        recommendations = []
        for job_key, job_details in self.job_market.items():
            match_score = self._calculate_score(
                user_data, job_key, job_details)
            req_skills = set(job_details['required_skills'])
            user_skills = set(user_data['skills'].keys())
            missing_skills = list(req_skills - user_skills)
            emerging_gaps = [s for s in job_details.get(
                'emerging_skills', []) if s not in user_skills]

            recommendations.append({
                'career': job_key,
                'score': match_score,
                'salary': job_details['avg_salary'],
                'missing_skills': missing_skills,
                'emerging_gaps': emerging_gaps,
                'details': job_details
            })
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:top_n]

    def build_learning_resources(self):
        """Complete Database covering ALL related_skills in the graph"""
        resources = {
            # ==========================================
            # 1. PROGRAMMING & TECH (Java, JS, SQL, etc.)
            # ==========================================
            'python': {
                'steps': ['Master Syntax & Data Types', 'Learn OOP & Modules', 'Build 3 Mini-Projects', 'Virtual Environments'],
                'resources': ['Course: CS50p (Harvard/EdX)', 'Video: Programming with Mosh', 'Book: Automate the Boring Stuff']
            },
            'javascript': {
                'steps': ['ES6 Syntax (Arrow functions, etc.)', 'DOM Manipulation', 'Async/Await & Promises', 'Learn a Framework (React/Vue)'],
                'resources': ['Site: JavaScript.info', 'Course: FreeCodeCamp JS Algorithms', 'Video: Traversy Media']
            },
            'java': {
                'steps': ['JVM Fundamentals', 'Object-Oriented Programming', 'Java Collections Framework', 'Spring Boot Basics'],
                'resources': ['Book: Head First Java', 'Course: MOOC.fi Java Programming', 'Site: Baeldung']
            },
            'sql': {
                'steps': ['SELECT, FROM, WHERE basics', 'Joins (Inner, Outer, Left)', 'Aggregations (GROUP BY)', 'Database Normalization'],
                'resources': ['Site: SQLZoo', 'Site: Mode Analytics SQL Tutorial', 'Video: Alex The Analyst']
            },
            'problem_solving': {
                'steps': ['Decompose complex problems', 'Pattern Recognition', 'Algorithm Design', 'Debugging strategies'],
                'resources': ['Book: Think Like a Programmer', 'Site: Project Euler', 'Method: The Rubber Duck Technique']
            },
            'algorithms': {
                'steps': ['Big O Notation', 'Sorting & Searching', 'Trees & Graphs', 'Dynamic Programming'],
                'resources': ['Book: Grokking Algorithms', 'Site: LeetCode', 'Video: NeetCode']
            },
            'cloud_computing': {
                'steps': ['AWS/Azure Core Services', 'Docker/Containers', 'Serverless Functions', 'Networking Basics'],
                'resources': ['Course: AWS Cloud Practitioner', 'Site: A Cloud Guru']
            },

            # ==========================================
            # 2. DATA & ANALYTICS
            # ==========================================
            'data_analysis': {
                'steps': ['Pandas/NumPy Mastery', 'Data Cleaning', 'Exploratory Analysis', 'Storytelling with Data'],
                'resources': ['Book: Python for Data Analysis', 'Site: Kaggle Learn', 'Video: Keith Galli']
            },
            'statistics': {
                'steps': ['Descriptive Stats', 'Probability Distributions', 'Hypothesis Testing (p-values)', 'Regression'],
                'resources': ['Site: Khan Academy Stats', 'Book: Naked Statistics', 'Video: StatQuest']
            },
            'visualization': {
                'steps': ['Chart Selection Theory', 'Tableau or PowerBI Basics', 'Matplotlib/Seaborn (Python)', 'Dashboard Design'],
                'resources': ['Book: Storytelling with Data', 'Course: Tableau Public Resources', 'Site: Data Viz Catalogue']
            },
            'machine_learning': {
                'steps': ['Supervised vs Unsupervised', 'Scikit-Learn', 'Model Evaluation metrics', 'Feature Engineering'],
                'resources': ['Course: Andrew Ng ML', 'Book: Hands-On ML', 'Site: Hugging Face']
            },
            'linear_algebra': {
                'steps': ['Vectors & Scalars', 'Matrix Multiplication', 'Eigenvalues/Eigenvectors', 'Dimensionality Reduction'],
                'resources': ['Video: 3Blue1Brown Linear Algebra', 'Course: Khan Academy Linear Algebra']
            },
            'excel': {
                'steps': ['VLOOKUP/XLOOKUP', 'Pivot Tables', 'Power Query', 'Macros/VBA'],
                'resources': ['Video: ExcelIsFun', 'Site: MrExcel', 'Course: Microsoft Excel Certification']
            },
            'data_interpretation': {
                'steps': ['Identifying Trends', 'Correlation vs Causation', 'Detecting Bias', 'Executive Summaries'],
                'resources': ['Book: Keeping Up with the Quants', 'Article: HBR Data Literacy']
            },
            'reporting': {
                'steps': ['KPI Definition', 'Automated Reporting', 'Slide Deck Design', 'Stakeholder Presentation'],
                'resources': ['Book: Slide:ology', 'Tool: Google Looker Studio']
            },

            # ==========================================
            # 3. BUSINESS & MANAGEMENT
            # ==========================================
            'project_management': {
                'steps': ['Project Lifecycle', 'Risk Management', 'Budgeting', 'Scope Management'],
                'resources': ['Course: Google PM Certificate', 'Book: PMBOK Guide']
            },
            'agile': {
                'steps': ['Scrum Ceremonies', 'Kanban Boards', 'User Stories', 'Sprint Planning'],
                'resources': ['Book: Scrum: The Art of Doing Twice the Work', 'Site: Atlassian Agile Coach']
            },
            'leadership': {
                'steps': ['Delegation', 'Conflict Resolution', 'Emotional Intelligence', 'Team Motivation'],
                'resources': ['Book: Leaders Eat Last', 'Video: Simon Sinek TED Talks', 'Book: Dare to Lead']
            },
            'planning': {
                'steps': ['Gantt Charts', 'Critical Path Method', 'Resource Allocation', 'Goal Setting (SMART)'],
                'resources': ['Tool: Asana Academy', 'Book: Getting Things Done']
            },
            'communication': {
                'steps': ['Active Listening', 'Public Speaking', 'Business Writing', 'Non-verbal cues'],
                'resources': ['Organization: Toastmasters', 'Book: Crucial Conversations', 'Book: Simply Said']
            },
            'organization': {
                'steps': ['Digital File Management', 'Time Blocking', 'Inbox Zero', 'Prioritization Matrices'],
                'resources': ['Book: The Life-Changing Magic of Tidying Up', 'Method: Eisenhower Matrix']
            },

            # ==========================================
            # 4. MARKETING & DIGITAL
            # ==========================================
            'digital_marketing': {
                'steps': ['Marketing Funnels', 'Customer Personas', 'Brand Voice', 'Campaign Analytics'],
                'resources': ['Site: HubSpot Academy', 'Book: This is Marketing']
            },
            'seo': {
                'steps': ['Keyword Research', 'On-Page Optimization', 'Backlink Strategy', 'Technical SEO'],
                'resources': ['Site: Moz Beginner Guide to SEO', 'Tool: Google Search Console', 'Video: Ahrefs YouTube']
            },
            'content_creation': {
                'steps': ['Copywriting', 'Basic Graphic Design', 'Video Editing', 'Storytelling'],
                'resources': ['Book: Everybody Writes', 'Tool: Canva Design School', 'Software: CapCut/Premiere']
            },
            'social_media': {
                'steps': ['Platform Algorithms', 'Content Calendars', 'Community Management', 'Social Analytics'],
                'resources': ['Site: Social Media Examiner', 'Course: Meta Social Media Cert']
            },
            'analytics': {  # Marketing analytics
                'steps': ['Google Analytics 4', 'Conversion Tracking', 'A/B Testing', 'Funnel Analysis'],
                'resources': ['Course: Google Analytics Academy', 'Book: Web Analytics 2.0']
            },

            # ==========================================
            # 5. HEALTHCARE & PATIENT CARE
            # ==========================================
            'patient_care': {
                'steps': ['Vital Signs', 'Patient Hygiene', 'Infection Control', 'Documentation'],
                'resources': ['Video: RegisteredNurseRN', 'Textbook: Fundamentals of Nursing']
            },
            'empathy': {
                'steps': ['Perspective Taking', 'Active Listening', 'Compassionate Response', 'Managing Burnout'],
                'resources': ['Book: I Hear You', 'Video: Brene Brown on Empathy']
            },
            'medical_knowledge': {
                'steps': ['Anatomy', 'Medical Terminology', 'Pharmacology', 'Pathology Basics'],
                'resources': ['Site: Kenhub', 'App: Epocrates', 'Video: Osmosis']
            },

            # ==========================================
            # 6. ELECTRICAL & SOLAR
            # ==========================================
            'electrical_systems': {
                'steps': ['Ohm\'s Law', 'Circuit Analysis', 'Wiring Methods', 'National Electric Code (NEC)'],
                'resources': ['Book: Ugly\'s Electrical References', 'Video: Electrician U']
            },
            'safety_protocols': {
                'steps': ['OSHA Standards', 'PPE Selection', 'Lockout/Tagout', 'First Aid Basics'],
                'resources': ['Site: OSHA.gov', 'Course: OSHA 10-Hour']
            },
            'troubleshooting': {
                'steps': ['Root Cause Analysis', 'Multimeter Usage', 'Schematic Tracing', 'Isolation Testing'],
                'resources': ['Book: How to Diagnose and Fix Everything Electronic']
            },
            'blueprint_reading': {
                'steps': ['Symbols & Legends', 'Scale Ratios', 'Floor Plans', 'Electrical Schedules'],
                'resources': ['Book: Blueprint Reading for the Building Trades']
            },
            'solar_technology': {
                'steps': ['Photovoltaic Physics', 'Inverters', 'Battery Systems', 'Grid Interconnection'],
                'resources': ['Site: Solar Energy International', 'Book: Solar Electricity Handbook']
            },
            'installation': {
                'steps': ['Racking Systems', 'Roof Penetrations', 'Wiring Management', 'Commissioning'],
                'resources': ['Video: Solar Power World', 'Certification: NABCEP']
            },

            # ==========================================
            # 7. DESIGN & CREATIVE
            # ==========================================
            'creativity': {
                'steps': ['Brainstorming Techniques', 'Lateral Thinking', 'Mind Mapping', 'Iterative Design'],
                'resources': ['Book: Steal Like an Artist', 'Method: SCAMPER']
            },
            'design_software': {
                'steps': ['Photoshop Layers', 'Illustrator Vectors', 'InDesign Layouts', 'Figma Prototyping'],
                'resources': ['Course: Adobe Creative Cloud Tutorials', 'Video: Piximperfect']
            },
            'visual_communication': {
                'steps': ['Color Theory', 'Layout & Composition', 'Imagery Selection', 'Branding'],
                'resources': ['Book: Thinking with Type', 'Site: Behance']
            },
            'typography': {
                'steps': ['Typeface Families', 'Kerning/Leading/Tracking', 'Font Pairing', 'Hierarchy'],
                'resources': ['Site: Google Fonts Knowledge', 'Book: The Elements of Typographic Style']
            },

            # ==========================================
            # 8. EDUCATION
            # ==========================================
            'classroom_management': {
                'steps': ['Establishing Rules', 'Behavior Intervention', 'Room Layout', 'Engagement Strategies'],
                'resources': ['Book: The First Days of School', 'Site: Cult of Pedagogy']
            },
            'patience': {
                'steps': ['Stress Management', 'Mindfulness', 'De-escalation Techniques', 'Perspective Taking'],
                'resources': ['App: Headspace', 'Book: The Power of Patience']
            },
            'subject_knowledge': {
                'steps': ['Curriculum Standards', 'Deep Dive into Topic', 'Pedagogical Content Knowledge'],
                'resources': ['Site: Khan Academy', 'Site: Coursera']
            },

            # ==========================================
            # 9. LEGAL
            # ==========================================
            'legal_research': {
                'steps': ['Using Westlaw/Lexis', 'Finding Case Law', 'Shepardizing', 'Statutory Interpretation'],
                'resources': ['Site: Cornell LII', 'Book: Legal Research in a Nutshell']
            },
            'legal_writing': {
                'steps': ['IRAC Method', 'Drafting Memos', 'Citation (Bluebook)', 'Persuasive Arguments'],
                'resources': ['Book: Point Made', 'Book: The Redbook']
            },
            'case_analysis': {
                'steps': ['Briefing Cases', 'Identifying Holdings', 'Distinguishing Facts', 'Synthesizing Rules'],
                'resources': ['Method: Case Briefing Templates', 'Site: Oyez']
            },
            'litigation': {
                'steps': ['Civil Procedure', 'Discovery Process', 'Motions Practice', 'Settlement'],
                'resources': ['Book: Civil Procedure: Examples & Explanations']
            },
            'trial_advocacy': {
                'steps': ['Opening Statements', 'Direct/Cross Exam', 'Objections', 'Closing Arguments'],
                'resources': ['Book: Mauet on Trial Techniques', 'Video: Mock Trial Competitions']
            },
            'evidence_law': {
                'steps': ['Relevance', 'Hearsay Rules', 'Character Evidence', 'Authentication'],
                'resources': ['Book: Evidence under the Rules', 'Flashcards: Law in a Flash']
            },
            'contract_law': {
                'steps': ['Offer & Acceptance', 'Consideration', 'Breach of Contract', 'Remedies'],
                'resources': ['Course: Harvard Contract Law Online', 'Book: Contracts E&E']
            },
            'negotiation': {
                'steps': ['BATNA Analysis', 'Active Listening', 'Value Creation', 'Closing Deals'],
                'resources': ['Book: Never Split the Difference', 'Book: Getting to Yes']
            },
            'business_law': {
                'steps': ['Business Entities (LLC/Corp)', 'Corporate Governance', 'M&A Basics', 'Compliance'],
                'resources': ['Site: SBA.gov', 'Book: Business Law Today']
            },
            'legal_analysis': {
                'steps': ['Issue Spotting', 'Applying Legal Principles', 'Reasoning by Analogy', 'Policy Analysis'],
                'resources': ['Book: Getting to Maybe', 'Course: Legal Analysis and Writing']
            },
            'legal_procedures': {
                'steps': ['Court Filing Systems', 'Deadline Management', 'Document Preparation', 'Client Interaction'],
                'resources': ['Book: The Legal Secretary\'s Handbook', 'Course: Paralegal Certification Programs']
            },

            # ==========================================
            # 10. LAW ENFORCEMENT & MILITARY
            # ==========================================
            'law_enforcement': {
                'steps': ['Constitutional Law', 'Patrol Procedures', 'Use of Force Continuum', 'Community Relations'],
                'resources': ['Academy: Police Training Program', 'Book: Verbal Judo', 'Course: State Certification']
            },
            'criminal_investigation': {
                'steps': ['Crime Scene Preservation', 'Evidence Collection', 'Witness Interviewing', 'Case File Preparation'],
                'resources': ['Book: Criminal Investigation', 'Course: FBI National Academy', 'Training: Detective School']
            },
            'military_operations': {
                'steps': ['Basic Training Completion', 'Weapons Proficiency', 'Tactical Movement', 'Team Coordination'],
                'resources': ['Training: Boot Camp', 'Manual: Army Field Manuals', 'Course: Officer Candidate School']
            },
            'military_training': {
                'steps': ['Physical Conditioning', 'Weapons Qualification', 'First Aid Certification', 'Leadership Development'],
                'resources': ['Program: Basic Combat Training', 'Manual: Military Training Manuals', 'Course: NCO Academy']
            },
            'military_strategy': {
                'steps': ['Study Military History', 'Learn Battlefield Tactics', 'Understand Chain of Command', 'Develop Leadership Skills'],
                'resources': ['Book: The Art of War', 'Course: War College', 'Manual: Joint Publication 3-0']
            },
            'national_security': {
                'steps': ['Study Intelligence Gathering', 'Learn Risk Assessment', 'Understand Geopolitics', 'Security Clearance Process'],
                'resources': ['Book: Intelligence: From Secrets to Policy', 'Course: National Security Studies', 'Agency: DHS Training']
            },
            'physical_fitness': {
                'steps': ['Cardiovascular Training', 'Strength Building', 'Endurance Exercises', 'Flexibility Work'],
                'resources': ['Program: Military PT Standards', 'App: Nike Training Club', 'Guide: ACSM Fitness Guidelines']
            },
            'discipline': {
                'steps': ['Time Management', 'Goal Setting', 'Self-Motivation Techniques', 'Routine Establishment'],
                'resources': ['Book: The Power of Discipline', 'Method: Pomodoro Technique', 'App: Habitica']
            },
            'forensics': {
                'steps': ['Evidence Collection Protocols', 'Laboratory Analysis', 'Digital Forensics', 'Expert Testimony Preparation'],
                'resources': ['Course: Forensic Science Degree', 'Book: Criminalistics', 'Certification: IAI Programs']
            },

            # ==========================================
            # 11. CULINARY & HOSPITALITY
            # ==========================================
            'culinary_skills': {
                'steps': ['Knife Handling', 'Heat Control', 'Seasoning/Balancing', 'Plating'],
                'resources': ['Book: The Professional Chef', 'Book: Salt, Fat, Acid, Heat']
            },
            'knife_skills': {
                'steps': ['Sharpening/Honing', 'The Claw Grip', 'Precision Cuts (Julienne/Dice)', 'Speed'],
                'resources': ['Video: Serious Eats Knife Skills', 'Video: Jacques Pépin Techniques']
            },
            'menu_planning': {
                'steps': ['Costing & Pricing', 'Seasonality', 'Menu Engineering', 'Inventory Management'],
                'resources': ['Book: Menu Design', 'Software: Toast POS Resources']
            },
            'nutrition': {
                'steps': ['Macronutrients', 'Dietary Restrictions', 'Allergens', 'Healthy Substitutions'],
                'resources': ['Textbook: Nutrition for Foodservice', 'Site: Nutrition.gov']
            },
            'cost_control': {
                'steps': ['Portion Control', 'Waste Management', 'Supplier Negotiation', 'P&L Analysis'],
                'resources': ['Book: Restaurant Financial Basics']
            },
            'food_safety': {
                'steps': ['HACCP Plans', 'Time/Temp Control', 'Cross-Contamination', 'Personal Hygiene'],
                'resources': ['Certification: ServSafe Manager', 'Site: FDA Food Code']
            },
            'sanitation_procedures': {
                'steps': ['Chemical Handling', 'Equipment Cleaning', 'Pest Control', 'Inspection Prep'],
                'resources': ['Checklist: Health Department Guides']
            },
            'culinary_management': {
                'steps': ['Staff Scheduling', 'Vendor Management', 'Quality Control', 'Customer Service Standards'],
                'resources': ['Book: Restaurant Success by the Numbers', 'Course: Hospitality Management']
            },

            # ==========================================
            # 12. AGRICULTURE
            # ==========================================
            'agricultural_production': {
                'steps': ['Soil Preparation', 'Crop Selection', 'Planting Techniques', 'Harvest Methods'],
                'resources': ['Book: The Market Gardener', 'Program: USDA Extension Services', 'Course: Sustainable Agriculture']
            },
            'crop_management': {
                'steps': ['Soil Testing', 'Pest Control', 'Irrigation Systems', 'Crop Rotation'],
                'resources': ['Guide: University Extension Programs', 'Book: Crop Production Science', 'Tool: Soil Testing Kits']
            },
            'animal_husbandry': {
                'steps': ['Animal Nutrition', 'Health Monitoring', 'Breeding Programs', 'Facility Management'],
                'resources': ['Book: Storey\'s Guide to Raising Livestock', 'Course: Animal Science Programs', 'Vet: Consultation Services']
            }
        }
        return resources

    def estimate_career_cost(self, career_details):
        """Estimate realistic education costs for a career in Indonesia"""
        base_cost = 0

        if career_details.get('education_required') == 'kedinasan':
            base_cost = 0
        elif career_details.get('education_required') == 'doctorate':
            base_cost = 150000000  # 150 juta
        elif career_details.get('education_required') == 'law_degree':
            base_cost = 80000000   # 80 juta
        elif career_details.get('education_required') == 'bachelor_degree':
            base_cost = 50000000   # 50 juta
        elif career_details.get('education_required') == 'associate_degree':
            base_cost = 25000000   # 25 juta
        elif career_details.get('education_required') == 'culinary_school':
            base_cost = 30000000   # 30 juta
        elif career_details.get('education_required') == 'apprenticeship':
            base_cost = 5000000    # 5 juta
        else:
            base_cost = 10000000   # 10 juta default

        if career_details.get('certification_required'):
            base_cost += 5000000  # +5 juta untuk sertifikasi

        return base_cost

    def display_university_recommendations(self, recommendation, user_budget):
        """Display Indonesian university recommendations with cost information"""
        print(f"\n🎓 REKOMENDASI UNIVERSITAS DI INDONESIA:")
        print("   Kampus terbaik untuk karir ini:")

        career_details = recommendation['details']
        if 'indonesian_universities' in career_details:
            for i, uni_key in enumerate(career_details['indonesian_universities'], 1):
                if uni_key in self.indonesian_universities:
                    uni = self.indonesian_universities[uni_key]
                    cost_per_semester = uni.get('cost_per_semester', 0)
                    total_degree_cost = cost_per_semester * 8  # 8 semester for bachelor

                    # Cost indicator
                    if cost_per_semester == 0:
                        cost_indicator = "🎓 GRATIS + TUNJANGAN"
                    elif user_budget >= total_degree_cost:
                        cost_indicator = "✅ Terjangkau"
                    elif user_budget >= total_degree_cost * 0.5:
                        cost_indicator = "⚠️ Butuh beasiswa"
                    else:
                        cost_indicator = "💡 Pertimbangkan alternatif"

                    cost_formatted = f"Rp {cost_per_semester:,.0f}".replace(
                        ',', '.')
                    print(f"   {i}. {uni['name']} ({uni['type'].title()})")
                    print(f"      📍 {uni['location']} | 🏆 {uni['ranking']}")
                    print(
                        f"      💰 {cost_formatted}/semester - {cost_indicator}")
                    print(f"      🌐 {uni['website']}")
                    print()

    def generate_learning_roadmap(self, user_data, recommendation):
        career_name = recommendation['career'].replace('_', ' ').title()
        missing = recommendation['missing_skills']
        resources_db = self.build_learning_resources()

        print(
            f"\n🚀 ROADMAP TO: {career_name} (Match: {recommendation['score']}%)")
        print("-" * 70)

        # 1. Market Data
        details = recommendation['details']
        salary_idr = details['avg_salary'] * \
            15000  # Convert to approximate IDR
        salary_formatted = f"Rp {salary_idr:,.0f}".replace(',', '.')
        print(
            f"💰 OUTLOOK: Gaji {salary_formatted}/tahun | Growth {details['growth_rate']*100:.1f}%")

        # Budget compatibility info
        user_budget = user_data['constraints']['financial_investment']
        estimated_cost = self.estimate_career_cost(details)

        if estimated_cost == 0:
            cost_info = "🎓 GRATIS (Sekolah Kedinasan)"
        elif user_budget >= estimated_cost:
            cost_info = "✅ Budget mencukupi"
        elif user_budget >= estimated_cost * 0.5:
            cost_info = "⚠️ Budget terbatas (perlu bantuan beasiswa)"
        else:
            cost_info = "❌ Budget tidak mencukupi (perlu alternatif)"

        estimated_cost_formatted = f"Rp {estimated_cost:,.0f}".replace(
            ',', '.')
        print(f"💰 ESTIMASI BIAYA: {estimated_cost_formatted} - {cost_info}")

        if not missing:
            print("\n✅ You have all the core required skills!")
            print("👉 Focus on emerging skills:", ", ".join(
                recommendation['emerging_gaps']))
        else:
            print(
                f"\n📋 DETAILED ACTION PLAN ({len(missing)} Skills to Learn):")

            for i, skill in enumerate(missing, 1):
                display_name = skill.replace('_', ' ').title()
                print(f"\n   [{chr(64+i)}] SKILL: {display_name}")

                if skill in resources_db:
                    data = resources_db[skill]
                    print("       🛠️  Steps to Master:")
                    for step_idx, step in enumerate(data['steps'], 1):
                        print(f"          {step_idx}. {step}")
                    print("       📚 Recommended Resources:")
                    for res in data['resources']:
                        print(f"          • {res}")
                else:
                    print("       ⚠️  General Advice:")
                    print(
                        f"          1. Search for '{display_name} beginner course' on Udemy/Coursera")
                    print(
                        f"          2. Build a small project using {display_name}")

        # Indonesian University Recommendations
        self.display_university_recommendations(recommendation, user_budget)

        print("-" * 70)


if __name__ == "__main__":
    advisor = CareerPathAdvisor()

    # Use real user input instead of mock data
    user_profile = advisor.get_user_input()

    advisor.display_user_profile_summary(user_profile)

    print("\n🔎 ANALYZING MARKET DATA...")
    top_matches = advisor.recommend_paths(user_profile)

    for i, match in enumerate(top_matches, 1):
        advisor.generate_learning_roadmap(user_profile, match)
