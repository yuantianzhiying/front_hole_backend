"""
快速API测试脚本
运行: python quick_test.py
"""

import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(name, url, method="GET", data=None, headers=None):
    """测试单个端点"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=5)
        
        status = "✓" if response.status_code < 400 else "✗"
        print(f"{status} {name}: {response.status_code}")
        return response
    except requests.exceptions.ConnectionError:
        print(f"✗ {name}: 连接失败")
        return None
    except Exception as e:
        print(f"✗ {name}: {str(e)}")
        return None

def main():
    print("=" * 60)
    print("  快速接口测试")
    print("=" * 60)
    
    # 1. 健康检查
    print("\n[健康检查]")
    response = test_endpoint("Health Check", f"{BASE_URL}/health")
    if not response:
        print("\n❌ 服务未启动！请先运行: uvicorn main:app --reload")
        sys.exit(1)
    
    # 2. 根路径
    print("\n[基础接口]")
    test_endpoint("Root", f"{BASE_URL}/")
    test_endpoint("API Docs", f"{BASE_URL}/docs")
    
    # 3. 认证
    print("\n[认证接口]")
    response = test_endpoint(
        "Login/Register",
        f"{BASE_URL}/api/v1/auth/login",
        "POST",
        {"device_id": "quick-test-device"}
    )
    
    token = None
    if response and response.status_code == 200:
        try:
            token = response.json().get("access_token")
            print(f"  Token: {token[:30]}..." if token else "  No token")
        except:
            pass
    
    if not token:
        print("\n❌ 登录失败，无法继续测试需要认证的接口")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 4. 帖子接口
    print("\n[帖子接口]")
    test_endpoint("Get Posts", f"{BASE_URL}/api/v1/posts", headers=headers)
    
    response = test_endpoint(
        "Create Post",
        f"{BASE_URL}/api/v1/posts",
        "POST",
        {"content": "快速测试帖子", "tag": "test"},
        headers
    )
    # 201 Created 也是成功的
    
    post_id = None
    if response and response.status_code in [200, 201]:
        try:
            post_id = response.json().get("id")
            print(f"  Post ID: {post_id}")
        except:
            pass
    
    if post_id:
        test_endpoint(f"Get Post Detail", f"{BASE_URL}/api/v1/posts/{post_id}", headers=headers)
    
    # 5. 其他接口
    print("\n[其他接口]")
    test_endpoint("Safety Check", f"{BASE_URL}/api/v1/safety/check-text", "POST", 
                  {"content": "测试文本"}, headers)
    test_endpoint("Daily Info", f"{BASE_URL}/api/v1/utility/daily-info", headers=headers)
    test_endpoint("Draw Bottle", f"{BASE_URL}/api/v1/bottles/draw", headers=headers)
    
    # 6. 管理员接口
    print("\n[管理员接口]")
    admin_headers = {"Authorization": "Bearer admin-secret-token-change-in-production"}
    test_endpoint("Admin Dashboard", f"{BASE_URL}/api/v1/admin/dashboard", headers=admin_headers)
    
    print("\n" + "=" * 60)
    print("✅ 快速测试完成！")
    print("=" * 60)
    print("\n详细测试请运行: python test_api.py")
    print("API文档: http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    main()
