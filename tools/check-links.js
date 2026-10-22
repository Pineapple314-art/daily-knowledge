/**
 * 来源链接可达性检测
 * 用法: node tools/check-links.js [knowledge.js 路径] [输出CSV路径]
 * 注意: 403 多为出版商反爬，不等于链接失效；404 需人工复核。
 */
const fs = require('fs');
const srcPath = process.argv[2] || 'knowledge.js';
const outPath = process.argv[3] || '';
const kb = new Function(fs.readFileSync(srcPath, 'utf8') + '\nreturn knowledgeBase;')();
const entries = kb.map(k => ({ id: k.id, title: k.title, url: k.source.url }));
const urls = [...new Set(entries.map(e => e.url))];

async function check(url) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 10000);
  try {
    const res = await fetch(url, {
      method: 'GET',
      redirect: 'follow',
      signal: controller.signal,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8'
      }
    });
    return res.status;
  } catch (e) {
    return 'ERR:' + e.name;
  } finally {
    clearTimeout(timer);
  }
}

(async () => {
  const result = {};
  const queue = [...urls];
  async function worker() {
    while (queue.length) {
      const url = queue.shift();
      result[url] = await check(url);
    }
  }
  await Promise.all(Array.from({ length: 8 }, worker));

  const rows = entries.map(e => {
    const status = result[e.url];
    return [e.id, '"' + String(e.title).replace(/"/g, '""') + '"', '"' + e.url + '"', status].join(',');
  });
  const csv = '\uFEFFid,title,url,status\n' + rows.join('\n') + '\n';

  const bucket = {};
  Object.values(result).forEach(s => {
    const key = typeof s === 'number' ? (s < 400 ? 'OK' : 'HTTP_' + s) : s;
    bucket[key] = (bucket[key] || 0) + 1;
  });

  console.log('检测 URL 数: ' + urls.length);
  console.log('结果分布: ' + JSON.stringify(bucket));
  console.log('提示: 403 通常为反爬拦截，404 才更可能是死链。');

  if (outPath) {
    fs.writeFileSync(outPath, csv, 'utf8');
    console.log('CSV 已写入: ' + outPath);
  }
})();
