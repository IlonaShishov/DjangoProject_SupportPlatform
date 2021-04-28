function completeDesc(me, parts) {
	// var index = me.parentNode.parentNode.rowIndex
	var elementId = me.id
	var elementIndex = elementId.split("_").pop();
	var input = document.getElementById(elementId).value;

	if( parts[input] ) {
		document.getElementById("part_description_" + elementIndex).value = parts[input];
	}
	else{
		document.getElementById("part_description_" + elementIndex).value = '';
	}
}


function toggleHiddenInput(me) {
	var elementIndex = me.id.split("_").pop();

	if (me.checked) {
		document.getElementById("hidden_charge_" + elementIndex).remove();
	}
	else {
		var element_hidden_input = document.createElement("input");
		element_hidden_input.type = "hidden";
		element_hidden_input.name="charge";
		element_hidden_input.id="hidden_charge_" + elementIndex;
		element_hidden_input.value="0";
		me.parentNode.appendChild(element_hidden_input);
	}
}


function addRow(tableID, parts) {
	var table = document.getElementById(tableID);

	var rowCount = table.rows.length;
	var row = table.insertRow(rowCount-1);

	while (document.getElementById('part_num_' + rowCount) !=null) {
		rowCount++;
	}

	// remove button
	var cell1 = row.insertCell(0);
	var element1 = document.createElement("button");
	element1.type = "button";
	element1.name="remove_btn";
	element1.setAttribute('class', 'btn btn-primary add_or_del_btn');
	element1.innerHTML="-";
	element1.onclick = function() {deleteRow(this, tableID);};
	cell1.appendChild(element1);

	// part num
	var cell2 = row.insertCell(1);
	var element2 = document.createElement("input");
	element2.type = "text";
	element2.name="part_num";
	element2.id="part_num_" + rowCount;
	element2.setAttribute('class', 'form-control');
	element2.oninput = function() {completeDesc(this, parts);};
	cell2.appendChild(element2);

	// part description
	var cell3 = row.insertCell(2);
	var element3 = document.createElement("input");
	element3.type = "text";
	element3.name="part_description";
	element3.id="part_description_" + rowCount;
	element3.setAttribute("readonly", true);
	element3.setAttribute('class', 'form-control');
	cell3.appendChild(element3);

	// part qty
	var cell4 = row.insertCell(3);
	var element4 = document.createElement("input");
	element4.type = "text";
	element4.name="qty";
	element4.setAttribute('class', 'form-control');
	cell4.appendChild(element4);

	// charge checkbox
	var cell5 = row.insertCell(4);
	var element_div = document.createElement("div");
	element_div.setAttribute('class', 'form-check charge_cb');

	var element_hidden_input = document.createElement("input");
	element_hidden_input.type = "hidden";
	element_hidden_input.name="charge";
	element_hidden_input.id="hidden_charge_" + rowCount;
	element_hidden_input.value="0";

	var element_input = document.createElement("input");
	element_input.type = "checkbox";
	element_input.name="charge";
	element_input.id="charge_" + rowCount;
	element_input.value="1";
	element_input.onclick = function() {toggleHiddenInput(this);};

	var element_label = document.createElement("label");
	element_label.for = "charge";
	element_label.innerHTML="Charge";
	element_label.setAttribute('class', 'add_row_cb');

	element_div.appendChild(element_hidden_input);
	element_div.appendChild(element_input);
	element_div.appendChild(element_label);

	cell5.appendChild(element_div);
}

  function deleteRow(me, tableID) {
	try {
	var table = document.getElementById(tableID);
	table.deleteRow(me.parentNode.parentNode.rowIndex);
	}
	catch(e) {
		alert(e);
	}
}

function calculateTime() {

	var start_time = document.getElementById('visit_start');
	var end_time = document.getElementById('visit_end');
	var tot_time = document.getElementById('visit_hours');

	if (start_time.value && end_time.value) {
		console.log('test');


		// start_time_lst = start_time.value.split(":");
		// var start_date = new Date();
		// start_date.setHours(start_time_lst[0]);
		// start_date.setMinutes(start_time_lst[1]);
		// console.log(start_date);

		// end_time_lst = end_time.value.split(":");
		// var end_date = new Date();
		// end_date.setHours(end_time_lst[0]);
		// end_date.setMinutes(end_time_lst[1]);
		// console.log(end_date);

		// var hours = Math.abs(date1 - date2) / 36e5;
		// console.log(hours);


	}
	else {
		tot_time.value = ''
	}

}