const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const HTML_PATH = path.resolve('C:\\Users\\bwd001.BWD\\OneDrive - bwd group\\ドキュメント\\Claude oguro\\oguro-private\\project\\uncle_b\\名刺\\名刺デザイン_v9.html');
const OUT_FRONT = path.resolve('C:\\Users\\bwd001.BWD\\OneDrive - bwd group\\ドキュメント\\Claude oguro\\oguro-private\\project\\uncle_b\\名刺\\名刺_表面_v9.jpg');
const OUT_BACK  = path.resolve('C:\\Users\\bwd001.BWD\\OneDrive - bwd group\\ドキュメント\\Claude oguro\\oguro-private\\project\\uncle_b\\名刺\\名刺_裏面_v9.jpg');

console.log('HTML:', HTML_PATH);
console.log('存在:', fs.existsSync(HTML_PATH));

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 900, deviceScaleFactor: 2 });

  const url = 'file:///' + HTML_PATH.replace(/\\/g, '/');
  console.log('URL:', url);
  await page.goto(url, { waitUntil: 'networkidle0' });

  const front = await page.$('.card-front');
  await front.screenshot({ path: OUT_FRONT, type: 'jpeg', quality: 97 });
  console.log('表面 完了:', OUT_FRONT);

  const back = await page.$('.card-back');
  await back.screenshot({ path: OUT_BACK, type: 'jpeg', quality: 97 });
  console.log('裏面 完了:', OUT_BACK);

  await browser.close();
})();
