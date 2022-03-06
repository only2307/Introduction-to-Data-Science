let tf = require('@tensorflow/tfjs-node');
let fs = require('fs');
let maxNumber=0;
let arrayMax=[0,0,0,0,0,0,0,0,0,0,0,0,0];
let normalize_number=function(array){
  let max=0;
  for(let i=0;i<array.length;i++){
    for(let j=0;j<array[i].length;j++){
      if(array[i][j]>arrayMax[j]){
        arrayMax[j]=array[i][j]
      }
    }
  }
  for(let i=0;i<array.length;i++){
    for(let j=0;j<array[i].length;j++){
      array[i][j]=array[i][j]/arrayMax[j]
    }
  }
 console.log(arrayMax)
  return array;
}
let normalize_input=function(arrayInput){
  for(let j=0;j<arrayInput.length;j++){
      arrayInput[j]=arrayInput[j]/arrayMax[j]
    }
  return arrayInput;
}
// Define a model for linear regression.
const model = tf.sequential();
model.add(tf.layers.dense({ units: 13, inputShape: [13] }));
model.add(tf.layers.dense({ units: 13 }));
model.add(tf.layers.dense({ units: 13 }));

model.add(tf.layers.dense({ units: 5 }));
model.add(tf.layers.dense({ units: 5 }));
model.add(tf.layers.dense({ units: 1 }));
// model.add(tf.layers.dense({ units: 4}));
// Prepare the model for training: Specify the loss and the optimizer.
model.compile({
  loss: 'meanSquaredError',
  metrics: ['accuracy'],
  optimizer: 'sgd'
});


// read data. 
let dataRaw = fs.readFileSync('./data/data_train.txt', 'utf-8').trim().split('\n');

let data = { xTrain: [], yTrain: [] }
for (let i = 0; i < dataRaw.length; i++) {
  let line = dataRaw[i].split(',');
  for (let i = 0; i < line.length; i++) line[i] = parseFloat(line[i])
  let output = [parseFloat(line.shift())]
  let input = line;
  data.xTrain.push(input);
  data.yTrain.push(output)
}
normalize_number(data.xTrain)

const xs = tf.tensor2d(data.xTrain, [
  data.xTrain.length,
  data.xTrain[0].length
]);
const ys = tf.tensor2d(data.yTrain, [
  data.yTrain.length,
  data.yTrain[0].length
]);
// model.fit(xs, ys, { epochs: 500 }).then(() => {
//   // Use the model to do inference on a data point the model hasn't seen before:
//   // model.predict(tf.tensor2d(normalize_input([10,45.454545,36,18,0,2,11,0.272727,14,0.0,39.727273,420,3.395]), [data.yTrain[0].length, data.xTrain[0].length])).print();
//   model.save('file://model')
// });

