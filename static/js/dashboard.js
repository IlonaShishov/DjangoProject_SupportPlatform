function ifMachineDown(me, machine_down) {
	if (machine_down){
		document.getElementById(me.id).setAttribute('class', 'machine_down');
	}
}