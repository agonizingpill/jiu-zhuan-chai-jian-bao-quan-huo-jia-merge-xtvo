        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "返潮复测与孔形",
  "module": "砖垛孔形实测",
  "caption": "砖垛孔形实测",
  "detail": "砖垛按原拆建地点编号，现场可复测湿度但不能改已合并的相关记录。",
  "path": "/brick_stacks",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "origin",
      "label": "拆建凭单"
    },
    {
      "name": "length",
      "label": "单砖长 mm"
    },
    {
      "name": "perforation",
      "label": "孔隙比"
    },
    {
      "name": "wet",
      "label": "含湿率 %"
    },
    {
      "name": "weighed",
      "label": "水分复检"
    },
    {
      "name": "pieces",
      "label": "砖数"
    },
    {
      "name": "merged",
      "label": "已合垛"
    }
  ],
  "layout": "stack",
  "view": "table",
  "actions": [
    {
      "name": "survey_stack",
      "label": "登记孔形取样垛",
      "path": "/brick_stacks/survey-stack",
      "fields": [
        {
          "name": "code",
          "label": "砖垛号",
          "kind": "text",
          "initial": "BR-X"
        },
        {
          "name": "origin",
          "label": "单据",
          "kind": "text",
          "initial": "DEMO-K"
        },
        {
          "name": "length",
          "label": "砖长 mm",
          "kind": "float",
          "initial": 194
        },
        {
          "name": "perforation",
          "label": "孔隙比",
          "kind": "float",
          "initial": 0.17
        },
        {
          "name": "wet",
          "label": "含湿率 %",
          "kind": "float",
          "initial": 9
        },
        {
          "name": "pieces",
          "label": "砖数",
          "kind": "int",
          "initial": 32
        }
      ],
      "help": "登记砖长、孔隙与湿度。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "confirm_moisture",
      "label": "复测返潮水平",
      "path": "/brick_stacks/confirm-moisture",
      "fields": [
        {
          "name": "stack",
          "label": "砖垛号",
          "kind": "text",
          "initial": "BR-X"
        },
        {
          "name": "wet",
          "label": "含湿率 %",
          "kind": "float",
          "initial": 3.6
        }
      ],
      "help": "复核湿度后保留读数。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "brick_stacks";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
