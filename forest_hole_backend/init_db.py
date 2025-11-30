"""
数据库初始化脚本
创建测试用户和管理员账号
"""

from app.core.database import engine, SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
from app.core.database import Base

def init_database():
    """初始化数据库"""
    print("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建完成")
    
    db = SessionLocal()
    try:
        # 检查是否已有用户
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"⚠️  数据库中已有 {existing_users} 个用户，跳过初始化")
            return
        
        # 创建管理员账号
        admin_user = User(
            username="admin",
            password_hash=get_password_hash("admin123"),
            is_admin=True,
            is_banned=False
        )
        db.add(admin_user)
        
        # 创建测试用户
        test_users = [
            User(
                username="testuser1",
                password_hash=get_password_hash("password123"),
                is_admin=False,
                is_banned=False
            ),
            User(
                username="testuser2",
                password_hash=get_password_hash("password123"),
                is_admin=False,
                is_banned=False
            ),
            User(
                username="testuser3",
                password_hash=get_password_hash("password123"),
                is_admin=False,
                is_banned=False
            ),
        ]
        
        for user in test_users:
            db.add(user)
        
        db.commit()
        
        print("\n✅ 初始化完成！已创建以下账号：")
        print("\n管理员账号:")
        print("  用户名: admin")
        print("  密码: admin123")
        print("\n测试账号:")
        print("  用户名: testuser1, testuser2, testuser3")
        print("  密码: password123")
        print("\n请在生产环境中修改这些默认密码！")
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
