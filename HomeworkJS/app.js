// from data.js
var tableData = data;

var tbody = d3.select("tbody");

function show(data) {
  tbody.html("");
  data.forEach((UFOReport) => {
    var row = tbody.append("tr");
    Object.entries(UFOReport).forEach(([key, value]) => {
      var cell = tbody.append("td");
      cell.text(value);
    });
  });
}

show(tableData);

var submit = d3.select("#filter-btn");

submit.on("click", function() {

  // Prevent the page from refreshing
  d3.event.preventDefault();

  // Select the input element and get the raw HTML node
  var inputElement = d3.select("#datetime");

  // Get the value property of the input element
  var inputValue = inputElement.property("value");

//   console.log(inputValue);
//   console.log(tableData[0]);

  var filteredData = tableData.filter(tableData => tableData.datetime === inputValue);

//   console.log(filteredData);

  show(filteredData);

});