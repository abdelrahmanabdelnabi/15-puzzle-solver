/**
 * 15-puzzle.js
 *
 * Copyright (c) 2015 Arnis Ritins
 * Released under the MIT license
 */
(function(){
	var currentStep = 0;
	var steps = [];

	var rows = 3;
	var cols = 3;

	var state = 1;
	var puzzle = document.getElementById('puzzle');
	puzzle.className = 'animate';
	// Creates solved puzzle
	initGame();

	var blankCell = getEmptyCell();

	// Listens for click on puzzle cells
	puzzle.addEventListener('click', function(e){
		if(state == 1){
			// Enables sliding animation
			puzzle.className = 'animate';
			shiftCell(e.target);
		}
	});

	// Listens for click on control buttons
	document.getElementById('solve').addEventListener('click', solve);
	document.getElementById('scramble').addEventListener('click', scramble);
	document.getElementById('enter').addEventListener('click', generate);

	/**
	 * Creates solved puzzle
	 *
	 */
	function solve(){

		p = document.getElementById('puzzle');

		if(!p.className.includes('animate'))
			p.className += 'animate';

		var sequence = []

		for(var i = 0; i < rows; i++) {
			for(var j = 0; j < cols; j++) {
				var cell = getCell(i, j);
				var num = cell.innerHTML == '' ? 0 : parseInt(cell.innerHTML)
				sequence.push(num)
			}
		}
		console.log(sequence)

		select = document.getElementsByName('search strategy')[0]

		const xmlHttp = new XMLHttpRequest();
		const url='http://localhost:5000/solve';
		xmlHttp.open("POST", url);
		xmlHttp.setRequestHeader("Content-Type", "application/json");
		xmlHttp.send(JSON.stringify(
			{"sequence":sequence,
			"strategy": select.options[select.selectedIndex].value}));

		xmlHttp.onreadystatechange=(e)=>{
			if(xmlHttp.readyState == 4) {
				response = JSON.parse(xmlHttp.responseText)
				steps = response["steps"];
				console.log(response);
				var table = document.getElementById('stats-table');

				var row = table.insertRow();

				if(response['status'] == 'failure') {
					row.innerHTML =
				`<td>${response['strategy']}</td>	
				 <td>${response['nodes explored']}</td>
				 <td>${response['running time']}</td>
				 <td>No solution found</td>`;
				} else {
					row.innerHTML =
					`<td>${response['strategy']}</td>	
					<td>${response['nodes explored']}</td>
					<td>${response['running time']}</td>
					<td>${response['path cost']}</td>`;
					currentStep = 0;
					blankCell = getEmptyCell()
					transitionEndHandler()
				}

				 console.log(response["status"]);

			}
		}

	}

	function transitionEndHandler() {
		if (currentStep >= steps.length)
			return
		var swapped = getCellGivenDicection(blankCell, steps[currentStep]);
		currentStep++;

		swapCells(blankCell, swapped);
	}

	function initGame() {
		puzzle.innerHTML = '';

		var n = 1;
		for(var i = 0; i < rows; i++){
			for(var j = 0; j < cols; j++){
				var cell = document.createElement('span');
				cell.id = 'cell-'+i+'-'+j;
				cell.style.left = (j*80+1*j+1)+'px';
				cell.style.top = (i*80+1*i+1)+'px';

				if(n <= rows * cols - 1){
					cell.classList.add('number');
					cell.classList.add((i%2==0 && j%2>0 || i%2>0 && j%2==0) ? 'dark' : 'light');
					cell.innerHTML = (n++).toString();
				} else {
					cell.className = 'empty';
					var transitionEnd = transitionEndEventName();
					cell.addEventListener(transitionEnd, transitionEndHandler, false);
				}

				puzzle.appendChild(cell);
			}
		}

		p = document.getElementById('puzzle');
		p.style.width = (rows * 80 + 5) + 'px';
		p.style.height = (cols * 80 + 5) + 'px';


	}

	function transitionEndEventName () {
	    var i,
	        undefined,
	        el = document.createElement('div'),
	        transitions = {
	            'transition':'transitionend',
	            'OTransition':'otransitionend',  // oTransitionEnd in very old Opera
	            'MozTransition':'transitionend',
	            'WebkitTransition':'webkitTransitionEnd'
	        };

	    for (i in transitions) {
	        if (transitions.hasOwnProperty(i) && el.style[i] !== undefined) {
	            return transitions[i];
	        }
	    }

	    //TODO: throw 'TransitionEnd event is not supported in this browser';
	}

	/**
	 * Shifts number cell to the empty cell
	 *
	 */
	function shiftCell(cell){

		// Checks if selected cell has number
		if(cell.clasName != 'empty'){

			// Tries to get empty adjacent cell
			var emptyCell = getEmptyAdjacentCell(cell);

			if(emptyCell){
				// Temporary data
				var tmp = {style: cell.style.cssText, id: cell.id};

				// Exchanges id and style values
				cell.style.cssText = emptyCell.style.cssText;
				cell.id = emptyCell.id;
				emptyCell.style.cssText = tmp.style;
				emptyCell.id = tmp.id;

				if(state == 1){
					// Checks the order of numbers
					checkOrder();
				}
			}
		}

	}

	function getCellGivenDicection(cell, dicrection) {
		var split = cell.id.split('-');
		var row = parseInt(split[1]);
		var col = parseInt(split[2]);
		if (dicrection == 'up')
			row = row - 1;
		else if (dicrection == 'down')
			row = row + 1;
		else if (dicrection == 'left')
			col = col - 1;
		else if (dicrection == 'right')
			col = col + 1;

		return getCell(row, col);
	}

	function swapCells(cellOne, cellTwo) {
		var tmp = {style: cellOne.style.cssText, id: cellOne.id};

		// Exchanges id and style values
		cellOne.style.cssText = cellTwo.style.cssText;
		cellOne.id = cellTwo.id;

		cellTwo.style.cssText = tmp.style;
		cellTwo.id = tmp.id;
	}

	/**
	 * Gets specific cell by row and column
	 *
	 */
	function getCell(row, col){

		return document.getElementById('cell-'+row+'-'+col);

	}

	/**
	 * Gets empty cell
	 *
	 */
	function getEmptyCell(){

		return puzzle.querySelector('.empty');

	}

	/**
	 * Gets empty adjacent cell if it exists
	 *
	 */
	function getEmptyAdjacentCell(cell){

		// Gets all adjacent cells
		var adjacent = getAdjacentCells(cell);

		// Searches for empty cell
		for(var i = 0; i < adjacent.length; i++){
			if(adjacent[i].className == 'empty'){
				return adjacent[i];
			}
		}

		// Empty adjacent cell was not found
		return false;

	}

	/**
	 * Gets all adjacent cells
	 *
	 */
	function getAdjacentCells(cell){

		var id = cell.id.split('-');

		// Gets cell position indexes
		var row = parseInt(id[1]);
		var col = parseInt(id[2]);

		var adjacent = [];

		// Gets all possible adjacent cells
		if(row < rows - 1){adjacent.push(getCell(row+1, col));}
		if(row > 0){adjacent.push(getCell(row-1, col));}
		if(col < cols - 1){adjacent.push(getCell(row, col+1));}
		if(col > 0){adjacent.push(getCell(row, col-1));}

		return adjacent;

	}

	/**
	 * Chechs if the order of numbers is correct
	 *
	 */
	function checkOrder(){

		// Checks if the empty cell is in correct position
		if(getCell(rows - 1, cols - 1).className != 'empty'){
			return;
		}

		var n = 1;
		// Goes through all cells and checks numbers
		for(var i = 0; i <= 3; i++){
			for(var j = 0; j <= 3; j++){
				if(n <= 15 && getCell(i, j).innerHTML != n.toString()){
					// Order is not correct
					return;
				}
				n++;
			}
		}

		// Puzzle is solved, offers to scramble it
		if(confirm('Congrats, You did it! \nScramble the puzzle?')){
			scramble();
		}

	}

	/**
	 * Scrambles puzzle
	 *
	 */
	function scramble(){

		if(state == 0){
			return;
		}

		puzzle.removeAttribute('class');
		state = 0;

		var previousCell;
		var i = 1;
		var interval = setInterval(function(){
			if(i <= 100){
				var adjacent = getAdjacentCells(getEmptyCell());
				if(previousCell){
					for(var j = adjacent.length-1; j >= 0; j--){
						if(adjacent[j].innerHTML == previousCell.innerHTML){
							adjacent.splice(j, 1);
						}
					}
				}
				// Gets random adjacent cell and memorizes it for the next iteration
				previousCell = adjacent[rand(0, adjacent.length-1)];
				shiftCell(previousCell);
				i++;
			} else {
				clearInterval(interval);
				state = 1;
			}
		}, 5);

	}

	/**
	 * Generates random number
	 *
	 */
	function rand(from, to){

		return Math.floor(Math.random() * (to - from + 1)) + from;

	}

	function generate() {

		var numbers = document.getElementById('numbers').value.split(" ");

		if (numbers.length == 0) {
			return;
		}

		rows = cols = Math.sqrt(numbers.length);

		console.log(rows);

		puzzle.innerHTML = '';

		for(var i = 0; i < rows; i++){
			for(var j = 0; j < cols; j++){
				n = numbers[cols * i + j];
				var cell = document.createElement('span');
				cell.id = 'cell-'+i+'-'+j;
				cell.style.left = (j*80+1*j+1)+'px';
				cell.style.top = (i*80+1*i+1)+'px';

				if(n != 0){
					cell.classList.add('number');
					cell.classList.add((i%2==0 && j%2>0 || i%2>0 && j%2==0) ? 'dark' : 'light');
					cell.innerHTML = (n).toString();
				} else {
					cell.className = 'empty';
					var transitionEnd = transitionEndEventName();
					cell.addEventListener(transitionEnd, transitionEndHandler, false);
				}

				puzzle.appendChild(cell);
			}
		}

		p = document.getElementById('puzzle');
		p.style.width = (rows * 80 + 5) + 'px';
		p.style.height = (cols * 80 + 5) + 'px';

	}

}());
