"""
测试所有模块是否可以正常导入
运行: python test_import.py
"""

print("开始测试模块导入...")

try:
    print("✓ 导入 main")
    import main
    
    print("✓ 导入 app.core.config")
    from app.core import config
    
    print("✓ 导入 app.core.database")
    from app.core import database
    
    print("✓ 导入 app.core.security")
    from app.core import security
    
    print("✓ 导入 app.core.utils")
    from app.core import utils
    
    print("✓ 导入所有模型")
    from app.models import user, post, comment, reaction, report, bottle, time_capsule, poll
    
    print("✓ 导入所有 schemas")
    from app.schemas import user as user_schema
    from app.schemas import post as post_schema
    from app.schemas import comment as comment_schema
    
    print("✓ 导入所有 API 路由")
    from app.api.v1 import auth, posts, comments, reactions, reports, safety
    from app.api.v1 import bottles, time_capsules, polls, utility, admin
    
    print("\n✅ 所有模块导入成功！")
    print("\n项目结构正确，可以启动服务了。")
    print("\n启动命令:")
    print("  python run.py")
    print("  或")
    print("  python -m uvicorn main:app --reload")
    
except ImportError as e:
    print(f"\n❌ 导入失败: {e}")
    print("\n请先安装依赖:")
    print("  python -m pip install -r requirements.txt")
except Exception as e:
    print(f"\n❌ 发生错误: {e}")
