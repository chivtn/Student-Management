def get_school_year_and_semester(id_semester: str):
    """
    Trả về học kỳ (1 hoặc 2) và năm học tương ứng từ id_semester.
    """
    try:
        sem_id = int(id_semester)
        semester = 2 if sem_id % 2 == 0 else 1
        start_year = 2020 + (sem_id - 1) // 2
        schoolyear = f"{start_year}-{start_year + 1}"
        return semester, schoolyear
    except (ValueError, TypeError):
        return None, "Không xác định"

# utils.py
import random
import string

def generate_code(prefix: str, length: int = 6) -> str:
    """
    Sinh mã code ngẫu nhiên với prefix (ví dụ 'AD', 'ST', 'TC', 'STU')
    và phần hậu tố là chuỗi số ngẫu nhiên có độ dài xác định (mặc định 6).
    """
    suffix = ''.join(random.choices(string.digits, k=length))
    return f"{prefix}{suffix}"


def generate_admin_code():
    return generate_code("AD")


def generate_staff_code():
    return generate_code("ST")


def generate_teacher_code():
    return generate_code("TC")


def generate_student_code():
    return generate_code("STU")