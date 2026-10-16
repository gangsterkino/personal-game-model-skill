# 能力预检与接入

1. 查询当前已安装的 Blender MCP、Meshy 技能与工具定义，不猜测接口或自动启动服务。
2. 有可信 Blender CLI 时读取实际版本，使用独立后台进程、factory-startup、disable-autoexec、python-exit-code；输入工程只读，输出新目录。
3. Meshy 以当前已安装技能处理账号、预算、任务ID与恢复；不把 API key 写入项目，不自动安装历史 CLI 或另建认证存储。
4. Rodin/Hyper3D 仅在当前已授权可调用时使用；否则选 Meshy、现成资产或程序建模。服务权限不能互相代替。
5. 缺扩展或第三方运行时，先确定具体缺项，再走宿主支持的官方安装流程。未具备能力可以继续分析/设计，但不能标记生成完成。
6. Windows 可显式指定 Blender 安装路径；Linux/macOS 使用受信任的实际路径。不要执行来自不可信项目缓存的程序。
7. 依赖表及运行例子见 dependencies.md。安装完成不等于场景完成，必须真实试产及看图。
