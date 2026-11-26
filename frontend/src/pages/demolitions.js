        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "砖材拆解来源",
  "module": "拆建来源凭单",
  "caption": "拆建来源凭单",
  "detail": "记录砌体原始用途。不同用途的批次继续分开保管。",
  "path": "/demolitions",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "street",
      "label": "来源街道"
    },
    {
      "name": "survey",
      "label": "拆检通告"
    },
    {
      "name": "load_grade",
      "label": "用途级别"
    },
    {
      "name": "allowed",
      "label": "已放行拆建"
    }
  ],
  "layout": "flip",
  "view": "grid",
  "actions": [
    {
      "name": "confirm_release",
      "label": "确认拆建保全授权",
      "path": "/demolitions/confirm-release",
      "fields": [
        {
          "name": "origin",
          "label": "拆建号",
          "kind": "text",
          "initial": "DEMO-K"
        },
        {
          "name": "allowed",
          "label": "准许保全货架",
          "kind": "bool",
          "initial": true
        }
      ],
      "help": "凭拆检通告归档。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "demolitions";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
