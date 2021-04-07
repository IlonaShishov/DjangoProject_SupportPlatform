function addRow(tableID, equip_sn_lst, equip_pn_lst, equip_description_lst) {
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

	// serial number
	var cell2 = row.insertCell(1);
	var element2_input = document.createElement("input");
	element2_input.setAttribute('class', 'form-control text_bar');
	element2_input.type = "text";
	element2_input.name="serial_number";
	element2_input.setAttribute("list", "serial_number");
	element2_input.placeholder="Choose...";
	element2_input.id="serial_number_" + rowCount;
	// element2.oninput = function() {completeDesc(this, parts);};
	
	var element2_datalist = document.createElement("datalist");
	element2_datalist.id = "serial_number";
	for (i=0; i < equip_sn_lst.length; i ++) {
		var option = document.createElement('option');
		option.value = equip_sn_lst[i];
		element2_datalist.appendChild(option);
	}

	cell2.appendChild(element2_input);
	cell2.appendChild(element2_datalist);


	// part number
	var cell3 = row.insertCell(2);
	var element3_input = document.createElement("input");
	element3_input.setAttribute('class', 'form-control text_bar');
	element3_input.type = "text";
	element3_input.name="part_number";
	element3_input.setAttribute("list", "part_number");
	element3_input.placeholder="Choose...";
	element3_input.id="part_number_" + rowCount;
	// element2.oninput = function() {completeDesc(this, parts);};
	
	var element3_datalist = document.createElement("datalist");
	element2_datalist.id = "part_number";
	for (i=0; i < equip_pn_lst.length; i ++) {
        var option = document.createElement('option');
        option.value = equip_pn_lst[i];
        element3_datalist.appendChild(option);
    }

	cell3.appendChild(element3_input);
	cell3.appendChild(element3_datalist);


	// equip description
	var cell4 = row.insertCell(3);
	var element4_input = document.createElement("input");
	element4_input.setAttribute('class', 'form-control text_bar');
	element4_input.type = "text";
	element4_input.name="equip_description";
	element4_input.setAttribute("list", "equip_description");
	element4_input.placeholder="Choose...";
	element4_input.id="equip_description_" + rowCount;
	// element2.oninput = function() {completeDesc(this, parts);};
	
	var element4_datalist = document.createElement("datalist");
	element2_datalist.id = "equip_description";
	for (i=0; i < equip_description_lst.length; i ++) {
        var option = document.createElement('option');
        option.value = equip_description_lst[i];
        element4_datalist.appendChild(option);
    }

	cell4.appendChild(element4_input);
	cell4.appendChild(element4_datalist);


	// installation date
	var cell5 = row.insertCell(4);
	var element5 = document.createElement("input");
	element5.setAttribute('class', 'form-control datepicker');
	element5.type = "date";
	element5.name="installation_date";
	element5.id="installation_date_" + rowCount;

	cell5.appendChild(element5);

	// warranty
	var cell6 = row.insertCell(5);
	var element6_input = document.createElement("input");
	element6_input.setAttribute('class', 'form-control inline_it');
	element6_input.type = "text";
	element6_input.name="warranty";
	element6_input.id="warranty_" + rowCount;

	var element6_label = document.createElement("label");
	element6_label.innerHTML = "months"

	cell6.appendChild(element6_input);
	cell6.appendChild(element6_label);

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