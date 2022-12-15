// D3.js | Heat map
// See: https://d3-graph-gallery.com/graph/heatmap_style.html

// set the dimensions and margins of the graph

function exposeHeatMapRender() {
  
  const d3HeatMapRender = document.getElementById('d3HeatMapResult');

  if (undefined !== d3HeatMapRender){
    d3HeatMapRender.innerHTML = '';
  }

  var margin = {top: 15, right: 25, bottom: 20, left: 40},
    width = 1100 - margin.left - margin.right,
    height = 145 - margin.top - margin.bottom;
  
  // append the svg object to the body of the page
  var svg = d3.select("#d3HeatMapResult")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");
  
  // The server-side return a non readable word, this function will improve the human readability.
  // "helloWorld" -> "Hello World"
  function improveSyntax(word) {
    wordCapitalized = word[0].toUpperCase() + word.slice(1, word.length);
    wordSeparated = wordCapitalized.match(/[A-Z][a-z]+/g);
  
    return wordSeparated.join(' ');
  }

  // Fetch the higher visited value in order to expose a correct message.
  // The higher visited value it's required to render the amount of visited times through the node.
  fetch(`${apiUrl}/result/collect/higher-visited-concept`, {method: 'GET'})
    .then((response) => response.json())
    .then((higherValue) => {
      // Fetch an object for translate words on heat map.
      fetch(`${apiUrl}/result/collect/heat-map-reference?clean=true&reverse=true`, {method: 'GET'})
        .then((response) => response.json())
        .then((translateObject) => {
  
            // Read the data
            const csvRoute = `${apiUrl}/result/collect/heat-map`;
            d3.csv(csvRoute, function(data) {  // Fetch the data object to pass into the heat map render.
              // Labels of row and columns -> unique identifier of the column called 'group' and 'variable'
              var myGroups = d3.map(data, function(d){
                return d.group;
              }).keys()
      
              var myVars = d3.map(data, function(d){
                return d.variable;
              }).keys()
      
              // Build X scales and axis:
              var x = d3.scaleBand()
                .range([ 0, width ])
                .domain(myGroups)
                .padding(0.05);
              svg.append("g")
                .style("font-size", 15)
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x).tickSize(0))
                .select(".domain").remove()
            
              // Build Y scales and axis:
              var y = d3.scaleBand()
                .range([ height, 0 ])
                .domain(myVars)
                .padding(0.05);
              svg.append("g")
                .style("font-size", 15)
                .call(d3.axisLeft(y).tickSize(0))
                .select(".domain").remove()
            
              // Build color scale
              var myColor = d3.scaleSequential()
                .interpolator(d3.interpolateInferno)
                .domain([1,100])
            
              // create a tooltip
              var tooltip = d3.select("#d3HeatMapResult")
                .append("div")
                .style("opacity", 0)
                .attr("class", "tooltip")
                .style("background-color", "white")
                .style("border", "solid")
                .style("border-width", "2px")
                .style("border-radius", "5px")
                .style("padding", "5px")
            
              // Three function that change the tooltip when user hover / move / leave a cell
              var mouseover = function(d) {
                tooltip
                  .style("opacity", 1)
                d3.select(this)
                  .style("stroke", "black")
                  .style("opacity", 1)
              }
              var portionToIntegerValue = function (higherValue, portion) {
                return  Math.floor( (portion/ 100) * parseInt(higherValue) );
              }
              var mousemove = function(d) {
                tooltip
                  .html("Cantidad de visitas al nodo \"" + translateObject[d.group] + 
                    "\" en la simulación: \"" + improveSyntax(translateObject[d.variable]) + "\": "
                    + portionToIntegerValue(higherValue, d.value)
                  )
                  .style("left", (d3.mouse(this)[0]+70) + "px")
                  .style("top", (d3.mouse(this)[1]) + "px")
                  .style("text-align", "center")
              }
              var mouseleave = function(d) {
                tooltip
                  .style("opacity", 0)
                d3.select(this)
                  .style("stroke", "none")
                  .style("opacity", 0.8)
              }
            
              // add the squares
              svg.selectAll()
                .data(data, function(d) {return d.group+':'+d.variable;})
                .enter()
                .append("rect")
                  .attr("x", function(d) { return x(d.group) })
                  .attr("y", function(d) { return y(d.variable) })
                  .attr("rx", 4)
                  .attr("ry", 4)
                  .attr("width", '28px' )
                  .attr("height", '25px' )
                  .style("fill", function(d) { return myColor(d.value)} )
                  .style("stroke-width", 4)
                  .style("stroke", "none")
                  .style("opacity", 0.8)
                .on("mouseover", mouseover)
                .on("mousemove", mousemove)
                .on("mouseleave", mouseleave)
      
            });
      
        }).catch((response) => {
          console.log('Error at D3 Heat map wrapper.');
          console.log(response);
        });
  
    })
    .catch((response) => {
      console.log("Error fetching the highest visited value inside the Archimate concepts.");
      console.log(response);
    });

}

// exposeHeatMapRender();
