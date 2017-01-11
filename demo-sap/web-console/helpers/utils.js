/************************************************
 * 
 ************************************************/
Array.prototype.rotate = function(n) {
    while (this.length && n < 0) {
    	n += this.length;
    } 

    this.push.apply(this, this.splice(0, n));

    return this;
}

/************************************************
 * 
 ************************************************/
var addRotate = function(arr, n, max) {
	if(arr.length >= max) {
		arr = arr.rotate(1)
		arr[arr.length-1] = n;
	}
	else {
		arr.push(n);
	}

	return arr;
}

exports.addRotate = addRotate;