let express = require('express');
var bodyParser = require('body-parser');
let fs = require('fs');
let app = new express();

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }))

// parse application/json
app.use(bodyParser.json())
app.set('view engine', 'ejs');

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/html/home.html');
});

app.post('/input', (req, res) => {
  fs.writeFileSync('./data/text.txt', req.body.input.trim());
  fs.writeFileSync('./data/domain.txt', req.body.domain.trim());
  const { exec } = require('child_process');
  exec('python Project3.py', (err, stdout, stderr) => {

  });
  res.sendFile(__dirname + '/html/wait.html');
});

app.get('/getResult', (req, res) => {
  let tf = require('@tensorflow/tfjs-node');
  let readModel = function () {
    return new Promise(async (res, rej) => {
      let tf = require('@tensorflow/tfjs-node');
      const model = await tf.loadLayersModel('file://model/model.json');
      res(model)
    })

  }

  readModel().then((_model) => {
    let arrayMax = [73, 106.1, 101, 87, 10, 9, 45, 1, 73, 1, 91.33333333333331, 1974, 3.6319999999999997]
    let normalize_input = function (arrayInput) {
      for (let j = 0; j < arrayInput.length; j++) {
        arrayInput[j] = arrayInput[j] / arrayMax[j]
      }
      return arrayInput;
    }
    let model = _model;
    let inputData = fs.readFileSync('./data/input.csv', 'utf-8').trim().split('\n');
let domain = fs.readFileSync('./data/domain.txt', 'utf-8').trim();
    let arrColumns = ['count_paragraph', 'average_words_in_paragraph', 'count_positive', 'count_negative', 'count_image', 'count_date', 'num_num_in_df', 'percent_num_start_1', 'numberRecordDomain', 'percentFraudDomain', 'average_words', 'noun', 'num_per_cha(%)']
    let arrDomain = ['binhluan.biz', 'www.ipick.vn', 'tintucqpvn.net', 'www.gioitreviet.net', 'giadinhtiepthi.com', 'suckhoe.vnexpress.net', 'phapluat.news', 'autoxe.net', 'thegioitre.vn', 'baoangiang.com.vn', 'thoibao.today', 'haiduong.tintuc.vn', 'laodong.vn', 'sorry.vn', 'thoibao.de', 'baonuocmy.com', 'tinvn.info', 'www.vietgiaitri.com/', 'https://news.zing.vn', 'news.zing.vn', 'thanhnien.vn', 'vnexpress.net', 'giaitri.vnexpress.net', 'thethao.tuoitre.vn', 'tuoitre.vn', 'kinhdoanh.vnexpress.net', 'dulich.vnexpress.net', 'sohoa.vnexpress.net', 'doisong.vnexpress.net', 'dantri.com.vn']
    let arrNumberRecord = [1, 2, 5, 1, 2, 1, 3, 1, 2, 1, 6, 1, 1, 1, 2, 1, 68, 1, 1, 6, 5, 73, 2, 10, 5, 3, 1, 1, 2, 14]
    let arrFraud = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    let input = [];
    for (let i = 0; i < arrColumns.length; i++) {
      if (arrColumns[i] == 'numberRecordDomain') {
        let domain = fs.readFileSync('./data/domain.txt', 'utf-8').trim();
        for (let t = 0; t < arrDomain.length; t++) {
          if (domain == arrDomain[t]) {
            input.push(arrNumberRecord[t]);
            break;
          }
        }
      } else if (arrColumns[i] == 'percentFraudDomain') {
        for (let t = 0; t < arrDomain.length; t++) {
          if (domain == arrDomain[t]) {
            input.push(arrFraud[t]);
            break;
          }
        }
      } else {
        for (let j = 0; j < inputData[0].split(',').length; j++) {
          if (arrColumns[i] == inputData[0].split(',')[j]) {
            input.push(inputData[1].split(',')[j]);
            break;
          }
        }
      }
    }
    let temp_input=input;
    let a = Math.round(model.predict(tf.tensor2d(normalize_input(input), [1, 13])).arraySync()[0][0]);
    let result;
    if(a==1) result='fake';
    else result= 'real'
    let text=fs.readFileSync('./data/text.txt')
    res.render('result',{result:result,text:text,domain:domain,arrColumns:arrColumns,input:temp_input})

  })
})

app.listen(8080 || process.env.PORT, () => {
  console.log('hello')
})