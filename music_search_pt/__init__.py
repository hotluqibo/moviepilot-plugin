"""
PT站点音乐搜索插件 for MoviePilot
基于PT站点搜索音乐资源并提供下载链接

使用方法：
1. 先启动 Mock Server: cd ~/.qclaw/workspace/mp_mock_server && python3 app.py
2. 安装插件到 MoviePilot
3. 配置 API 地址和 Key
"""

import os
import re
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

# 插件信息
__plugin_name__ = "music_search_pt"
__plugin_author__ = "QClaw"
__plugin_version__ = "1.1.0"
__plugin_description__ = "PT站点音乐搜索下载插件 v1.1"


class MusicSearchPlugin:
    """PT音乐搜索插件主类"""
    
    def __init__(self):
        self.name = __plugin_name__
        self.version = __plugin_version__
        self.session = None
        self._config = {}
        
    @property
    def plugin_info(self) -> Dict[str, Any]:
        """插件信息"""
        return {
            "name": self.name,
            "version": self.version,
            "author": __plugin_author__,
            "description": __plugin_description__,
        }
    
    def init_plugin(self, config: Dict[str, Any]) -> None:
        """初始化插件"""
        logger.info(f"[{self.name}] 初始化插件...")
        import requests
        self.session = requests.Session()
        self._config = config or {}
        self.api_key = self._config.get("api_key", "")
        self.mp_api_url = self._config.get("mp_api_url", "http://localhost:3001")
        
    def get_state(self) -> Dict[str, Any]:
        """获取插件状态"""
        return {
            "plugin": self.name,
            "version": self.version,
            "status": "running" if self.api_key else "not_configured",
            "api_url": self.mp_api_url,
            "timestamp": datetime.now().isoformat(),
        }
    
    def search_music(self, keyword: str, site: str = "moviepilot") -> List[Dict[str, Any]]:
        """
        搜索音乐
        
        Args:
            keyword: 搜索关键词
            site: 站点名称
            
        Returns:
            搜索结果列表
        """
        if not self.api_key:
            return [{"error": "请先配置 MoviePilot API Key"}]
        
        try:
            url = f"{self.mp_api_url}/api/v1/resource"
            params = {"keyword": keyword, "type": "music"}
            headers = {"Authorization": self.api_key}
            
            resp = self.session.get(url, params=params, headers=headers, timeout=10)
            data = resp.json()
            
            if data.get("success"):
                results = data.get("data", [])
                logger.info(f"[{self.name}] 搜索 '{keyword}' 找到 {len(results)} 首")
                return results
            else:
                logger.error(f"[{self.name}] 搜索失败: {data.get('message')}")
                return [{"error": data.get("message", "未知错误")}]
                
        except Exception as e:
            logger.error(f"[{self.name}] 搜索异常: {e}")
            return [{"error": str(e)}]
    
    def get_music_detail(self, music_id: str) -> Dict[str, Any]:
        """获取音乐详情"""
        if not self.api_key:
            return {"success": False, "error": "请先配置 API Key"}
        
        try:
            url = f"{self.mp_api_url}/api/v1/resource/{music_id}"
            headers = {"Authorization": self.api_key}
            
            resp = self.session.get(url, headers=headers, timeout=10)
            return resp.json()
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def add_download_task(self, resource_id: str, site: str = "moviepilot") -> Dict[str, Any]:
        """
        添加下载任务
        
        Args:
            resource_id: 资源ID
            site: 站点
            
        Returns:
            结果
        """
        if not self.api_key:
            return {"success": False, "message": "请先配置 API Key"}
        
        try:
            url = f"{self.mp_api_url}/api/v1/download"
            data = {"resource_id": resource_id, "site": site}
            headers = {"Authorization": self.api_key, "Content-Type": "application/json"}
            
            resp = self.session.post(url, json=data, headers=headers, timeout=10)
            result = resp.json()
            
            if result.get("success"):
                logger.info(f"[{self.name}] 添加下载任务: {result.get('task_id')}")
            
            return result
            
        except Exception as e:
            logger.error(f"[{self.name}] 添加下载任务异常: {e}")
            return {"success": False, "message": str(e)}
    
    def get_download_tasks(self) -> List[Dict[str, Any]]:
        """获取下载任务列表"""
        if not self.api_key:
            return []
        
        try:
            url = f"{self.mp_api_url}/api/v1/download/tasks"
            headers = {"Authorization": self.api_key}
            
            resp = self.session.get(url, headers=headers, timeout=10)
            data = resp.json()
            
            if data.get("success"):
                return data.get("data", [])
            return []
            
        except Exception as e:
            logger.error(f"[{self.name}] 获取任务列表异常: {e}")
            return []
    
    def get_sites(self) -> List[Dict[str, Any]]:
        """获取可用站点列表"""
        if not self.api_key:
            return []
        
        try:
            url = f"{self.mp_api_url}/api/v1/site"
            headers = {"Authorization": self.api_key}
            
            resp = self.session.get(url, headers=headers, timeout=10)
            data = resp.json()
            
            if data.get("success"):
                return data.get("data", [])
            return []
            
        except Exception as e:
            logger.error(f"[{self.name}] 获取站点异常: {e}")
            return []
    
    def get_plugin_stats(self) -> Dict[str, Any]:
        """获取插件统计"""
        tasks = self.get_download_tasks()
        return {
            "name": self.name,
            "version": self.version,
            "active_tasks": len(tasks),
            "timestamp": datetime.now().isoformat(),
        }
    
    def get_config(self) -> Dict[str, Any]:
        """获取配置表单"""
        return {
            "api_key": {
                "label": "API Key",
                "type": "input",
                "default": "mock_token_123",
                "required": True,
                "description": "MoviePilot API Key",
            },
            "mp_api_url": {
                "label": "API 地址",
                "type": "input",
                "default": "http://127.0.0.1:3001",
                "required": True,
                "description": "Mock Server: http://127.0.0.1:3001",
            },
        }
    
    def run_task(self) -> None:
        """定时任务"""
        logger.info(f"[{self.name}] 定时任务执行")
    
    def get_page(self) -> str:
        """获取插件页面 HTML"""
        return """
        <div class="music-search-pt">
            <h3>🎵 PT音乐搜索</h3>
            <p>使用说明：</p>
            <ol>
                <li>先启动 Mock Server</li>
                <li>配置 API 地址和 Key</li>
                <li>搜索音乐并添加下载任务</li>
            </ol>
        </div>
        """


# 导出插件实例
plugin = MusicSearchPlugin()


def get_plugin() -> MusicSearchPlugin:
    """获取插件实例"""
    return plugin


# 测试代码
if __name__ == "__main__":
    p = MusicSearchPlugin()
    p.init_plugin({"api_key": "mock_token", "mp_api_url": "http://127.0.0.1:3001"})
    
    print("=" * 40)
    print(f"🎵 {p.name} v{p.version}")
    print("=" * 40)
    
    # 测试搜索
    print("\n🔍 测试搜索 '周杰伦':")
    results = p.search_music("周杰伦")
    for r in results[:3]:
        print(f"  - {r.get('title')} ({r.get('size')}, 🧲{r.get('seeders')})")
    
    # 测试添加下载
    if results:
        print("\n📥 测试添加下载:")
        res = p.add_download_task(results[0].get("id"))
        print(f"  结果: {res}")
    
    # 测试获取任务列表
    print("\n📋 下载任务列表:")
    tasks = p.get_download_tasks()
    for t in tasks:
        print(f"  - {t}")
    
    print("\n✅ 插件测试完成!")
