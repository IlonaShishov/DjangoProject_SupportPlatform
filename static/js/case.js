function completeProperties(me, equip_properties, equip_sn_lst, equip_pn_lst, equip_description_lst) {

	var elementId = me.id
	var elementIndex = elementId.split("_").pop();
	var input = document.getElementById(elementId).value;

	if (!input) {

		document.getElementById("serial_number_" + elementIndex).value = '';
		document.getElementById("part_number_" + elementIndex).value = '';
		document.getElementById("equip_description_" + elementIndex).value = '';
		document.getElementById("installation_date_" + elementIndex).value = '';
		document.getElementById("warranty_" + elementIndex).value = '';

		original_sn_element = document.getElementById("serial_number_list_" + elementIndex);
		parent_sn_element = original_sn_element.parentNode;
		original_sn_element.remove();

		var new_sn_datalist = document.createElement("datalist");
		new_sn_datalist.id = "serial_number_list_" + elementIndex;
		for (i=0; i < equip_sn_lst.length; i ++) {
			var option = document.createElement('option');
			option.value = equip_sn_lst[i];
			new_sn_datalist.appendChild(option);
		parent_sn_element.appendChild(new_sn_datalist);
		}

		original_pn_element = document.getElementById("part_number_list_" + elementIndex);
		parent_pn_element = original_pn_element.parentNode;
		original_pn_element.remove();

		var new_pn_datalist = document.createElement("datalist");
		new_pn_datalist.id = "part_number_list_" + elementIndex;
		for (i=0; i < equip_pn_lst.length; i ++) {
			var option = document.createElement('option');
			option.value = equip_pn_lst[i];
			new_pn_datalist.appendChild(option);
		parent_pn_element.appendChild(new_pn_datalist);
		}

		original_desc_element = document.getElementById("equip_description_list_" + elementIndex);
		parent_desc_element = original_desc_element.parentNode;
		original_desc_element.remove();

		var new_desc_datalist = document.createElement("datalist");
		new_desc_datalist.id = "equip_description_list_" + elementIndex;
		for (i=0; i < equip_description_lst.length; i ++) {
			var option = document.createElement('option');
			option.value = equip_description_lst[i];
			new_desc_datalist.appendChild(option);
		parent_desc_element.appendChild(new_desc_datalist);
		}
	}

	else if(elementId.includes("serial_number")){
		const items = equip_properties.filter(item => item.sn == input);

		if (items.length == 0){
			document.getElementById("part_number_" + elementIndex).value = '';
			document.getElementById("equip_description_" + elementIndex).value = '';
			document.getElementById("installation_date_" + elementIndex).value = '';
			document.getElementById("warranty_" + elementIndex).value = '';
		}

		else{
			original_pn_element = document.getElementById("part_number_list_" + elementIndex);
			parent_pn_element = original_pn_element.parentNode;
			original_pn_element.remove();

			var new_pn_datalist = document.createElement("datalist");
			new_pn_datalist.id = "part_number_list_" + elementIndex;
			for (i=0; i < items.length; i ++) {
				var option = document.createElement('option');
				option.value = items[i].pn;
				new_pn_datalist.appendChild(option);
			parent_pn_element.appendChild(new_pn_datalist);
			}

			original_desc_element = document.getElementById("equip_description_list_" + elementIndex);
			parent_desc_element = original_desc_element.parentNode;
			original_desc_element.remove();

			var new_desc_datalist = document.createElement("datalist");
			new_desc_datalist.id = "equip_description_list_" + elementIndex;
			for (i=0; i < items.length; i ++) {
				var option = document.createElement('option');
				option.value = items[i].description;
				new_desc_datalist.appendChild(option);
			parent_desc_element.appendChild(new_desc_datalist);
			}

			if (items.length == 1){
			document.getElementById("part_number_" + elementIndex).value = items[0].pn;
			document.getElementById("equip_description_" + elementIndex).value = items[0].description;
			document.getElementById("installation_date_" + elementIndex).value = items[0].date;
			document.getElementById("warranty_" + elementIndex).value = items[0].warranty;
			}
		}
	}

	else if(elementId.includes("part_number")){

		var items = equip_properties.filter(item => item.pn == input);

		if (document.getElementById("equip_description_" + elementIndex).value){
			items = items.filter(item => item.description.includes(document.getElementById("equip_description_" + elementIndex).value));
		}

		if (items.length == 0){
			document.getElementById("serial_number_" + elementIndex).value = '';
			document.getElementById("equip_description_" + elementIndex).value = '';
			document.getElementById("installation_date_" + elementIndex).value = '';
			document.getElementById("warranty_" + elementIndex).value = '';
		}

		else{
			original_sn_element = document.getElementById("serial_number_list_" + elementIndex);
			parent_sn_element = original_sn_element.parentNode;
			original_sn_element.remove();

			var new_sn_datalist = document.createElement("datalist");
			new_sn_datalist.id = "serial_number_list_" + elementIndex;
			for (i=0; i < items.length; i ++) {
				var option = document.createElement('option');
				option.value = items[i].sn;
				new_sn_datalist.appendChild(option);
			parent_sn_element.appendChild(new_sn_datalist);
			}

			original_desc_element = document.getElementById("equip_description_list_" + elementIndex);
			parent_desc_element = original_desc_element.parentNode;
			original_desc_element.remove();

			var new_desc_datalist = document.createElement("datalist");
			new_desc_datalist.id = "equip_description_list_" + elementIndex;
			for (i=0; i < items.length; i ++) {
				var option = document.createElement('option');
				option.value = items[i].description;
				new_desc_datalist.appendChild(option);
			parent_desc_element.appendChild(new_desc_datalist);
			}

			if (items.length == 1){
			document.getElementById("serial_number_" + elementIndex).value = items[0].sn;
			document.getElementById("equip_description_" + elementIndex).value = items[0].description;
			document.getElementById("installation_date_" + elementIndex).value = items[0].date;
			document.getElementById("warranty_" + elementIndex).value = items[0].warranty;
			}
		}
	}

	else if(elementId.includes("equip_description")){

		var items = equip_properties.filter(item => item.description.includes(input));

		if (document.getElementById("part_number_" + elementIndex).value){
			items = items.filter(item => item.pn == document.getElementById("part_number_" + elementIndex).value);
		}


		if (items.length == 0){
			document.getElementById("serial_number_" + elementIndex).value = '';
			document.getElementById("part_number_" + elementIndex).value = '';
			document.getElementById("installation_date_" + elementIndex).value = '';
			document.getElementById("warranty_" + elementIndex).value = '';
		}

		else{
			original_sn_element = document.getElementById("serial_number_list_" + elementIndex);
			parent_sn_element = original_sn_element.parentNode;
			original_sn_element.remove();

			var new_sn_datalist = document.createElement("datalist");
			new_sn_datalist.id = "serial_number_list_" + elementIndex;
			for (i=0; i < items.length; i ++) {
				var option = document.createElement('option');
				option.value = items[i].sn;
				new_sn_datalist.appendChild(option);
			parent_sn_element.appendChild(new_sn_datalist);
			}

			original_pn_element = document.getElementById("part_number_list_" + elementIndex);
			parent_pn_element = original_pn_element.parentNode;
			original_pn_element.remove();

			var new_pn_datalist = document.createElement("datalist");
			new_pn_datalist.id = "part_number_list_" + elementIndex;
			for (i=0; i < items.length; i ++) {
				var option = document.createElement('option');
				option.value = items[i].pn;
				new_pn_datalist.appendChild(option);
			parent_pn_element.appendChild(new_pn_datalist);
			}

			if (items.length == 1){
			document.getElementById("serial_number_" + elementIndex).value = items[0].sn;
			document.getElementById("part_number_" + elementIndex).value = items[0].pn;
			document.getElementById("installation_date_" + elementIndex).value = items[0].date;
			document.getElementById("warranty_" + elementIndex).value = items[0].warranty;
			}
		}
	}	

	else{
		//pass
	}
}

function addRow(tableID, equip_properties, equip_sn_lst, equip_pn_lst, equip_description_lst) {
	var table = document.getElementById(tableID);

	var rowCount = table.rows.length;
	var row = table.insertRow(rowCount-1);

	while (document.getElementById('serial_number_' + rowCount) !=null) {
		rowCount++;
	}

	// create "remove" button
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
	element2_input.setAttribute("list", "serial_number_list_" + rowCount);
	element2_input.placeholder="Choose...";
	element2_input.id="serial_number_" + rowCount;
	element2_input.oninput = function() {completeProperties(this, equip_properties, equip_sn_lst, equip_pn_lst, equip_description_lst);};
	
	var element2_datalist = document.createElement("datalist");
	element2_datalist.id = "serial_number_list_" + rowCount;
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
	element3_input.setAttribute("list", "part_number_list_" + rowCount);
	element3_input.placeholder="Choose...";
	element3_input.id="part_number_" + rowCount;
	element3_input.oninput = function() {completeProperties(this, equip_properties, equip_sn_lst, equip_pn_lst, equip_description_lst);};
	
	var element3_datalist = document.createElement("datalist");
	element3_datalist.id = "part_number_list_" + rowCount;
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
	element4_input.setAttribute("list", "equip_description_list_" + rowCount);
	element4_input.placeholder="Choose...";
	element4_input.id="equip_description_" + rowCount;
	element4_input.oninput = function() {completeProperties(this, equip_properties, equip_sn_lst, equip_pn_lst, equip_description_lst);};
	
	var element4_datalist = document.createElement("datalist");
	element4_datalist.id = "equip_description_list_" + rowCount;
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
	element5.setAttribute('class', 'form-control text_bar');
	element5.type = "text";
	element5.name="installation_date";
	element5.id="installation_date_" + rowCount;
	element5.setAttribute("readonly", true);

	cell5.appendChild(element5);

	// warranty
	var cell6 = row.insertCell(5);
	var element6_input = document.createElement("input");
	element6_input.setAttribute('class', 'form-control inline_it');
	element6_input.type = "text";
	element6_input.name="warranty";
	element6_input.id="warranty_" + rowCount;
	element6_input.setAttribute("readonly", true);

	var element6_label = document.createElement("label");
	var element6_small = document.createElement("small");
	element6_small.innerHTML = "months";

	element6_label.appendChild(element6_small);
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

function statusReason(on_hold_str='', cancellation_str=''){

	if (document.getElementById('reason') !=null){
			document.getElementById('reason').remove();
		}
	var status = document.getElementById("status").value;

	if (status == "On Hold"){
		var element_div = document.createElement("div");
		element_div.setAttribute('class', 'form-group reason_bar');
		element_div.id="reason";

		var element_label = document.createElement("label");
		element_label.innerHTML = "On Hold Reason";

		var element_textarea = document.createElement("textarea");
		element_textarea.setAttribute('class', 'form-control');
		element_textarea.name="on_hold_reason";
		element_textarea.rows="3";
		element_textarea.id="on_hold_reason";
		element_textarea.innerHTML = on_hold_str;

		element_div.appendChild(element_label);
		element_div.appendChild(element_textarea);

		var placement_node = document.getElementById("first_solid");
		var status_parent = document.getElementById("status").parentNode.parentNode
		status_parent.insertBefore(element_div, placement_node);


	}

	else if (status == "Cancelled"){
		var element_div = document.createElement("div");
		element_div.setAttribute('class', 'form-group reason_bar');
		element_div.id="reason";

		var element_label = document.createElement("label");
		element_label.innerHTML = "Cancellation Reason";

		var element_textarea = document.createElement("textarea");
		element_textarea.setAttribute('class', 'form-control');
		element_textarea.name="cancellation_reason";
		element_textarea.rows="3";
		element_textarea.id="cancellation_reason";
		element_textarea.innerHTML = cancellation_str;


		element_div.appendChild(element_label);
		element_div.appendChild(element_textarea);

		var placement_node = document.getElementById("first_solid");
		var status_parent = document.getElementById("status").parentNode.parentNode
		status_parent.insertBefore(element_div, placement_node);
	}

	else{
		//pass
	}
}
