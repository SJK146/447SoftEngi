d3
 .csv(“/file/Bar_cases.csv”)
 .then(makeChart);
function makeChart(data) {
      var country = data.map(function(d) {return d.province;});
      var value = data.map(function(d) {return d.cumulative_cases;});
      
/*link = window.getElementById("study1").value;

link.addEventListener("click", (event) => {
  alert("fuck this shit");
});*/