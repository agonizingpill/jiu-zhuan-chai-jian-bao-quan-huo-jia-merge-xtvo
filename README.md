# 旧砖拆建保全货架合并

西汀砖材回收站按拆建来源和孔形记录回收旧砖，返潮复查完成后封存到保全货架。

## 现场工作与联系人

模拟客户为西汀砖材回收站。砖垛拆除来源、孔形测量、批量压缩分簇、货架合垛；非承重与新近返潮垛禁止合栈。

- 拆建来源凭单 `demolitions`，字段为 `street`（来源街道）、`survey`（拆检通告）、`load_grade`（用途级别）、`allowed`（已放行拆建）。模型约束位于 `backend/domain/demolitions_model.py`，规则位于 `demolitions_service.py`。
- 砖垛孔形实测 `brick_stacks`，字段为 `origin`（拆建凭单）、`length`（单砖长 mm）、`perforation`（孔隙比）、`wet`（含湿率 %）、`weighed`（水分复检）、`pieces`（砖数）、`merged`（已合垛）。模型约束位于 `backend/domain/brick_stacks_model.py`，规则位于 `brick_stacks_service.py`。
- 货架分簇候选 `rack_candidates`，字段为 `member`（试配砖垛）、`pair`（同组砖垛）、`cluster_size`（同簇总垛数）、`token`（计算号）。模型约束位于 `backend/domain/rack_candidates_model.py`，规则位于 `rack_candidates_service.py`。
- 合垛货架卡 `rack_merges`，字段为 `candidate`（参考候选）、`rack`（保全货架）、`pieces`（合计砖数）、`operator_note`（交接标签）。模型约束位于 `backend/domain/rack_merges_model.py`，规则位于 `rack_merges_service.py`。

团队为模拟的11 人保全砖材班，负责拆建回收物登记与合垛。

工头在拆源清单和堆场板对照砖垛。孔形相近的料堆难手选，返潮复测被旧纸签覆盖，合垛完容易找不到两垛来源。

拆源许可、砖垛规格和复测值进入合架台，库员按原垛和合计块数做保全归位。

### 一天的业务操作

1. 08:10 核查拆建凭证 SX-431。
2. 09:00 记录砖垛 BR-X 的砖长 194 mm，孔隙比 0.17。
3. 10:15 复核初始湿度 9%。
4. 11:20 用 BIRCH 对同用途参考垛分簇。
5. 13:00 湿度不足以放行，货架未占用。
6. 15:10 复测湿度 3.6%，柜位 K-17 成功锁定两垛。

## 启动

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec -T backend python -m scripts.seed_demo
```

打开 `http://127.0.0.1:18326`。FastAPI OpenAPI 在 `http://127.0.0.1:19326/docs`。
Compose 运行 Nginx、Python FastAPI、独立 Redis 消费进程、SQL 数据库和 Redis，SQL 与 Redis 使用命名卷。
本机开发时，在 Python 3.11 环境安装 `backend/requirements.txt` 后从 backend 目录运行 `uvicorn core.app:app`。须提供 `DATABASE_URL`、`REDIS_URL`、`JWT_SECRET`，`SEED_DEMO` 控制演示初始化。

| 演示账号 | 权限 |
|---|---|
| operator@demo.test | 提交领域记录和计算请求 |
| reviewer@demo.test | 提交记录并执行有业务约束的复核操作 |
| viewer@demo.test | 浏览业务台账 |

三个本地演示账号均使用 `DemoC0de!2026`。角色在 `backend/core/roles.py` 和 `frontend/src/store.js` 中声明。计算状态在 worker、queueing、API 和同一前端 store 中使用。

## 页面与接口

| 业务任务 | FastAPI 路由 | 页面 |
|---|---|---|
| 拆建来源凭单 | `/demolitions` /demolitions/confirm-release | `frontend/src/pages/demolitions.js` |
| 砖垛孔形实测 | `/brick_stacks` /brick_stacks/survey-stack，/brick_stacks/confirm-moisture | `frontend/src/pages/brick_stacks.js` |
| 货架分簇候选 | `/rack_candidates` /rack_candidates/suggest-pair，/rack_candidates/record-candidate | `frontend/src/pages/rack_candidates.js` |
| 合垛货架卡 | `/rack_merges` /rack_merges/pack-rack | `frontend/src/pages/rack_merges.js` |

SQL 实体与约束在 `backend/domain` 下维护。前端使用原生 ES modules。核心算子为 Birch。在孔隙比和砖长标准化空间逐批更新 BIRCH 子簇，返回当前同簇最邻近参考垛。

模拟读数与审查范围仅用于保全操作演练。现有库存通过内置种子初始化。

[MIT](LICENSE)
