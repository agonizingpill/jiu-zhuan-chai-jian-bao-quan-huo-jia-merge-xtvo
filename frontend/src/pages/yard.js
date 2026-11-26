import {awaitCompute, request} from '../api.js';
import {display, el} from '../dom.js';
import {COMPUTE_STATES} from '../store.js';
import {status, titleBlock} from '../widgets.js';

export const title = '堆场待复测榜';
export const key = 'yard';

const BASE = [
  ['code', '砖垛号'],
  ['origin', '拆建凭单'],
  ['initial_wet', '初测湿度 %'],
  ['length', '单砖长 mm'],
  ['perforation', '孔隙比'],
];

const pct = row => row.score === null || row.score === undefined ? '—' : (row.score * 100).toFixed(1) + '%';
const at = row => row.updated ? new Date(row.updated).toLocaleString() : '—';

function table(cols, rows) {
  return el('div', {class:'scroll'}, el('table', {},
    el('thead', {}, el('tr', {}, cols.map(([, label]) => el('th', {scope:'col'}, label)))),
    el('tbody', {}, rows.map(row => el('tr', {}, cols.map(([name, , format]) =>
      el('td', {}, format ? format(row) : display(row[name]))))))));
}

function group(caption, note, cols, rows) {
  return el('section', {},
    el('h3', {}, `${caption}（${rows.length}）`),
    el('p', {}, note),
    rows.length ? table(cols, rows) : status('暂无。'));
}

function sections(data) {
  const rankedCols = [
    ['rank', '名次', row => row.rank],
    ...BASE,
    ['score', '超标风险', pct],
    ['updated', '出分时间', at],
  ];
  return [
    el('h2', {}, '待复测垛返潮风险'),
    group('风险榜', '按复测超 6% 风险从高到低排列，复测员先查榜前的垛。',
      rankedCols, data.ranked.map((row, index) => ({...row, rank: index + 1}))),
    group('无法估计', '训练样本缺超标或未超标垛，暂无法估计。', BASE, data.unestimable),
    group('待出分', '已登记初测，等待评分。', BASE, data.waiting),
    group('缺初测', '缺初测湿度的垛不进训练也不出分。', BASE, data.unscorable),
  ];
}

export async function render(root, role) {
  const panel = el('section', {class:'ledger', 'aria-label':'堆场待复测榜'});
  const notice = status('');
  const refresh = async () => {
    try {
      const data = await request('/yard');
      panel.replaceChildren(...sections(data));
    } catch (error) {
      panel.replaceChildren(status(error.message, 'error'));
    }
  };
  const side = [];
  if (role !== 'viewer') {
    const button = el('button', {type:'submit'}, '评估待复测垛');
    const form = el('form', {class:'action'},
      el('h3', {}, '评估待复测垛'),
      el('p', {}, '用初测湿度和孔形预测复测超 6% 的风险；训练排除与待测垛同拆建凭单的样本。'),
      button, notice);
    form.addEventListener('submit', async event => {
      event.preventDefault();
      button.disabled = true;
      notice.className = 'status';
      try {
        const data = await request('/yard/assess', {});
        const result = await awaitCompute(data.token, current => {
          notice.textContent = COMPUTE_STATES[current.status] || current.status;
        });
        if (result.status === 'rejected') throw new Error(result.detail);
        if (result.status === 'stale') {
          notice.textContent = result.detail || '该批分数已作废';
        } else {
          const done = result.result || {};
          notice.textContent = done.state === 'unestimable'
            ? '缺超标或未超标样本，无法估计'
            : `已出分 ${(done.admitted || []).length} 垛`;
        }
        notice.classList.add('ok');
      } catch (error) {
        notice.textContent = error.message;
        notice.classList.add('error');
      } finally {
        button.disabled = false;
        await refresh();
      }
    });
    side.push(el('section', {class:'actions'}, form));
  }
  root.replaceChildren(
    titleBlock('堆场', '待复测垛返潮风险榜', '复测值更正后旧分立即失效并重算，其余照排；复测入账的垛即撤下，晚到的旧分不回榜。'),
    el('div', {class:'work stack'}, panel, ...side));
  await refresh();
}
