/**
 * http://usejsdoc.org/
 */
var createMachine = function(containerId, machineNum, titles, chartNames, notes) {
	var row = $("<div/>", {
		class: 'row'
	});
	for(var i =0; i < machineNum; i++) {
		if(0 == i/3) {
			row = $("<div/>", {
				class: 'row'
			});
		}
		var col = $("<div/>", {
			class: 'col-sm-6 col-md-4'
		});
		var chartWrapper = $("<div/>", {
			class: 'chart-wrapper'
		});
		
		var charTitle = $("<div/>", {
			class: 'chart-title',
			text: titles[i]
		});
		var chartStage = $("<div/>", {
			class: 'chart-stage'
		});
		var chart = $("<div/>", {
			id: chartNames[i]
		});
		var chartNotes = $("<div/>", {
			class: 'chart-notes',
			text: notes[i]
		});
		
		chartStage.append(chart);
		chartWrapper.append(charTitle);
		chartWrapper.append(chartStage);
		chartWrapper.append(chartNotes);
		col.append(chartWrapper);
		row.append(col);
		
		$('#' + containerId).append(row);
		console.log($('#' + containerId));
	}
}
$(function() {
	var titles = ['1', '2', '3', '4', '5', '6', '7'];
	var chartNames = ['1', '2', '3', '4', '5', '6', '7'];
	var notes = ['1', '2', '3', '4', '5', '6', '7'];
	createMachine('containerChart', 7, titles, chartNames, notes)
});