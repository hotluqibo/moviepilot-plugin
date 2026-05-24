# MoviePilot 插件集合

本仓库包含多个 MoviePilot 插件，用于扩展 MoviePilot 功能。

## 📦 插件列表

### 1. 朱雀抽奖插件（`zhuque_lottery/`）

自动抽取朱雀站点喇叭球，显示灵石余额，支持定时任务和消息推送。

**功能：**
- 自动抽奖：定时抽取朱雀站点喇叭球
- 灵石余额：实时显示朱雀灵石余额
- 余额对比：抽奖前后余额对比
- 消息推送：抽奖结果推送到微信/Telegram
- 定时任务：支持 Cron 表达式定时抽奖
- 灵石提醒：低于设定阈值时提醒

**安装：**
1. 打开 MoviePilot 插件管理
2. 点击"从 GitHub 安装"
3. 输入仓库 URL：`https://github.com/hotluqibo/moviepilot-plugin`
4. 选择插件：`zhuque_lottery`
5. 点击"安装"
6. 等待安装完成

**配置：**
| 配置项 | 说明 | 获取方法 |
|--------|------|----------|
| ✅ 启用插件 | 开启/关闭插件 | 开关 |
| 🍪 朱雀 Cookie | 登录朱雀后的 Cookie | 浏览器 F12 → Application → Cookies → `socute` |
| 🔑 CSRF Token | 从朱雀页面获取 | 浏览器 F12 → Network → 查看请求头 |
| ⏰ 定时任务 | Cron 表达式 | `0 8 * * *`（每天早上8点） |
| 💰 灵石阈值 | 低于此值时提醒 | `1000.0` |
| 📢 开启通知 | 抽奖后发送通知 | 开关 |

## 🚀 安装方法

### 方法 1：从 GitHub 安装（推荐）

1. 打开 MoviePilot 插件管理
2. 点击"从 GitHub 安装"
3. 输入仓库 URL：
   ```
   https://github.com/hotluqibo/moviepilot-plugin
   ```
4. 选择要安装的插件
5. 点击"安装"
6. 等待安装完成

### 方法 2：手动安装

1. 下载插件代码：进入对应插件目录，下载 `__init__.py`
2. 打开 MoviePilot 插件管理
3. 点击"本地安装"
4. 上传 `__init__.py` 文件
5. 等待安装完成

## 📝 配置插件

安装后，需要配置：

1. 启用插件
2. 填写配置项（如 Cookie、CSRF Token 等）
3. 保存配置
4. 测试插件功能
5. 设置定时任务（可选）

## 🧪 测试插件

配置完成后：

1. 保存配置
2. 在插件页面点击测试按钮
3. 查看运行结果
4. 检查微信/Telegram 是否收到通知

## 📚 插件开发

### 目录结构

```
moviepilot-plugin/
├── README.md                    # 本文件
└── zhuque_lottery/            # 朱雀抽奖插件
    ├── __init__.py             # 插件主文件
    └── README.md              # 插件说明文档
```

### 添加新插件

1. 创建插件目录：`mkdir new_plugin`
2. 创建插件主文件：`touch new_plugin/__init__.py`
3. 编写插件代码（继承 `_PluginBase`）
4. 提交到本仓库
5. 在 MoviePilot 中安装测试

## 🤝 贡献

欢迎提交 Pull Request 添加新的插件！

## 📄 许可证

MIT License

## 📞 支持

如有问题，请在 GitHub 仓库提交 Issue。
