        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "保全货架合垛",
  "module": "合垛货架卡",
  "caption": "合垛货架卡",
  "detail": "湿度超过入架线时，保留候选但拒绝合垛。两个原垛一起被锁定并更新。",
  "path": "/rack_merges",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "candidate",
      "label": "参考候选"
    },
    {
      "name": "rack",
      "label": "保全货架"
    },
    {
      "name": "pieces",
      "label": "合计砖数"
    },
    {
      "name": "operator_note",
      "label": "交接标签"
    }
  ],
  "layout": "flip",
  "view": "stack",
  "actions": [
    {
      "name": "pack_rack",
      "label": "签发合垛货架卡",
      "path": "/rack_merges/pack-rack",
      "fields": [
        {
          "name": "code",
          "label": "合垛卡",
          "kind": "text",
          "initial": "PACK-24"
        },
        {
          "name": "candidate",
          "label": "候选号",
          "kind": "text",
          "initial": "COMP-24"
        },
        {
          "name": "rack",
          "label": "货架号",
          "kind": "text",
          "initial": "K-17"
        },
        {
          "name": "operator_note",
          "label": "交接标签",
          "kind": "text",
          "initial": "放墙样朝外"
        }
      ],
      "help": "两垛复检后关闭原垛，并产生一张货架卡。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "rack_merges";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
