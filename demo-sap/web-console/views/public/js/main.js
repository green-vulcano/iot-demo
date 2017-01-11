
window.onload = function(){

	var socket = io();
   	var client = undefined;
   	var mqtt_connected = false;

   	var statusHole = false;
   	var statusTree = false;
   	var statusTunnel = false;
   	var statusSignal = false;

	/******************************************************
     *
     ******************************************************/
    socket.on('btn1', function(value) {
		console.log("button1 detected: " + value);
	});

    // albero
	socket.on('btn2', function(value) {
		console.log("button2 tree: " + value);
		statusTree = value;
	});

	// segnale
	socket.on('btn3', function(value) {
		console.log("button3 signal: " + value);
		statusSignal = (value === 'true');
	});

	// tombino
	socket.on('btn4', function(value) {
		console.log("button4 hole: " + value);
		statusHole = (value === 'true');
	});

	// galleria
	socket.on('btn5', function(value) {
		console.log("button5 tunnel: " + value);
		statusTunnel = (value === 'true');
	});

	// albero
	socket.on('prx1', function(value) {
		console.log("proximity tree detected");
		if(!statusTree) {
			console.log("danger tree");
			triggerDanger("tree");
		}
	});

	// segnale
	socket.on('prx2', function(value) {
		console.log("proximity signal detected");
		if(!statusSignal) {
			console.log("danger signal");
			triggerDanger("sign");
		}
	});

	// fumo
	socket.on('prx3', function(value) {
		console.log("proximity smoke detected");
		if(statusSmoke) {
			console.log("danger smoke");
			triggerDanger("smoke");
		}		
	});

	// tombino
	socket.on('prx4', function(value) {
		console.log("proximity hole detected");
		if(!statusHole) {
			console.log("danger hole");
			triggerDanger("hole");
		}
	});

	// galleria
	socket.on('prx5', function(value) {
		console.log("proximity5 tunnel detected");
		if(!statusTunnel) {
			console.log("danger tunnel");
			triggerDanger("tunnel");
		}
	});

//Global variables
	var s = Snap("#map_wrap"),
		animation,
		animateAlongPath,
		car,
		movePoint, //car position
		carMove = true, //boolean for start and stop
		dataInterval, //need to stop random data interval
		first = true; //boolean to see if first car run
/***** 
 * Buttons for development -- comment before production (see HTML too) - start
 *****/
	$( "#holeBt" ).unbind('click').click(function(evt) {
		triggerDanger("hole");
	});
	$( "#treeBt" ).click(function() {
		triggerDanger("tree");
	});
	$( "#tunnelBt" ).unbind('click').click(function(evt) {
		triggerDanger("tunnel");
	});
	$( "#signBt" ).unbind('click').click(function(evt) {
		triggerDanger("sign");
	});
	$( "#getPtBt" ).unbind('click').click(function(evt) {
		console.log(movePoint);
	});
	$( "#StopTrip" ).click(function() {
		endAll();
	});
	$( "#StartTrip" ).unbind('click').click(function(evt) {
		carMove = true;
		startAll();
	});
/***** 
 * Buttons for development -- comment before production (see HTML too) - end
 *****/
	
	
/***** 
 * Main functions for start and stop - start
 *****/

	function startAll(){
		$("#rest_time_wrap").fadeOut(1000);
		//start car
		animation();
		
		// Set new random value every 10 seconds and store old data in table.
		dataInterval = setInterval(randomValue, 10000);
	}
	
	function endAll(){
		//reset car animation
		carMove = false;
		first = true;
		
		//move car to base
		car.transform('t0,0');
		
		//stop random data
		clearInterval(dataInterval);
		dataInterval = null;
		
		//clear tables
		$("#danger_data_table > tbody").html("");
		$("#historical_data_table > tbody").html("");
		
		$("#rest_time_wrap").fadeIn(1500);
	}
/***** 
 * Main functions for start and stop - end
 *****/
	
	
/***** 
 * Functions for dangers. call this when danger is triggered. see development buttons -start
 *****/
	
	//generic function for display.
	function triggerDanger(typeOfDanger){
		// Array data for generic objects [icon, description]
		var data;
		
		switch(typeOfDanger){
			case "hole":
		        data = ["Hole detected in the street"];
		        break;
		    case "tree":
		    	data = ["Tree falling in the street"];
		        break;
		    case "tunnel":
		    	data = ["Low lights detected on the street, also low gps signal"];
		        break;
		    case "sign":
		    	data = ["Traffic sign falling"];
		        break;
		    case "smoke":
		    	data = ["Smoke detected"];
		        break;
		    default:
		        break;
		}
		
		//draw circle on map
		dangerCircle();
		
		//get now moment in format "gg/mm/aaaa hh:mm:ss"
		var today = new Date(),
			now = today.getDate()+"/"+today.getMonth()+1+"/"+today.getFullYear()+" "+today.getHours()+":"+today.getMinutes()+":"+today.getSeconds();
		
		//div for danger table
		var tableDiv = 
			'<tr>'+
				'<td class="col-lg-1"><img src="../assets/'+typeOfDanger+'.svg"></td>'+
		        '<td  class="col-lg-2">'+now+'</td>'+
		        '<td  class="col-lg-4">'+movePoint.x+', '+movePoint.y+'</td>'+
		        '<td  class="col-lg-5">'+data[0]+'</td>'+
	        '</tr>';
		
		//div for danger section
		var dangerDiv = 
			'<img src="../assets/screen_event_'+typeOfDanger+'.png">'+
			'<div class="col-lg-1 data_wrap icon_wrap">'+
				'<img src="../assets/'+typeOfDanger+'.svg">'+
				'<small>Type</small>'+
			'</div>'+
			'<div class="col-lg-2 data_wrap">'+
				'<strong>'+now+'</strong>'+
				'<small>Time</small>'+
			'</div>'+
			'<div class="col-lg-4 data_wrap">'+
				'<strong>'+movePoint.x+', '+movePoint.y+'</strong>'+
				'<small>GPS</small>'+
			'</div>'+
			'<div class="col-lg-5 data_wrap">'+
				'<strong>'+data[0]+'</strong>'+
				'<small>Description</small>'+
			'</div>';
		
		// Populate & show danger section 
		$("#danger_data_wrap .panel-body").html(dangerDiv);
		$("#danger_data_wrap").show();
		$("#noDanger_data_wrap").hide();
		
		//Hide danger section after 15 seconds. Change accordingly to the speed of demo
		//it should be less then the movement of the car from one danger to the other
		setTimeout(function(){
			$("#noDanger_data_wrap").show();
			$("#danger_data_wrap").hide();
		}, 15000);
		
		// Populate table with data
		$("#danger_data_table > tbody").prepend(tableDiv);
		
	};
	
/***** 
 * Functions for dangers. call this when danger is triggered. see development buttons -end
 *****/
	
	
/***** 
 * Map & car animation -start
 *****/
	Snap.load("../assets/map2.svg", function(SVG) {
	//variables for map, car, route && events
		var map = SVG.select("#mapBKGRD"),
	    	carRoute = SVG.select("#carRoute");
			car = SVG.select("#car");
		animation = function () {
				car.transform('t0,0');
				// Animation set to 600.000 milliseconds =  10 minute
				animateAlongPath(carRoute, car, 0, 600000, mina.linear);
			};
			
	    s.append(SVG);
	});


//SNIPPET FOR ANIMATE ALONG PATH
	animateAlongPath = function (path, el, start, duration, easing) {
		  var len = Snap.path.getTotalLength(path), 
		      elBB =  el.getBBox(),
		      elCenter = {
		        x: elBB.x + (elBB.width / 2),
		        y: elBB.y + (elBB.height / 2),
		      };
		  
		  el.current_anim = Snap.animate(start, len, function (value) {
			  // Boolean to stop car middle run. No start and stop, just restart.
			  if(carMove){
		    	  movePoint = Snap.path.getPointAtLength(path, value);
		    	  el.transform('t'+ (movePoint.x - elCenter.x) + ',' + (movePoint.y - elCenter.y));
		      }
		    }, duration, easing);
	};
/***** 
 * Map & car animation -end
 *****/
	
	
/***** 
 * Function for pulsating circle -start
 *****/	
	function dangerCircle(){
		var paper = Snap("#mapBKGRD"),
			//create circles of color #961E24, size 7
			centerCircle = paper.circle(movePoint.x, movePoint.y, 7).attr({fill: "#961E24", opacity: "0.8"}),
			c1 = paper.circle(movePoint.x, movePoint.y, 7).attr({fill: "#961E24", opacity: "0.2"}),
			c2 = paper.circle(movePoint.x, movePoint.y, 7).attr({fill: "#961E24", opacity: "0.2"}),
			c3 = paper.circle(movePoint.x, movePoint.y, 7).attr({fill: "#961E24", opacity: "0.2"});
		
		//Load circles in svg part
		paper.append(centerCircle);
		paper.append(c1);
		paper.append(c2);
		paper.append(c3);
		
		var circleAnimation = function () {
			//start animation async for wave style
		    cAnim(c1);
		    setTimeout(function () {
		      cAnim(c2);
		    }, 1200);
		    setTimeout(function () {
		        cAnim(c3);
		    }, 2400);

		    function cAnim(el){
		      el.stop().animate(
		        { opacity: 0, transform: 's3 center center'},
		        3600,
		        function(){
		          el.attr({ opacity: 1, transform: 'scale(1)'});
		          cAnim(el);
		        });
		      }
		    }
		
		circleAnimation();
		
		// Dismiss circles after 15 seconds and remove them from DOM
		setTimeout(function(){
			c1.stop(); c2.stop(); c3.stop(); 
			centerCircle.remove(); c1.remove(); c2.remove(); c3.remove();
		}, 15000);
	}
/***** 
 * Function for pulsating circle -end
 *****/	

	
/***** 
 * Function for random value -start
 *****/	
	function randomValue(){
		//get now moment in format "gg/mm/aaaa hh:mm:ss"
		var today = new Date(),
			now = today.getDate()+"/"+today.getMonth()+1+"/"+today.getFullYear()+" "+today.getHours()+":"+today.getMinutes()+":"+today.getSeconds();
		
		if(!first){
		//prepare values for storage in a table
		var tableDiv = '<tr>'+
	        '<td>'+$("#data_time").text()+'</td>'+
	        '<td>'+$("#temp_wrap > strong").text()+'</td>'+
	        '<td>'+$("#CO2_wrap > strong").text()+'</td>'+
	        '<td>'+$("#light_wrap > strong").text()+'</td>'+
	        '<td>'+$("#noise_wrap > strong").text()+'</td>'+
	    '</tr>';
		}
		
		// Populate table with data
		$("#historical_data_table > tbody").prepend(tableDiv);
		
		// Set new random data in "Data for: " section
		$("#data_time").text(now);
		$("#temp_wrap > strong").text(Math.floor(Math.random() * 6) + 10);
		$("#CO2_wrap > strong").text(Math.floor(Math.random() * 11) + 30);
		$("#light_wrap > strong").text(Math.floor(Math.random() * 80001) + 20000);
		$("#noise_wrap > strong").text(Math.floor(Math.random() * 11) + 41);
		
		first = false;
	}
	/***** 
	 * Function for random value -end
	 *****/	
}; //end graph for window.onload