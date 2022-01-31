var pieColors = [
  "#AEF091", "#A8ABF0", "#F0837D", "#7FD4F0", "#E397F0", "#F0C930", "#F0A497", "#81A352", "#58F0AE", "#658BF0"
]

var scaleColors = [
  "#AEF091", "#A8ABF0"
]

var Piechart = function(options) {
  this.options = options;
  this.canvas = document.createElement("canvas");
  this.canvas.width = 200;
  this.ctx = this.canvas.getContext("2d");
  this.colors = options.colors;
  this.bgcolor = options.bg || "#ffffff";
  this.ctx.fillStyle = this.bgcolor;
  this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
  this.draw();
  if (options.legend) {
    this.showLegend();
  }
  if (this.options.holeSize > 0) {
    this.addHole(this.options.holeSize);
  }

  var result = document.createElement("div");
  result.classList.add("piechart-container");

  var a_result;
  if (this.options.href) {
    a_result = document.createElement("a");
    a_result.href = this.options.href;
  }
  else {
    a_result = document.createElement("div");
  }

  if (options.title) {
    var title = document.createElement("h3");
    title.innerHTML = options.title;
    a_result.appendChild(title);
  }

  if (options.subtitle) {
    var title = document.createElement("h5");
    title.innerHTML = options.subtitle;
    a_result.appendChild(title);
  }
  a_result.appendChild(this.canvas);
  if (options.legend) {
    a_result.appendChild(this.legend);
  }

  result.appendChild(a_result);
  return result;

}

Piechart.prototype.drawPieSlice = function(ctx,centerX, centerY, radius, startAngle, endAngle, color) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(centerX,centerY);
  ctx.arc(centerX, centerY, radius, startAngle, endAngle);
  ctx.closePath();
  ctx.fill();
}

Piechart.prototype.draw = function() {
  var total_value = 0;
  var colorIndex = 0;
  for (var categ in this.options.data){
    var val = this.options.data[categ];
    total_value += val;
  }

  var start_angle = 0;
  for (categ in this.options.data){
    val = this.options.data[categ];
    var slice_angle = 2 * Math.PI * val / total_value;
    this.drawPieSlice(this.ctx, this.canvas.width / 2, this.canvas.height / 2,
      Math.min(this.canvas.width / 2,this.canvas.height / 2),
      start_angle, start_angle + slice_angle, this.colors[colorIndex % this.colors.length]
    );
    start_angle += slice_angle;
    colorIndex++;
  }
}

Piechart.prototype.addHole = function(holeSize) {
  if (holeSize){
    this.drawPieSlice(this.ctx, this.canvas.width / 2, this.canvas.height / 2,
      holeSize * Math.min(this.canvas.width / 2,this.canvas.height / 2),
      0, 2 * Math.PI, this.bgcolor
    );
  }
}

Piechart.prototype.showLegend = function() {
  this.legend = (this.options.legend) ? document.createElement("div") : "";
  this.legend.classList.add("piechart-legend");
  if (this.options.legend) {
    colorIndex = 0;
    var legendContent = "";
    for (categ in this.options.data){
      legendContent += `
      <div class="piechart-legend-category">
        <span class='color-sample' style='background-color:${this.colors[colorIndex++]};'>
          &nbsp;
        </span>
        <span>${categ}</span>
      </div>`;
    }
    this.legend.innerHTML = legendContent
  }
}

var ScaleBar = function(options) {
  var average = (array) => array.reduce((a, b) => a + b) / array.length;
  var point = ((average(options.data) - options.dataRange[0]) / Math.abs(options.dataRange[1] - options.dataRange[0])) * 100
  if (point > 96) {
    point = 96;
  }
  this.options = options;
  this.div = document.createElement("div");
  this.div.classList.add("scalechart-container");
  if (!options.border) {
    this.div.style.border = "0px";
  }
  var subtitle = (options.subtitle) ? `<h5>${options.subtitle}</h5>` : "";
  var legend = (options.legend) ? `<div class="scalechart-num">
    <div style="left:${point}%">${average(options.data).toFixed(1).replace(".0", "")}</div>
  </div>` : "";
  this.div.innerHTML += `
    <h3>${options.title}</h3>
    ${subtitle}
    <div class="scalebar-container">
      ${legend}
      <span>${options.dataRange[0]}</span>
      &nbsp;
      <div class="scale-bar" style="background-image: linear-gradient(to right, ${options.colors[0]}, ${options.colors[1]});">
        <div class="scale-bar-before" style="left:${point}%;"></div>
      </div>
      &nbsp;
      <span>${options.dataRange[1]}</span>
    </div>`;
  return this.div;
}
