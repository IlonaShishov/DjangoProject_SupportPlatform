function myFunction(parts) {
	var input = document.getElementById("part_num").value;
	if( parts[input] ) {
		document.getElementById("part_description").value = parts[input];
	}
	else{
		document.getElementById("part_description").value = '';
	}
}


function addRow(tableID) {
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
	// element1.setAttribute('onclick','deleteRow('+this+', '+tableID+');');
	cell1.appendChild(element1);

	// part num
	var cell2 = row.insertCell(1);
	var element2 = document.createElement("input");
	element2.type = "text";
	element2.name="part_num";
	element2.id="part_num";
	element2.setAttribute('class', 'form-control');
	cell2.appendChild(element2);

	// part description
	var cell3 = row.insertCell(2);
	var element3 = document.createElement("input");
	element3.type = "text";
	element3.name="part_description";
	element3.id="part_description";
	element3.setAttribute("disabled", true);
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

	var element_input = document.createElement("input");
	element_input.type = "checkbox";
	element_input.name="charge";

	var element_label = document.createElement("label");
	element_label.for = "charge";
	element_label.innerHTML="Charge";
	element_label.setAttribute('class', 'add_row_cb');

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

