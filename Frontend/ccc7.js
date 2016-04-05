/*
	ccc7.html

	(for opened in fypGit)
	
	data generation:  genGC.py
	Time series (TS) length: 30
	Interval between TS: 5
	Format: comma separated, not csv, by year

	
	include all coe data

    data source: temp
    range: 2003 - 2012

    All data are preloaded into lists in JS to speed up reading time.
    * including coefficients (strength)		22/2/16

*/

var show_rec_i = 0
var dateList = []	// store available TC dates for this year
var oldYear = yearBegin
var oldStation = null

var allFromTo = [];
var allToFrom = [];
var yearBegin = 2003
var nYear = 1
var yearEnd = yearBegin+nYear-1;
var lagsChecked = [true,true,true,true,true,true];
var rawData;
var chinaStation = [50136099999,50434099999,50564099999,50888099999,51431099999,51463099999,51709099999,
				    51811099999,51828099999,51886099999,52203099999,52418099999,52436099999,52495099999,
				    52602099999,52737099999,52787099999,52818099999,52836099999,53083099999,53336099999,
				    53352099999,53391099999,53564099999,53646099999,53705099999,53787099999,53923099999,
				    53959099999,54012099999,54026099999,54259099999,54273099999,54292099999,54337099999,
				    54377099999,54511099999,54808099999,54823099999,54843099999,54863099999,55228099999,
				    55279099999,55578099999,55696099999,56004099999,56065099999,56106099999,56167099999,
				    56247099999,56444099999,56492099999,56748099999,56954099999,56985099999,57328099999,
				    57476099999,57598099999,57745099999,57816099999,58221099999,58345099999,58367099999,
				    58633099999,58754099999,58968099999,59007099999,59117099999,59134099999,59278099999,
				    59316099999,59358099999,59431099999,59456099999,59493099999,59845099999]

// initialize data array
function Initialize()
{
	for (var y = yearBegin; y <= yearEnd; ++y)
	{
		allFromTo[y] = {};
		allToFrom[y] = {};
		/*
		for (var m = 1; m <= 12; ++m)
		{
			allFromTo[y][m] = [];
			allToFrom[y][m] = [];
			for (var i = 0; i < 76; ++i)
			{
				allFromTo[y][m][chinaStation[i]] = {};
				allToFrom[y][m][chinaStation[i]] = {};
			}
		}
		*/
	}
}
Initialize();

var body_w = 1500, body_h = 1500, positions = [], objmp={};
var projection = d3.geo.azimuthal()
					   .mode("equidistant")
					   .origin([107, 31])
					   .scale(1350)
					   .translate([640, 570]);
var path = d3.geo.path().projection(projection);
var svg = d3.select("body")
            .insert("svg:svg", "body")
            .attr("width", body_w)
            .attr("height", body_h);
var states = svg.append("svg:g").attr("id", "states");
var circles = svg.append("svg:g").attr("id", "circles");
var cells = svg.append("svg:g").attr("id", "cells");

// show voronoi
/*d3.select("input[type=checkbox]").on("change", function() {
        cells.classed("voronoi", this.checked);
});*/

d3.json("china.json", function (collection) {
        states.selectAll("path")
                  .data(collection.features)
                  .enter()
                  .append("svg:path")
                  .attr("d", path);
});

d3.csv("stationData.csv", function (datas)
{
	datas = datas.filter(function (station) {
		if (chinaStation.indexOf(parseInt(station.id)) > -1)
		{
			$("#selectSrc").append($("<option></option>").attr("value", station.id)
														 .text(station.name));
			$("#selectDst").append($("<option></option>").attr("value", station.id)
														 .text(station.name));
			var location = [+station.long, +station.lat];
			positions.push(projection(location));
			objmp[station.id] = {};
			objmp[station.id]["name"] = station.name;
			objmp[station.id]["org"] = location;
			objmp[station.id]["pos"] = projection(location);
			return true;
		}
	});
	console.log("totalsz:" + positions.length);
	console.log(objmp);//0:long,1:lat
	// Compute the Voronoi diagram of datas' projected positions.
	var polygons = d3.geom.voronoi(positions);
	var g = cells.selectAll("g")
							 .data(datas)
							 .enter()
							 .append("svg:g");
	g.append("svg:path")
	 .attr("class", "cell")
	 .attr("d", function(d, i) { return "M" + polygons[i].join("L") + "Z"; })
	 .on("mouseover", function(d, i) { d3.select("#stationNow")
																			 .text(d.name); });
	circles.selectAll("circle")
		   .data(datas)
		   .enter()
		   .append("svg:circle")
		   .attr("cx", function(d, i) { return positions[i][0]; })
		   .attr("cy", function(d, i) { return positions[i][1]; })
		   .attr("r", 3)
});

svg.append("svg:defs")
   .append("svg:marker")
   .attr("id", "arrow")
   .attr("viewBox", "0 0 10 10")
   .attr("refX", 27)
   .attr("refY", 5)
   .attr("markerUnits", "strokeWidth")
   .attr("markerWidth", 8)
   .attr("markerHeight", 6)
   .attr("orient", "auto")
   .append("svg:path")
   .attr("d", "M 0 0 L 10 5 L 0 10 z");

function upd()
{
	show_rec_i = parseInt($('#mmdd').val());
	if (isNaN(show_rec_i))
		show_rec_i = 0;
	//console.log(show_rec_i);
	var yy = $('#yearSelect').val();
	var mm = dateList[show_rec_i][0];
	var dd = dateList[show_rec_i][1];
	// all station
	if ($('#allDirections').prop('checked'))
	{
		// remove old svg elements
		cleanSVG();
		for (i in chinaStation){
			var key = chinaStation[i]
			loadData(yy, mm, dd, key)
		}
	}
	// one station
	else
	{
	    var key = $("#selectSrc").val().substring(0,6) + $("#selectSrc").val().substring(6);
		// remove old svg elements
		cleanSVG();
	    loadData(yy, mm, dd, key);
	}
}

function upd3(change)
{
	show_rec_i += change;
	var yy = parseInt($('#yearSelect').val());
	var key = $("#selectSrc").val().substring(0,6) + $("#selectSrc").val().substring(6);
	if (yy != oldYear || oldStation != key)
	{
		dateList = []
		// update dateList
		for (mmdd in allFromTo[yy])
		{
			L1 = Object.keys(allFromTo[yy][mmdd][key]).length;
			L2 = Object.keys(allToFrom[yy][mmdd][key]).length;
			if (L1 > 0 || L2 > 0)
				dateList.push(mmdd.split('-'));
		}
		dateList.sort(function(a,b){
			var a1 = parseInt(a[0]);
			var b1 = parseInt(b[0]);
			var a2 = parseInt(a[1]);
			var b2 = parseInt(b[1]);
			if (a1 == b1)
				return a2 - b2;
			else 
				return a1 - b1;
		});
		oldYear = yy;
		oldStation = key;
		// update dateDiv content
		var dateDiv_content = '<select id="mmdd" onchange="upd()">'
		for (i in dateList)
		{
			var mmdd = dateList[i][0]+'-'+dateList[i][1];
			dateDiv_content += '<option value="'+i+'">'+mmdd+'</option>';
		}
		dateDiv_content += '</select>'
		$('#dateDiv').html(dateDiv_content);
		$('#mmdd').val(0);
	}
	show_rec_i = Math.min(Math.max(0, show_rec_i), dateList.length-1);
	// change "select" option
	$('#mmdd').val(show_rec_i);
	upd();
}

var this_year;
var storedData;
var lagRange = 5;

function ImportData()
{

	console.log('Importing data...');
	console.log(yearBegin,'-',yearEnd);
	// years
	var folder = 'data/continuous_light_d30_i5_2003_2012/'
	for (var i = yearBegin; i <= yearEnd; i++)
	{

		var filePath = folder + i + '.txt';
		d3.text(filePath, function(text){
			tmp_data = d3.csv.parseRows(text);
			if (tmp_data != null)
			{
				year = tmp_data[0][2].split('-')[0]
				console.log('Year:',year,', Data Length:', tmp_data.length);
				tmp_data.forEach( function(rec){
					//console.log(rec)
					var srcID = rec[0].substring(0,6) + rec[0].substring(7,12);
					var dstID = rec[1].substring(0,6) + rec[1].substring(7,12);
					var date = rec[2].split('-');
					var yy = parseInt(date[0]);
					var mm = date[1];
					var dd = date[2];
					var mmdd = mm + '-' + dd;

					try
					{
						allFromTo[yy][mmdd][srcID][dstID] = [];
						allToFrom[yy][mmdd][dstID][srcID] = [];
					}
					catch(err)
					{
						allFromTo[yy][mmdd] = [];
						allToFrom[yy][mmdd] = [];
						for (var j = 0; j < chinaStation.length; j++)
						{
							allFromTo[yy][mmdd][chinaStation[j]] = {};
							allToFrom[yy][mmdd][chinaStation[j]] = {};
						}
						allFromTo[yy][mmdd][srcID][dstID] = [];
						allToFrom[yy][mmdd][dstID][srcID] = [];
					}

					for (var j = 1; j <= lagRange; j++)
					{
						p = rec[2+j];
						coe = rec[7+j];
						allFromTo[yy][mmdd][srcID][dstID][j] = {'p': p, 'coe': coe};
						allToFrom[yy][mmdd][dstID][srcID][j] = {'p': p, 'coe': coe};
					}
				});
			}
		});
	}
}

function draw(fromto, srcID, dstID, stationP, theLags, yy, mm, dd)
{
	theLags = theLags.split('');
	//console.log(theLags);
	var srck = srcID;
	var dstk = dstID;
	var s0 = objmp[srck]["pos"][0];
	var s1 = objmp[srck]["pos"][1];
	var d0 = objmp[dstk]["pos"][0];
	var d1 = objmp[dstk]["pos"][1];
	var lineWidth;

	// check if bidirectional
	var p1 = [s0, s1].join();
	var p2 = [d0, d1].join();
	var p1_org = [objmp[srck]["org"][0], objmp[srck]["org"][1]];	// [longtitude, latitude]
	var p2_org = [objmp[dstk]["org"][0], objmp[dstk]["org"][1]];
	var bidirectional = false;
	for (var i = 0; i < lineData.length; i++){
		if ( p1==lineData[i].p1.join() && p2==lineData[i].p1.join()) {
			//var single_line = [[s0, s1], [d0, d1], p1_org, p2_org]
			bidirectional = true;
			//lineData.push(single_line);
			console.log('what?! same GC appear twice?!');
		}
		if (p2==lineData[i].p1.join() && p1==lineData[i].p2.join()) {
			//var single_line = [[d0, d1], [s0, s1], p2_org, p1_org]
			bidirectional = true;
			lineData[i].fromto = 2;
			//lineData.push([p2_org, p1_org]);
		}
	}
	if (!bidirectional)
	{
		var single_line = {}
		if (fromto)
		{
			single_line.p1 = [s0, s1]
			single_line.p2 = [d0, d1]
			single_line.p1_org = p1_org
			single_line.p2_org = p2_org
			single_line.fromto = 1
		}
		else
		{
			single_line.p1 = [d0, d1]
			single_line.p2 = [s0, s1]
			single_line.p1_org = p2_org
			single_line.p2_org = p1_org
			single_line.fromto = 0
		}
		lineData.push(single_line)
	}
	/*
	if (stationP < 0.001)
		lineWidth = 6;
	else if (stationP < 0.01)
		lineWidth = 3;
	else
		lineWidth = 1;
	*/
	if (!$('#allGCLines').prop('checked')){
		return
	}
	lineWidth = 1;
	
	//console.log(objmp[srck]["name"] + "(" + srck + ") -> " + objmp[dstk]["name"] + '(' + dstk + ')');
	//var mapdist = (objmp[srck]["pos"][0]-objmp[dstk]["pos"][0])*(objmp[srck]["pos"][0]-objmp[dstk]["pos"][0])+(objmp[srck]["pos"][1]-objmp[dstk]["pos"][1])*(objmp[srck]["pos"][1]-objmp[dstk]["pos"][1]);
	var mapdist = Math.pow((s0-d0),2) + Math.pow((s1-d1),2);
	var color;
	if (fromto)     color = "red";
	else            color = "green";
	if (bidirectional) color = "yellow";
	//1. draw line
	DrawLine( s0, s1, d0, d1, lineWidth, color )

	// 2. draw valid lags box
	var rectHeight = 22;
	var rectWidth = 5 + 18*theLags.length;
	var middleX = (s0+d0)/2;
	var middleY = (s1+d1)/2;
	var infoX;
	var infoY;
	if (fromto)	{
		infoX = (d0 + middleX) / 2;
		infoY = (d1 + middleY) / 2;
	}
	else {
		infoX = (s0 + middleX) / 2;
		infoY = (s1 + middleY) / 2;
	}
	
	var rectX = infoX - rectWidth/2;
	var rectY = infoY - rectHeight/2;
	DrawLagBox ( infoX, infoY, rectHeight, rectWidth, theLags )

	// 3. draw strength bar
	// take the lag variables coefficient
	// e.g. 5 lags, 5 coefficients
	var colors = ['red','blue','yellow','green','orange'];
	var barLength = 70;
	var subBarLength = barLength/lagRange;
	var barY = rectY + rectHeight + 3;
	var barX = infoX - barLength/2;
	var barSpace = 4;	// space between bars
	var barMax = 1;		// max coe value of a sub-bar
	for (var i in theLags)
	{
		var lag = theLags[i];	// 1-5
		var mmdd = mm + '-' + dd;
		var coes = allFromTo[yy][mmdd][srcID][dstID][lag]['coe'].split(' ');
		coes = coes.slice(lag, 2*lag);	// take lag coes
		//console.log(coes);
		var bar_y1 = barY + i*barSpace;
		var bar_y2 = bar_y1;
		var bar = svg.append('line')
					 .style('stroke', 'white')
					 .attr('x1', barX)
					 .attr('x2', barX + barLength)
					 .attr('y1', bar_y1)
					 .attr('y2', bar_y2)
					 .attr("stroke-width", barSpace);
		for (var j in coes)
		{
			coes[j] = parseFloat(coes[j]);
			//console.log(coes[j]);
			// draw short sub-bar
			var bar_x1 = barX + j*subBarLength;
			var bar_x2 = barX + j*subBarLength + Math.min((Math.abs(coes[j])/barMax),barMax)*subBarLength;
			//console.log('coes[j]:',coes[j]);
			//console.log('abs(coes[j]) / barMax:',Math.abs(coes[j])/barMax);
			//console.log('(',bar_x1,',',bar_y1,') , (',bar_x2,',',bar_y2);
			var bar = svg.append('line')
						 .style('stroke', colors[j])
						 .attr('x1', bar_x1)
						 .attr('x2', bar_x2)
						 .attr('y1', bar_y1)
						 .attr('y2', bar_y2)
						 .attr("stroke-width", 3);
		}
	}
}

function DrawLine( x1, y1, x2, y2, lineWidth, color ){
	var line = svg.append("line")
				  .style("stroke", color)
				  .attr("x1", x1)
				  .attr("y1", y1)
				  .attr("x2", x2)
				  .attr("y2", y2)
				  .attr("marker-end", "url(\#arrow)")
				  .attr("stroke-width", lineWidth)
	//			  .attr("title", stationP)
}

function DrawLagBox ( infoX, infoY, rectHeight, rectWidth, theLags ){
	var x = infoX - rectWidth/2;
	var y = infoY - rectHeight/2;
	var rect = svg.append("rect")
					.attr('x',x)
					.attr('y',y)
					.attr('width',rectWidth)
					.attr('height',rectHeight)
					.attr('stroke','black')
					.attr('stroke-width','3')
					.attr('fill','white');
	
	var lagtext = svg.append('text')
					 .attr('x', infoX - 7*theLags.length)
					 .attr('y', infoY + 5)
					 .attr('fill', 'orange')
					 .attr('font-size', 20)
					 .text(theLags.join());
}

function cleanSVG(){
	$("svg line").remove();
	$("svg text").remove();
	$("svg rect").remove();
}

var lineData = []
var outGCsStrength = []
var inGCsStrength = []
var checkList = []
var outDirs = []
var inDirs = []

var maxAngle = 30	// max angle between two consecutive GCs in an arrow group
var minArrowGC = 4	// min no. of GC to form an arrow
function loadData(yy,mm,dd,tg)
{
	//console.log("Load some data...");
	//console.log(tg)
	var str = tg;
	//alert(str);
	$("#selectSrc").val(str);

	// year out of range
	if (yy < yearBegin || yy > yearEnd)
	{
		alert("Data not exist. Range limit: 2003-2012");
		return;
	}
	var limDistCount = 0;
	var degOut = 0, degIn = 0;

	// draw
	// all edges from the station
	mmdd = mm + '-' + dd;

	lineData = []
	drawAll(allFromTo, true);
	drawAll(allToFrom, false);
	// draw lines
	function drawAll(data, fromto)
	{
		for (var stationID in data[yy][mmdd][tg])
		{
			var srcID;
			var dstID;
			if (fromto) {
				srcID = tg;
				dstID = stationID;
			}
			else {
				srcID = stationID;
				dstID = tg;
			}
			// take the min stationP
			var hasValidP = false;
			var minP = 1;
			var lags = '';
			var stationP;
			for (var i = 1; i <= lagRange; i++)
			{
				stationP = data[yy][mmdd][tg][stationID][i]['p'];
				//if ($('#selectLag'+i).attr( "checked" ) && stationP < 0.05)
				if (stationP < 0.05 && lagsChecked[i])
				{
					lags += i;
					hasValidP = true;
				}
			}
			if (hasValidP)
			{
				draw(fromto, srcID, dstID, stationP, lags, yy, mm, dd);
				if (fromto)
					degOut++
				else
					degIn++
			}
		}
	}
	//console.log('degIn:', degIn);
	//console.log('degOut:', degOut);
	// draw GC general directions arrow
	//
	// 1. calculate angles for each line
	// 2. sort by angle
	// 3. pick general GC directions (GCs consecutive in angle)
	//
	var total = lineData.length
	//console.log(total)
	for (i in lineData)
	{
		var lng1 = toRadian(parseFloat(lineData[i].p1_org[0]))
		var lat1 = toRadian(parseFloat(lineData[i].p1_org[1]))
		var lng2 = toRadian(parseFloat(lineData[i].p2_org[0]))
		var lat2 = toRadian(parseFloat(lineData[i].p2_org[1]))
		var dir = bearing(lat1, lng1, lat2, lng2)
		//console.log(lineData[i])
		lineData[i].dir = dir
		//var what0 = [parseFloat(lineData[i].p1[0]),parseFloat(lineData[i].p1[1])]
		//var what = [lat1,lng1,lat2,lng2,dir]
		//console.log(what.join())
	}
	// sort by dir (angle)
	var sorted_lineData = lineData.sort(function(a,b){ return a.dir - b.dir })
	// count max continuous GC in same direction 
	var theMax = 0	// count out
	var theMin = 0
	checkList = []	// double sorted_lineData
	/*for (var i in sorted_lineData)
	{
		var datum = {}
		datum.dir = sorted_lineData[i].dir
		datum.fromto = sorted_lineData[i].fromto
		checkList.push(datum)
	}*/
	checkList = sorted_lineData
	checkList.push.apply(checkList, checkList)	// extend itself

	outGCsStrength = []
	inGCsStrength = []
	// generate sequence for counting arrow
	for (var i in checkList)
	{
		if (checkList[i].fromto == 1){
			if (i == 0)
			{
				outGCsStrength[i%total] = 1
				inGCsStrength[i%total] = 0
			}
			else {
				// avoid too wide spread GCs
				var isFirstGC = (outGCsStrength[(i-1)%total] == 0)
				if (!isFirstGC && !isSmallAngle(checkList[i-1].dir, checkList[i].dir, maxAngle))
					outGCsStrength[i%total] = 0
				else
					outGCsStrength[i%total] = outGCsStrength[(i-1)%total] + 1
				inGCsStrength[i%total] = 0
			}
		}
		else if (checkList[i].fromto == 0)
		{
			if (i == 0)
			{
				outGCsStrength[i%total] = 0
				inGCsStrength[i%total] = 1
			}
			else
			{
				// avoid too wide spread GCs
				var isFirstGC = (inGCsStrength[(i-1)%total] == 0)
				if (!isFirstGC && !isSmallAngle(checkList[i-1].dir, checkList[i].dir, maxAngle))
					inGCsStrength[i%total] = 0
				else
					inGCsStrength[i%total] = inGCsStrength[(i-1)%total] + 1
				outGCsStrength[i%total] = 0
			}
		}
		else{
			outGCsStrength[i%total] = 0
			inGCsStrength[i%total] = 0
		}
	}
	//console.log(outGCsStrength)
	//console.log(inGCsStrength)
	// find avg. angle for GCsStrength > 3
	// (take avg. angle)
	outDirs = findGeneralDirections( outGCsStrength, minArrowGC, true )
	inDirs = findGeneralDirections( inGCsStrength, minArrowGC, false )

	function findGeneralDirections ( strList, minCount, fromto )
	{
		var result = []
		for (var i in strList){
			if (strList[i] == 0){
				var count = strList[(i-1+total)%total]
				var first_angle = lineData[(i-count+total)%total].dir
				if (count >= minCount){
					var angleSum = 0
					var tmp_angle_list = []
					for (var j = 1; j < count; j++){
						var tmp_angle = lineData[(i-count+j+total)%total].dir
						tmp_angle_list.push(tmp_angle)
						var relative_angle = (tmp_angle + 360 - first_angle)%360
						//console.log(relative_angle)
						//angleSum += lineData[(i-1-j+total)%total].dir
						angleSum += relative_angle
						//console.log(lineData[(i-1-j+total)%total].dir)
					}
					//console.log(tmp_angle_list)
					var angleAvg = (angleSum/count + first_angle)%360
					//console.log('avg. angle:',angleAvg)
					var datum = {}
					datum.dir = angleAvg
					datum.str = count
					datum.fromto = fromto
					result.push(datum)
				}
			}
		}
		return result
	}
	drawArrows()
}

function isSmallAngle(a1, a2, threshold){
	var diff = Math.abs(a1-a2)
	if (diff > threshold && 360-diff > threshold)
		return false
	else{
		return true
	}
}
var centerStation;
function drawArrows()
{
	// draw arrows !
	var margin = 50
	var defs = svg.append("defs")
	var x1					// center x
	var y1					// center y
	var arrowLength = 70			// arrow length


	// find center first
	centerStation = []	// hold [x,y]
	for (var i in lineData){
		/*
		if (lineData[i].fromto == 1){
			centerStation = lineData[i].p1
			console.log(lineData[i])
			break
		}
		else if (lineData[i].fromto == 0){
			centerStation = lineData[i].p1
			break
		}*/
		centerStation = lineData[i].p1
	}
	x1 = centerStation[0]	// center x
	y1 = centerStation[1]	// center y

	defs.append("marker")
			.attr({
				"id":"arrow",
				"viewBox":"0 -5 10 10",
				"refX":5,
				"refY":0,
				"markerWidth":4,
				"markerHeight":4,
				"orient":"auto"
			})
		.append("path")
			.attr("d", "M0,-5L10,0L0,5")
			.attr("class","arrowHead");

	// draw line plus arrow head
	//console.log('center:',x1,',',y1)
	
	//console.log('outDirs:',outDirs)
	//console.log('inDirs:',inDirs)
	drawSomeArrows(outDirs, 'red')
	drawSomeArrows(inDirs, 'green')

	function drawSomeArrows(data, color){
		for (var i in data){
			var angle = toRadian(data[i].dir)
			DrawArrow( x1, y1, angle, arrowLength, color, 0 )
		}
	}
}

function DrawArrow( x, y, angle, arrowLength, color, strength ){
	var x2 = x - arrowLength*(Math.sin(angle))
	var y2 = y - arrowLength*(Math.cos(angle))
	svg.append('line')
	  	.style("stroke", color)
		.attr({
			"class":"arrow",
			"marker-end":"url(#arrow)",
			"x1": x,
			"y1": y,
			"x2": x2,
			"y2": y2
		});
}

function bearing(lat1, lng1, lat2, lng2)
{
	var dLon = (lng2-lng1);
    var y = Math.sin(dLon) * Math.cos(lat2);
    var x = Math.cos(lat1)*Math.sin(lat2) - Math.sin(lat1)*Math.cos(lat2)*Math.cos(dLon);
    var brng = toDeg(Math.atan2(y, x));
    return 360 - ((brng + 360) % 360);
}

function toRadian(deg)
{
	return deg * Math.PI / 180;
}
function toDeg(radian)
{
	return radian * 180 / Math.PI;
}

$(document).ready(function(){


	// year options div
	$('#yearDiv').html(function(){
		var str;
		str += "<select id='yearSelect'>";
		for (var i = yearBegin; i <= yearEnd; i++)
		{
			str += "<option value='" + i + "'>" + i + "</option>";
		}
		str += "</select>";
		return str;
	});

	ImportData();
	$('#yearSelect').val(yearBegin);

	// checked?
	$( ":checkbox" ).change(function(){
		var checkedLag = $(this).val();
		if ($(this).prop('checked')){
			lagsChecked[checkedLag] = true;
			console.log('lag',$(this).val(),'checked.');
		}
		else{
			lagsChecked[checkedLag] = false;
			console.log('lag',$(this).val(),'un-checked.');
		}
		upd();
	});

	$("#selectSrc").change(upd());
});
