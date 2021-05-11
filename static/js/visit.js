function completeDesc(me, parts) {
	var input = me.value;
	me.setCustomValidity("");


	me.parentNode.parentNode.classList.remove("alert_row_desc");
	if( parts[input] ) {
		me.parentNode.nextElementSibling.firstElementChild.value = parts[input];
		me.parentNode.nextElementSibling.nextElementSibling.firstElementChild.required = true;
	}
	else{
		me.parentNode.nextElementSibling.firstElementChild.value = '';
		me.parentNode.nextElementSibling.nextElementSibling.firstElementChild.required = false;
		if(me.value){
			me.setCustomValidity("Please Select a valid part number");
			me.parentNode.parentNode.classList.add('class', 'alert_row_desc');

		}
	}
}


function toggleHiddenInput(me) {

	if (me.checked) {
		me.parentNode.firstElementChild.remove();
	}
	else {
		var element_hidden_input = document.createElement("input");
		element_hidden_input.type = "hidden";
		element_hidden_input.name="charge";
		element_hidden_input.value="0";
		me.parentNode.insertBefore(element_hidden_input, me);

	}
}


function addRow(tableID, parts) {
	var table = document.getElementById(tableID);

	var rowCount = table.rows.length;
	var row = table.insertRow(rowCount-1);


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
	element2.setAttribute('class', 'form-control');
	element2.oninput = function() {completeDesc(this, parts);};
	cell2.appendChild(element2);

	// part description
	var cell3 = row.insertCell(2);
	var element3 = document.createElement("input");
	element3.type = "text";
	element3.name="part_description";
	element3.setAttribute("readonly", true);
	element3.setAttribute('class', 'form-control');
	cell3.appendChild(element3);

	// part qty
	var cell4 = row.insertCell(3);
	var element4 = document.createElement("input");
	element4.type = "text";
	element4.name="qty";
	element4.setAttribute('class', 'form-control');
	element4.oninput = function() {IntValueValidation(this);};
	cell4.appendChild(element4);

	// charge checkbox
	var cell5 = row.insertCell(4);
	var element_div = document.createElement("div");
	element_div.setAttribute('class', 'form-check charge_cb');

	var element_hidden_input = document.createElement("input");
	element_hidden_input.type = "hidden";
	element_hidden_input.name="charge";
	element_hidden_input.value="0";

	var element_input = document.createElement("input");
	element_input.type = "checkbox";
	element_input.name="charge";
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

		start_time_lst = start_time.value.split(":");
		var start_date = new Date();
		start_date.setHours(start_time_lst[0]);
		start_date.setMinutes(start_time_lst[1]);

		end_time_lst = end_time.value.split(":");
		var end_date = new Date();
		end_date.setHours(end_time_lst[0]);
		end_date.setMinutes(end_time_lst[1]);

		if (end_date > start_date) {
			var hours = (Math.abs(end_date - start_date) / 36e5).toFixed(2);
			tot_time.value = hours;	
		}
		else {
			var hours = (Math.abs(end_date.setDate(end_date.getDate() + 1) - start_date) / 36e5).toFixed(2)
			tot_time.value = hours;	
		}

	}

	else {

		tot_time.value = ''

	}

}

function listValueValidation(me) {
	
	if(me.value && document.querySelector("#"+me.getAttribute('list') + " option[value='" + me.value+ "']") === null){
		me.setCustomValidity("Please select a valid value.");
	}
	else{
		me.setCustomValidity("");
	}
}

function IntValueValidation(me) {
	me.parentNode.parentNode.classList.remove("alert_row_qty");
	// if (!me.value || me.value >>> 0 === parseFloat(me.value)){
	if (!me.value || me.value.match("^[1-9][0-9]*$")){
		me.setCustomValidity("");
	}
	else{
		me.setCustomValidity("Please enter a whole number");
		me.parentNode.parentNode.classList.add('class', 'alert_row_qty');

	}
}