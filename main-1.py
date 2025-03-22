from database import create_tables
from auth import AuthManager
from models import Student

if __name__ == "__main__":
    create_tables()
    print("Bazaviy ma'lumotlar bazasi yaratildi.")

    # Foydalanuvchi ro'yxatdan o'tkazish
    AuthManager.register("admin", "admin123", "admin")
    user = AuthManager.login("admin", "admin123")
    if user:
        print(f"Tizimga muvaffaqiyatli kirildi: {user['username']} ({user['role']})")

    # Talaba qo'shish
    student = Student("Ali Valiyev", 20, "A")
    student.save()
    print("Talaba qo'shildi!")
    
