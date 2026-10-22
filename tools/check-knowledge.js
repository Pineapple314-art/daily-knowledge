/**
 * 知识库自检脚本
 * 用法: node tools/check-knowledge.js [knowledge.js 路径]
 * 输出: 条目数、ID 连续性、冷热分布、分类数、来源数、字段完整性
 */
const fs = require('fs');
const path = process.argv[2] || 'knowledge.js';
const source = fs.readFileSync(path, 'utf8');

let kb;
try {
  kb = new Function(source + '\nreturn knowledgeBase;')();
} catch (e) {
  console.error('语法错误: ' + e.message);
  process.exit(1);
}

const ids = kb.map(k => k.id);
const sequential = JSON.stringify(ids) === JSON.stringify(ids.map((_, i) => i + 1));
const cold = kb.filter(k => k.type === 'cold').length;
const hot = kb.filter(k => k.type === 'hot').length;
const cats = [...new Set(kb.map(k => k.category))];
const urls = new Set(kb.map(k => k.source && k.source.url));
const missing = kb.filter(k =>
  !k.title || !k.content || !k.category || !k.source ||
  !k.source.name || !k.source.url || !Array.isArray(k.questions) || k.questions.length === 0
);

console.log('文件: ' + path);
console.log('条目总数: ' + kb.length);
console.log('ID 连续: ' + (sequential ? '是' : '否'));
console.log('冷知识: ' + cold + ' / 热知识: ' + hot);
console.log('分类数: ' + cats.length);
console.log('唯一来源 URL: ' + urls.size);
console.log('字段缺失条目: ' + missing.length);
if (missing.length) {
  console.log(missing.map(k => '  #' + k.id + ' ' + k.title).join('\n'));
}
process.exit(missing.length === 0 && sequential ? 0 : 1);
