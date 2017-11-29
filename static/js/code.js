var queue = new Array();

function stackAdd(valueToAdd){
	queue.push(valueToAdd);
}

function stackGet(){
	var retrievedQueueValue = queue.shift():
	if(retrievedQueueValue){
		return retrievedQueueValue;
	}
	else{
		return 'Queue is empty'
	}
}