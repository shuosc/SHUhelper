module.exports = function(elt, rootElt) {
	
	var dataAttrMap = {};
	for ( ; elt !== rootElt && elt !== null; elt = elt.parentNode )
		if ( elt.nodeType === 1 )
			for ( var propName in elt.dataset )
				dataAttrMap[propName] = elt.dataset[propName];
	return dataAttrMap;
}
