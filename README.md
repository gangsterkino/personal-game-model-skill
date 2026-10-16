# Personal Game Model Skill

参考图 → 资产清单 → 主动研究制作经验 → 现成模型/贴图/特效直接复用 → 建模或Meshy生成 → 组装 → 灯光渲染 → 实图对照 → 可编辑工程交付。

## 完整模块

- Curio九类：机械、拆件封口、油画、画框、珠宝、2.5D角色、修复交互、资产演进、Meshy。
- cc-blender：灯光、渲染、参考外观校准及指标脚本。
- Blender Agent Studio：作者场景保留、预检渲染、真实制作检查点与过程视频入口。
- Capybala bpy：几何、建筑、材质、组件、比例、自然环境、三视图、细节、风格和场景库。
- 主工作流：经验检索、资源许可、断点恢复、火焰烟水等方法选择、视觉验收。

包含详细文档、代码、模板和许可证，不再是此前8个Markdown摘要。文件来源和修改后hash见 [source-lock.json](skills/build-reference-scene/references/source-lock.json)，修改与测试范围见 [REVIEW.md](REVIEW.md)。

## 使用

将整个 `skills/build-reference-scene/` 安装至客户端支持的技能目录，再调用 `$build-reference-scene`。内部modules按需加载，不单独安装。

> 用 build-reference-scene 美化这个场景。主动检索制作经验；难复刻的物件、材质和特效优先找许可合适的现成资源直接采用。保留原工程，交付同镜头前后对照和可编辑工程。

[依赖与入口](skills/build-reference-scene/references/dependencies.md)。模块收录不代表工具已安装或全部运行验证。本次为离线回归，当前环境无Blender，未重跑渲染。GitHub保存不等于ChatGPT已安装或通过平台扫描。

保留四个来源的MIT许可证与Curio第三方声明，不分发受单独限制的展示截图和源模型。来源见 [SOURCES.md](SOURCES.md)。
