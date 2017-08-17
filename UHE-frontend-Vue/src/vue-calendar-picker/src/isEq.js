module.exports = function isEq(val1, val2) {
	
	if ( val1 === val2 )
		return true;
	
	var type1 = typeof(val1);
	if ( type1 !== typeof(val2) )
		return false;

	if ( type1 === 'object' && val1 !== null && val2 !== null ) {
		
		var k1 = Object.keys(val1);
		var k1len = k1.length;
		if ( Object.keys(val2).length !== k1len )
			return false;

		for ( var i = 0; i < k1len; ++i )
			if ( !isEq(val1[k1[i]], val2[k1[i]]) )
				return false;
		return true;
	}
	return false;
}