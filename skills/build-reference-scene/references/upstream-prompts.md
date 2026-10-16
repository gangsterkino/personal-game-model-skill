# 可复用提示词与清单

资产图提示词：
“根据参考图提取主要独特物件，制作整洁的三维资产参考清单。每种物件只出现一次，保留轮廓、材质和配色；完整呈现，不重叠，纯色背景，留足裁剪间距；不含场景地面、投影和装饰文字。被遮挡部分合理补全并说明推测。”

快速调用：
“用 $build-reference-scene 把这张图做成可编辑的 Blender 场景，先低成本草模，再试产一个主体，通过后复用资产完成搭景。”

宠物项圈场景：
“用 $build-reference-scene 做宠物智能项圈产品展示场景，以我提供的产品图为准。先给静态预览；未提供的功能不添加，动画另行制作。”

manifest 最小结构：
```json
{"schema_version":1,"reference":null,"units":"meters","assets":[{"id":"a01","name":"主体","count":1,"method":"procedural","status":"planned","job_id":null,"model_path":null,"crop_px":null,"dimensions_m":[1,1,1],"position_m":[0,0,0],"rotation_deg":[0,0,0]}]}
```

用 scripts/manifest.py init 路径 初始化；用 check 路径 验证标识唯一性、状态和数量。按真实结果填充，禁止为了通过检查伪造 job id。
