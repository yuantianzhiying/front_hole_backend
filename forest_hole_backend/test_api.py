"""
完整的API接口测试程序
运行: python test_api.py
确保服务已启动: uvicorn main:app --reload
"""

import requests
import json
import time
from typing import Dict, Any, Optional

# 配置
BASE_URL = "http://127.0.0.1:8000/api/v1"
ADMIN_TOKEN = "admin-secret-token-change-in-production"

# 全局变量存储测试数据
test_data = {
    "token": None,
    "user_id": None,
    "post_id": None,
    "comment_id": None,
    "bottle_id": None,
    "capsule_id": None,
    "poll_id": None,
}

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg: str):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg: str):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")

def print_section(title: str):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.END}\n")


def test_request(
    method: str,
    endpoint: str,
    description: str,
    data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    expected_status: int = 200,
    save_to: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    执行API测试请求
    """
    url = f"{BASE_URL}{endpoint}"
    
    try:
        print_info(f"测试: {description}")
        print(f"      {method} {endpoint}")
        
        if method == "GET":
            response = requests.get(url, headers=headers, params=data)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            print_error(f"不支持的HTTP方法: {method}")
            return None
        
        # 检查状态码
        if response.status_code == expected_status:
            print_success(f"状态码: {response.status_code}")
            
            # 尝试解析JSON
            try:
                result = response.json()
                print(f"      响应: {json.dumps(result, ensure_ascii=False, indent=2)[:200]}...")
                
                # 保存数据
                if save_to and result:
                    if isinstance(result, dict):
                        if save_to == "token" and "access_token" in result:
                            test_data[save_to] = result["access_token"]
                        elif save_to in result:
                            test_data[save_to] = result[save_to]
                        elif "id" in result:
                            test_data[save_to] = result["id"]
                    print_info(f"已保存 {save_to}: {test_data.get(save_to)}")
                
                return result
            except:
                print_success("响应成功（无JSON内容）")
                return {}
        else:
            print_error(f"状态码错误: 期望 {expected_status}, 实际 {response.status_code}")
            print(f"      响应: {response.text[:200]}")
            return None
            
    except requests.exceptions.ConnectionError:
        print_error("连接失败！请确保服务已启动 (uvicorn main:app --reload)")
        return None
    except Exception as e:
        print_error(f"请求异常: {str(e)}")
        return None


def get_auth_headers() -> Dict[str, str]:
    """获取认证头"""
    if test_data["token"]:
        return {"Authorization": f"Bearer {test_data['token']}"}
    return {}


def get_admin_headers() -> Dict[str, str]:
    """获取管理员认证头"""
    return {"Authorization": f"Bearer {ADMIN_TOKEN}"}


def test_health_check():
    """测试健康检查"""
    print_section("0. 健康检查")
    
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        if response.status_code == 200:
            print_success("服务运行正常")
            return True
        else:
            print_error("服务状态异常")
            return False
    except:
        print_error("无法连接到服务！请先启动: uvicorn main:app --reload")
        return False


def test_auth():
    """测试认证接口"""
    print_section("1. 认证接口 (Authentication)")
    
    # 1.1 用户登录/注册
    result = test_request(
        "POST",
        "/auth/login",
        "用户登录/注册",
        data={"device_id": "test-device-12345"},
        save_to="token"
    )
    
    if result and "access_token" in result:
        test_data["token"] = result["access_token"]
        print_success(f"登录成功，Token: {test_data['token'][:20]}...")
    else:
        print_error("登录失败，后续测试可能无法进行")


def test_posts():
    """测试帖子接口"""
    print_section("2. 帖子接口 (Posts)")
    
    headers = get_auth_headers()
    
    # 2.1 发布帖子
    result = test_request(
        "POST",
        "/posts",
        "发布新帖子",
        data={
            "content": "这是一个测试帖子，测试敏感词过滤功能",
            "tag": "test",
            "media_urls": ["https://example.com/image1.jpg"]
        },
        headers=headers,
        expected_status=201,
        save_to="post_id"
    )
    
    if result and "id" in result:
        test_data["post_id"] = result["id"]
    
    time.sleep(0.5)
    
    # 2.2 获取帖子列表（最新）
    test_request(
        "GET",
        "/posts",
        "获取帖子列表（最新）",
        data={"sort": "new", "page": 1, "limit": 10},
        headers=headers
    )
    
    time.sleep(0.5)
    
    # 2.3 获取帖子列表（热门）
    test_request(
        "GET",
        "/posts",
        "获取帖子列表（热门）",
        data={"sort": "hot", "page": 1, "limit": 10},
        headers=headers
    )
    
    time.sleep(0.5)
    
    # 2.4 按标签筛选
    test_request(
        "GET",
        "/posts",
        "按标签筛选帖子",
        data={"tag": "test"},
        headers=headers
    )
    
    time.sleep(0.5)
    
    # 2.5 搜索帖子
    test_request(
        "GET",
        "/posts",
        "搜索帖子",
        data={"keyword": "测试"},
        headers=headers
    )
    
    time.sleep(0.5)
    
    # 2.6 获取帖子详情
    if test_data["post_id"]:
        test_request(
            "GET",
            f"/posts/{test_data['post_id']}",
            "获取帖子详情",
            headers=headers
        )


def test_comments():
    """测试评论接口"""
    print_section("3. 评论接口 (Comments)")
    
    headers = get_auth_headers()
    
    if not test_data["post_id"]:
        print_warning("跳过评论测试：没有可用的帖子ID")
        return
    
    # 3.1 发表评论
    result = test_request(
        "POST",
        f"/posts/{test_data['post_id']}/comments",
        "发表评论",
        data={"content": "这是一条测试评论"},
        headers=headers,
        expected_status=201,
        save_to="comment_id"
    )
    
    if result and "id" in result:
        test_data["comment_id"] = result["id"]
    
    time.sleep(0.5)
    
    # 3.2 发表楼中楼回复
    if test_data["comment_id"]:
        test_request(
            "POST",
            f"/posts/{test_data['post_id']}/comments",
            "发表楼中楼回复",
            data={
                "content": "这是一条楼中楼回复",
                "parent_id": test_data["comment_id"]
            },
            headers=headers,
            expected_status=201
        )


def test_reactions():
    """测试表态接口"""
    print_section("4. 表态接口 (Reactions)")
    
    headers = get_auth_headers()
    
    if not test_data["post_id"]:
        print_warning("跳过表态测试：没有可用的帖子ID")
        return
    
    # 4.1 点赞
    test_request(
        "POST",
        f"/posts/{test_data['post_id']}/reactions",
        "点赞帖子",
        data={"type": "like"},
        headers=headers
    )
    
    time.sleep(0.5)
    
    # 4.2 取消点赞（Toggle）
    test_request(
        "POST",
        f"/posts/{test_data['post_id']}/reactions",
        "取消点赞（Toggle）",
        data={"type": "like"},
        headers=headers
    )
    
    time.sleep(0.5)
    
    # 4.3 抱抱
    test_request(
        "POST",
        f"/posts/{test_data['post_id']}/reactions",
        "抱抱表态",
        data={"type": "hug"},
        headers=headers
    )


def test_reports():
    """测试举报接口"""
    print_section("5. 举报接口 (Reports)")
    
    headers = get_auth_headers()
    
    if not test_data["post_id"]:
        print_warning("跳过举报测试：没有可用的帖子ID")
        return
    
    # 5.1 举报帖子
    test_request(
        "POST",
        "/reports",
        "举报帖子",
        data={
            "target_type": "post",
            "target_id": test_data["post_id"],
            "reason": "spam",
            "description": "这是一个测试举报"
        },
        headers=headers,
        expected_status=201
    )


def test_safety():
    """测试安全检测接口"""
    print_section("6. 安全检测接口 (Safety)")
    
    headers = get_auth_headers()
    
    # 6.1 检测普通文本
    test_request(
        "POST",
        "/safety/check-text",
        "检测普通文本",
        data={"content": "这是一段正常的文本"},
        headers=headers
    )
    
    time.sleep(0.5)
    
    # 6.2 检测敏感词
    test_request(
        "POST",
        "/safety/check-text",
        "检测敏感词",
        data={"content": "我感到很抑郁"},
        headers=headers
    )


def test_bottles():
    """测试漂流瓶接口"""
    print_section("7. 漂流瓶接口 (Bottles)")
    
    headers = get_auth_headers()
    
    # 7.1 扔漂流瓶
    result = test_request(
        "POST",
        "/bottles",
        "扔漂流瓶",
        data={"content": "这是一个测试漂流瓶"},
        headers=headers,
        expected_status=201,
        save_to="bottle_id"
    )
    
    time.sleep(0.5)
    
    # 7.2 捡漂流瓶（可能返回404如果没有可用的瓶子）
    result = test_request(
        "GET",
        "/bottles/draw",
        "捡漂流瓶",
        headers=headers,
        expected_status=200
    )
    # 如果返回404是正常的（没有可用的瓶子）
    if result is None:
        print_info("没有可用的漂流瓶（这是正常的）")


def test_time_capsules():
    """测试时间胶囊接口"""
    print_section("8. 时间胶囊接口 (Time Capsules)")
    
    headers = get_auth_headers()
    
    # 8.1 创建时间胶囊
    result = test_request(
        "POST",
        "/time-capsules",
        "创建时间胶囊",
        data={
            "content": "这是一个测试时间胶囊",
            "deliver_at": "2025-12-31T23:59:59"
        },
        headers=headers,
        expected_status=201,
        save_to="capsule_id"
    )
    
    time.sleep(0.5)
    
    # 8.2 获取我的时间胶囊
    test_request(
        "GET",
        "/time-capsules/my",
        "获取我的时间胶囊",
        headers=headers
    )


def test_polls():
    """测试投票接口"""
    print_section("9. 投票接口 (Polls)")
    
    headers = get_auth_headers()
    
    # 9.1 创建投票
    result = test_request(
        "POST",
        "/polls",
        "创建投票",
        data={
            "title": "你最喜欢哪个学科？",
            "options": ["数学", "语文", "英语", "物理"],
            "expires_at": "2025-12-31T23:59:59"
        },
        headers=headers,
        expected_status=201,
        save_to="poll_id"
    )
    
    if result and "id" in result:
        test_data["poll_id"] = result["id"]
    
    time.sleep(0.5)
    
    # 9.2 参与投票
    if test_data["poll_id"]:
        test_request(
            "POST",
            f"/polls/{test_data['poll_id']}/vote",
            "参与投票",
            data={"option_index": 0},
            headers=headers
        )
        
        time.sleep(0.5)
        
        # 9.3 获取投票结果
        test_request(
            "GET",
            f"/polls/{test_data['poll_id']}",
            "获取投票结果",
            headers=headers
        )


def test_utility():
    """测试工具接口"""
    print_section("10. 工具接口 (Utility)")
    
    headers = get_auth_headers()
    
    # 10.1 获取每日信息
    test_request(
        "GET",
        "/utility/daily-info",
        "获取每日信息",
        headers=headers
    )


def test_admin():
    """测试管理员接口"""
    print_section("11. 管理员接口 (Admin)")
    
    headers = get_admin_headers()
    
    # 11.1 获取仪表盘数据
    test_request(
        "GET",
        "/admin/dashboard",
        "获取仪表盘数据",
        headers=headers
    )
    
    time.sleep(0.5)
    
    # 11.2 获取待审核列表
    test_request(
        "GET",
        "/admin/audit/list",
        "获取待审核列表",
        data={"status_filter": "all"},
        headers=headers
    )
    
    time.sleep(0.5)
    
    # 11.3 获取举报列表
    test_request(
        "GET",
        "/admin/reports",
        "获取举报列表",
        headers=headers
    )
    
    time.sleep(0.5)
    
    # 11.4 审核内容（通过）
    if test_data["post_id"]:
        test_request(
            "PUT",
            f"/admin/audit/{test_data['post_id']}",
            "审核内容（通过）",
            data={
                "target_type": "post",
                "action": "approve"
            },
            headers=headers
        )


def test_delete_post():
    """测试删除帖子"""
    print_section("12. 删除帖子 (Cleanup)")
    
    headers = get_auth_headers()
    
    if test_data["post_id"]:
        test_request(
            "DELETE",
            f"/posts/{test_data['post_id']}",
            "删除测试帖子",
            headers=headers
        )


def print_summary():
    """打印测试总结"""
    print_section("测试总结")
    
    print("测试数据:")
    for key, value in test_data.items():
        if value:
            print(f"  {key}: {value}")
    
    print(f"\n{Colors.GREEN}所有接口测试完成！{Colors.END}")
    print(f"\n访问 API 文档查看更多信息:")
    print(f"  http://127.0.0.1:8000/docs")


def main():
    """主函数"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("  校园树洞 API 接口测试程序")
    print(f"{'='*60}{Colors.END}\n")
    
    print_info(f"测试目标: {BASE_URL}")
    print_info("开始测试...\n")
    
    # 0. 健康检查
    if not test_health_check():
        print_error("\n服务未启动，测试终止！")
        print_info("请先启动服务: uvicorn main:app --reload")
        return
    
    # 1. 认证
    test_auth()
    if not test_data["token"]:
        print_error("\n认证失败，测试终止！")
        return
    
    # 2-12. 其他接口测试
    test_posts()
    test_comments()
    test_reactions()
    test_reports()
    test_safety()
    test_bottles()
    test_time_capsules()
    test_polls()
    test_utility()
    test_admin()
    test_delete_post()
    
    # 总结
    print_summary()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}测试被用户中断{Colors.END}")
    except Exception as e:
        print(f"\n\n{Colors.RED}测试过程中发生错误: {str(e)}{Colors.END}")
