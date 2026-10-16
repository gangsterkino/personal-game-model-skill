# 依赖、运行入口与边界

本包含14个模块方向的源码、步骤、参数模板与许可证，不包含Blender、Meshy服务或游戏运行时。

| 能力 | 已包含入口 | 外部依赖 | 本次验证 |
|---|---|---|---|
| 断点恢复 | scripts/manifest.py | Python | init/check/覆盖拒绝 |
| 机械、珠宝、修复 | Curio对应GUIDE及references | Blender/用户引擎工程 | 静态检查 |
| 拆件封口 | mesh-split-fill/scripts | 标准库；导入渲染需要Blender | 21项通过，2项集成跳过 |
| 油画任务/PBR | prepare_painting.py、paint_surface.py | NumPy、Pillow；艺术画芯用图像工具 | 实际32×40技术表面生成 |
| 画框 | frame_workshop.py及辅助库 | Blender | 语法与保护检查 |
| 角色贴图 | check_character_maps.py | Pillow | 报告覆盖回归 |
| 质量契约 | evolve-blender-assets/scripts | Python；真实引擎证据 | 静态检查 |
| Meshy | 历史GUIDE/参数参考 | 当前已安装Meshy技能及授权预算 | 未新增付费任务 |
| 灯光/校准 | cc-blender GUIDE及look_fit_report.py | Blender；指标需OpenCV、NumPy | 语法/输出保护 |
| 作者场景渲染 | studio/.../scripts/render_scene.py | Blender | 静态检查，未重跑渲染 |
| 过程帧/视频 | scripts/render_progress.py | Blender；MP4另需FFmpeg | CLI检查，未实际编码 |
| PBR/HDRI下载 | studio/.../scripts/poly-haven-cli.ts | 已安装Bun与允许的网络 | 静态检查，未联网 |
| 模型/参考图下载 | bpy/assets/asset_fetch_lib.py | Blender；任务下载配置 | 离线路径/限额/覆盖回归 |
| 程序建模/自然 | bpy/assets/*_lib.py、scene_pkg | Blender；部分函数需Sapling/ANT/Extra Mesh | 语法检查，扩展未打包 |

## 隔离执行

清场、生成器、T.main和模板只在新后台进程及新输出目录执行。当前工程先另存副本。对受审阅本地脚本使用 `--python`；禁用autoexec不等于沙箱化显式Python代码。宿主进程设置超时。

```text
BLENDER_PATH --background --factory-startup --disable-autoexec --python-exit-code 1 --python SKILL_ROOT/modules/studio/plugins/blender-agent-studio/skills/blender-rendering-workflow/scripts/render_scene.py -- --input PROJECT/scene.blend --output-dir PROJECT/preview-v1 --inspect-only
```

核对后去掉inspect-only并按实际参数指定尺寸/采样/设备。脚本只预检部分图片与库，字体、UDIM、音视频、模拟缓存仍需检查及重开验证。

## 任务下载配置

Python下载默认关闭；先核对服务条款与资产许可，再显式调用 `configure_downloads(project_cache, ['api.polyhaven.com','dl.polyhaven.org'], max_bytes=268435456)`。参考图域名仅来自实际选定来源。拒绝非HTTPS、未配置域名、重定向、缓存越界、已有文件覆盖与超额响应。缓存hash用于发现本地变化，不是作者签名。遇403等错误记录并遵守限制。

历史机器路径、MCP名字、测试成绩、版本及UI规则不是当前能力。外链指向来源快照，不表示本地存在对应工具。当前Meshy技能优先于旧CLI例子。仅启用命中的模块，不自动安装全部依赖。

`manifest.py check`只验证结构、ID、数量与任务状态，不检查文件存在、成本、许可或视觉结果；这些必须通过实际工具与看图单独核对。render_scene.py不保存修复后的工程，修复要另存副本后再渲染验收。
