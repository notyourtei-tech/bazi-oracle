# BaZi (八字) Auto Chart System

> 基于真太阳时的专业八字排盘与分析系统，支持全球 90+ 国家、6 种语言、AI 深度解读。

## ✨ 功能特性

### 核心排盘
- **真太阳时计算** — 根据城市经度（200+ 城市）进行真太阳时修正，而非简单时区转换
- **四柱八字生成** — 年柱以立春为界，月柱按节气换月，日柱公历推算，时柱按时辰划分
- **节气天文计算** — 通过太阳黄经近似公式精确定位 24 节气时刻（精度到分钟）
- **五行强弱分析** — 天干地支五行力量评分，身强身弱判断
- **神煞标注** — 20+ 神煞星曜（天乙贵人、文昌、桃花、驿马等）
- **十神分析** — 日主与其他天干的十神关系解读
- **起运与大运** — 根据节气差计算起运年龄，顺逆推算 8 步大运
- **大运流年详解** — 每步大运内逐年流年，涵盖健康、感情、财运、事业、学业、社交

### 运势系统
- **每日运势** — 基于当日干支与日主关系计算运势评分
- **每周运势** — 未来 7 天运势预测
- **每月运势** — 整月运势概览与平均分

### 综合分析
- **性格解读** — 基于日主五行、身强身弱、十神关系生成性格特征
- **人生建议** — 事业、财运、感情、健康、学业、社交全方位建议
- **神煞详解** — 每颗神煞的含义、影响、柱位说明
- **五行详解** — 各五行的性质、季节、颜色、脏腑、性格、职业建议

### AI 深度解读
- **OpenRouter 集成** — 接入大语言模型生成个性化分析
- **流式输出** — SSE 实时打字机效果展示
- **多语言 prompt** — 支持中、英、日、韩、越 5 种语言的 AI 分析

### 用户体验
- **语言选择弹窗** — 首次访问选择语言（中文、日本語、English、한국어、Tiếng Việt、မြန်မာ）
- **引导教程** — 6 步新手引导
- **我的八字** — 标记任意排盘为"我的八字"，首页常驻显示
- **暗金高级感 UI** — 粒子星空、鼠标光晕、3D 卡片倾斜、打字机动效、滚动淡入
- **PWA 支持** — Service Worker 离线缓存，可添加到手机桌面

### 导出与分享
- **分享卡生成** — 生成精美命盘图片一键保存（需 Pillow）
- **PDF 报告** — 导出专业排版的分析报告（需 ReportLab）
- **用户账号** — 登录后保存排盘历史

## 🌏 支持国家（90+）

| 地区 | 国家 |
|------|------|
| 东亚 | 中国、日本、韩国、台湾、香港、澳门、蒙古 |
| 东南亚 | 越南、泰国、菲律宾、马来西亚、新加坡、印尼、缅甸、柬埔寨、老挝、文莱 |
| 南亚 | 印度、巴基斯坦、孟加拉国、斯里兰卡、尼泊尔、马尔代夫 |
| 西亚/中亚 | 土耳其、沙特、阿联酋、卡塔尔、科威特、巴林、阿曼、以色列、约旦、黎巴嫩、伊拉克、伊朗、哈萨克斯坦、乌兹别克斯坦 |
| 欧洲 | 英国、德国、法国、意大利、西班牙、葡萄牙、荷兰、比利时、瑞士、奥地利、瑞典、挪威、丹麦、芬兰、波兰、捷克、希腊、爱尔兰、罗马尼亚、乌克兰、匈牙利、俄罗斯 |
| 美洲 | 美国、加拿大、墨西哥、危地马拉、古巴、牙买加、巴拿马、巴西、阿根廷、智利、哥伦比亚、秘鲁、委内瑞拉、厄瓜多尔 |
| 非洲 | 埃及、南非、尼日利亚、肯尼亚、加纳、摩洛哥、埃塞俄比亚、坦桑尼亚、阿尔及利亚 |
| 大洋洲 | 澳大利亚、新西兰、斐济 |

## 🚀 快速开始

### 环境要求
- Python 3.10+
- pip

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/bazi-app.git
cd bazi-app

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
flask db upgrade

# 启动应用
python app.py
```

打开 http://127.0.0.1:5000

### 可选配置

```bash
# AI 深度解读（OpenRouter）
set OPENROUTER_API_KEY=your_api_key_here

# 强制 HTTPS（生产环境）
set FORCE_HTTPS=1
```

## 📁 项目结构

```
bazi_app/
├── app.py                    # Flask 应用 & 路由
├── config.py                 # 配置（密钥、数据库、Session）
├── requirements.txt          # Python 依赖
├── migrations/               # Flask-Migrate 数据库迁移
│
├── models/
│   ├── user.py               # 用户模型（密码哈希）
│   └── chart.py              # 排盘记录模型（含 is_own 字段）
│
├── core/
│   ├── pipeline.py           # 主分析流水线（编排所有引擎）
│   ├── calendar_engine.py    # 节气天文计算 & 四柱推算
│   ├── geo_time_engine.py    # 真太阳时转换
│   ├── city_lookup.py        # 城市经度数据库（200+ 城市）
│   ├── bazi_utils.py         # 干支工具函数（五行、十神、纳音、空亡）
│   ├── wuxing_engine.py      # 五行力量评分
│   ├── shensha_engine.py     # 神煞计算（20+ 星曜）
│   ├── personality_engine.py # 性格与身强身弱分析
│   ├── interpretation_engine.py # 综合解读（神煞、五行、十神、性格、建议）
│   ├── comprehensive_analysis.py # 大运流年多维度分析
│   ├── daily_fortune_engine.py   # 每日/每周/每月运势
│   ├── compatibility_engine.py   # 双人合盘分析
│   ├── ai_engine.py          # OpenRouter AI 集成
│   ├── share_card.py         # 分享卡生成（Pillow）
│   ├── pdf_engine.py         # PDF 报告生成（ReportLab）
│   ├── security.py           # 安全模块（CSRF、限流、验证）
│   └── cache.py              # 内存缓存（LRU）
│
├── templates/
│   ├── base.html             # 基础布局（导航、弹窗、粒子、光晕）
│   ├── index.html            # 首页（表单、我的八字、今日运势）
│   ├── result.html           # 分析结果（标签页：命盘/分析/运势/建议）
│   ├── history.html          # 历史记录
│   ├── explain.html          # 系统说明与免责声明
│   ├── consult.html          # 付费咨询页
│   ├── glossary.html         # 术语表
│   ├── login.html            # 登录
│   └── register.html         # 注册
│
├── static/
│   ├── style.css             # 暗金高级感主题 CSS
│   ├── timepicker.js         # 时钟式时间选择器
│   ├── sw.js                 # PWA Service Worker
│   ├── manifest.json         # PWA 配置
│   ├── i18n/                 # 国际化（6 种语言）
│   │   ├── zh.json           # 中文
│   │   ├── en.json           # English
│   │   ├── ja.json           # 日本語
│   │   ├── ko.json           # 한국어
│   │   ├── vi.json           # Tiếng Việt
│   │   └── my.json           # မြန်မာ
│   ├── weixin.jpg            # 微信二维码
│   └── line.jpg              # LINE 二维码
│
├── data/
│   └── city_coords.json      # 城市经度数据
│
└── tests/
    └── test_core.py          # 核心引擎单元测试（23 项）
```

## 🔒 安全特性

- 请求限流（120 次/分钟/IP）
- XSS 防护（输入清理）
- CSRF 保护（所有表单和 API）
- 安全 Session 管理（HttpOnly、SameSite、30 天有效期）
- 安全响应头（HSTS、CSP、X-Frame-Options）
- 密码哈希（Werkzeug）
- 登录暴力破解防护
- 攻击路径拦截（wp-admin、phpmyadmin 等）

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python Flask、Flask-Migrate、SQLAlchemy |
| 数据库 | SQLite（开发）/ PostgreSQL（生产） |
| 前端 | HTML5、CSS3、Vanilla JavaScript |
| AI | OpenRouter API（可选） |
| 排盘 | 自研天文计算引擎 |
| i18n | 客户端 JSON 翻译系统（6 语言） |
| 导出 | Pillow（分享卡）、ReportLab（PDF） |
| PWA | Service Worker + manifest.json |

## 🧪 测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 仅运行核心引擎测试
python -m pytest tests/test_core.py -v
```

## 📱 响应式设计

- 桌面：最大宽度 1100px 居中
- 平板（≤768px）：单列布局，底部导航
- 手机（≤480px）：紧凑排版，禁用 3D 倾斜效果

## 🤝 贡献

欢迎贡献！请提交 Pull Request。

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 License

MIT License - 详见 [LICENSE](LICENSE)

---

**免责声明：** 本系统提供的八字分析属于传统文化研究范畴，仅供个人参考，不构成任何医疗、法律、投资等高风险决策的依据。如需详细个人咨询，请通过微信或 LINE 联系作者（付费服务）。
