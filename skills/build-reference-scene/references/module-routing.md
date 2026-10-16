# 模块路由与阶段交接

先读本表，再只读命中的 GUIDE；路径相对本文件。模块作为主技能的参考能力，不是独立安装的插件。执行前读 [适配规则](integration.md)。

| 模块 | 启用条件与插入阶段 | 入口 | 必须交接的结果 |
|---|---|---|---|
| curio-mechanism-workshop | 机械、古董器械、铰链或运动结构；拆图后、建模前 | [GUIDE](../modules/curio/skills/curio-mechanism-workshop/GUIDE.md) | 尺寸/BOM、轴与接口、可运动体块、部件ID；按请求交付运动验证 |
| mesh-split-fill | 已有网格需语义拆件、封口或独立编辑；导入后 | [GUIDE](../modules/curio/skills/mesh-split-fill/GUIDE.md) | 原件只读、接缝契约、最难接缝试产、分件与重导入QA；不默认封闭设计孔洞 |
| curio-oil-paintings | 场景内油画、画芯、表面笔触或指定真伪变化；材质阶段 | [GUIDE](../modules/curio/skills/curio-oil-paintings/GUIDE.md) | 实际画芯、配准材质、斜光检验；prepare脚本只出任务说明，不代表画已完成 |
| curio-frame-workshop | 画框、徽章、批量长宽比变化；资产阶段 | [GUIDE](../modules/curio/skills/curio-frame-workshop/GUIDE.md) | 独立画芯/框/徽章、物理UV、GLB/blend、正面与斜视预览 |
| curio-jewelry-workshop | 宝石、珠宝、玻璃饰物；建模与材质阶段 | [GUIDE](../modules/curio/skills/curio-jewelry-workshop/GUIDE.md) | 真实厚度、刻面法线、镶口配合、透射检验；游戏近似明确标注 |
| noir-character-pipeline | 用户要求2.5D可重打光角色立绘；贴图阶段 | [GUIDE](../modules/curio/skills/noir-character-pipeline/GUIDE.md) | 对齐底色/alpha/形体normal、左右光及开关对照；不是绑定3D角色 |
| curio-part-finishing | 用户要求游戏内打磨、加工、修复交互；引擎阶段 | [GUIDE](../modules/curio/skills/curio-part-finishing/GUIDE.md) | 连续接触去料、过切失败、合格件与手动安装、真实运行验证；静态场景不启用 |
| evolve-blender-assets | 要求可复用参数资产、版本审计或引擎级交付 | [GUIDE](../modules/curio/skills/evolve-blender-assets/GUIDE.md) | 与资产hash对应的质量契约、round-trip报告；引擎级须真实引擎证据 |
| meshy-3d-generation | 独立复杂造型的生成/重贴图；试产与批量阶段 | [备份GUIDE](../modules/curio/skills/meshy-3d-generation/GUIDE.md) | 优先读取当前已安装Meshy技能；成本、job ID、可恢复状态、模型及预览 |
| blender-lighting | 所有需要新建/调优灯光的三维场景 | [GUIDE](../modules/cc-blender/plugin/skills/blender-lighting/GUIDE.md) | 与场景尺度相符的主/补/轮廓光或环境光；保留参考图光向 |
| blender-rendering | 所有三维图像输出；预览与最终渲染 | [GUIDE](../modules/cc-blender/plugin/skills/blender-rendering/GUIDE.md) | 实际引擎/设备/采样/色彩/尺寸记录、实际图像 |
| reference-look-calibration | 参考图复刻，或色相/明暗/主体占比偏差 | [GUIDE](../modules/cc-blender/plugin/skills/reference-look-calibration/GUIDE.md) | 几何和相机锁定后比对区域、颜色、亮度；对照图及指标辅助肉眼判断 |
| blender-rendering-workflow | 已有blend的渲染预检、保留作者光照、可重跑交付 | [GUIDE](../modules/studio/plugins/blender-agent-studio/skills/blender-rendering-workflow/GUIDE.md) | render-manifest、缺依赖清单、实际预览、干净进程重现 |
| capybala-bpy-skill | 程序化建模、组件审查、可维护场景脚本 | [GUIDE](../modules/bpy/GUIDE.md) | 设计→搭建→视觉评审、组件和朝向检查、可重跑脚本；按主题取assets中的库 |

## 默认全流程

1. 预检与恢复：发现真实工具、版本、认证、已有任务和资产；建立项目manifest。
2. 设计与拆图：布局/相机体块、独特资产清单、目标尺寸；机械任务补BOM；记录模块选择。
3. 生产：先检索可直接复用的合适资产；缺合适资源的复杂独立物件走Meshy或已授权Rodin，规则形体走bpy；单件试产后继续批量。画框/珠宝/机械按类型插入；需要拆件时先做接缝试产。
4. 材质与组装：独立命名/实例复用、尺度落地、贴图配准；油画/2.5D仅处理命中资产。
5. 灯光与预览：先落实参考光向和构图，再调材质、环境、曝光；使用已验证引擎/设备。复刻任务加载look calibration。
6. 视觉复核：检查真实渲染的剪影、接触、遮挡、反射、纹理密度、曝光、噪声。指标不能代替看图；回到错误所属阶段修复。
7. 最终交付：打包依赖、干净进程重新打开blend并渲染，更新manifest；动画/游戏交互另需相应实测，不能用静态图替代。

## 状态与断点

保留已有manifest字段，增补 `workflow.modules`（名称、原因、输入、输出、status）及 `workflow.render_contract`（相机、帧、引擎、设备、尺寸、采样、色彩、时间预算）。模块status用 pending/running/complete/blocked；只有实际输出与检查齐全才能complete。每次修改记录受影响资产与检查，不重跑无关付费生成。把预览、最终渲染和引擎运行结果分别记录。

## 快速调用示例

- “按参考图做完整场景”：默认流程＋参考外观校准；不中途停在一个模型。
- “只改善现有blend灯光”：灯光＋渲染工作流；保留几何、相机和已接受的材质。
- “做一组可换尺寸的油画框”：画框＋bpy＋渲染；已有画芯不重新生成。
- “模型分成独立零件并封口”：拆件模块；只有明确要求打印时再用已安装的3D打印技能。
- “角色立绘能左右打光”：2.5D模块；风格沿用用户参考，不强制动物黑色电影风。
