# 上游模块适配与执行边界

## 优先级与范围
用户目标、当前环境指令和主工作流决定范围；上游GUIDE是参考实现。只加载命中模块，不因上游示例扩展制作数量、改变艺术风格或增加付费任务。Curio中的游戏设定、真伪画作配对、动物家徽、修复经济规则是条件分支；未请求时不增加。上游的独立插件名称、allowed-tools、MCP名字和路径不会自动赋予工具能力。

## 运行环境
- 优先复用实际可用的连接或CLI，先查询版本、设备与API；保留用户指定后端。无Blender MCP时用可验证的headless Blender继续。
- Capybala的Windows路径、PowerShell、Blender 5.1.2和特定显卡实测仅代表其作者环境。Linux使用实际可执行文件；版本不同先跑小样，不复制机器路径、不强制升级。
- Blender引擎、节点socket、色彩look、GPU枚举以当前RNA/官方版本文档为准。上游EEVEE功能表和“永不使用Standard”等绝对化建议不可跨版本/风格套用；cel或准确色票场景可能需要Standard。
- 示例脚本可能清空场景；只在新进程、新blend或项目副本执行。先读脚本入口、依赖与输出路径，不在既有场景直接粘贴整段。
- 脚本本地依赖按实际导入检查；Curio requirements提供Pillow/NumPy/PyYAML范围，Blender自带bpy/NumPy。look_fit_report还需cv2；Studio的TS下载/延时摄影工具需要其完整运行时，未打包为MCP服务器；过程帧/视频由主技能scripts/render_progress.py调度。可独立用render_scene.py；未验证的扩展功能先检查依赖或使用现有工具等效实现。
- 上游链接的未打包插件/服务器和机器文件是可选外部依赖，不宣称已安装。需要时按官方来源取完整依赖，不编造路径/API；外部参考链接仅在实际需要时读取。

## 生成与艺术资源
使用当前已安装Meshy插件技能的认证/成本/异步任务规则，打包的0.6.0快照只作回退参考；复用有效认证及job，不写入密钥。ImageGen任务遵循当前图像生成技能；Curio prepare脚本或程序噪声纹理不替代真实艺术图像。来源示例截图未打包、也不作为可商用资产库；下载第三方HDRI/模型时记录各自许可证。

## 渲染与质量
不要全局套用上游固定灯功率、采样数、材质数量、黄金比例或曝光阈值。以参考图、物理尺度、风格和预算形成具体render contract；先小图再最终图。先修几何/UV/相机再校色；HDRI、辉光、雾不是必选项。保留已有合成器，避免重复降噪。GPU须探测实际可用设备，失败明确回退CPU。

已有blend预检（所有路径替换为实际路径，输出须新目录）：

```bash
BLENDER_EXECUTABLE --background --factory-startup --disable-autoexec --python-exit-code 1 --python SKILL_ROOT/modules/studio/plugins/blender-agent-studio/skills/blender-rendering-workflow/scripts/render_scene.py -- --input SCENE.blend --output-dir NEW_OUTPUT --inspect-only
```

渲染时移除 `--inspect-only`，按任务加 `--max-edge 1280 --samples 64 --device cpu`；最终尺寸按该脚本 `--render-edge` 参数指定。脚本不保存源blend；因此修复与最终打包应由搭景脚本另存工程后，再用此脚本检查/渲染。生成manifest不等于肉眼验收完成。

## 可复用与引擎级分支
普通场景保留必要的源文件、可复跑脚本和manifest即可。明确启用evolve资产晋级流程时，遵守其真实授权记录、hash锚定及引擎验证要求；执行命令本身不是审批，不伪造签字。不为了普通静态图引入整套晋级审批。

## 来源与更新
[锁定清单](source-lock.json)记录四个上游仓库的精确commit、原始路径和文件SHA256。上游SKILL.md改名GUIDE.md并同步Markdown引用，避免增加一批独立技能入口；本版安全与兼容修订由source-lock记录修改后hash。各模块LICENSE及Curio第三方声明保留。更新时复查依赖、适配规则和实际渲染小样；不得只更新文档后宣称全部功能经验证。


## 本次检查
本次结果见仓库validation-report.json及REVIEW.md。上游历史渲染成绩不是本次实测。当前未发现Blender，因此不宣称重新通过渲染或所有模块运行验证。
