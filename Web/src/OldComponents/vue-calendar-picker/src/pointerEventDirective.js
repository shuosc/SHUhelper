var docComputedStyles = window.getComputedStyle(window.document.documentElement);
var hasUserSelect = 'userSelect' in docComputedStyles || 'MozUserSelect' in docComputedStyles || 'OUserSelect' in docComputedStyles || 'msUserSelect' in docComputedStyles || 'WebkitUserSelect' in docComputedStyles;
var hasTouchScreen = 'ontouchstart' in window || navigator.maxTouchPoints;
var hasMouse = true;

var uaName = navigator.appVersion;
var pos = uaName.indexOf('MSIE ');
var ieVer = pos !== -1 ? parseFloat(uaName.substr(pos+5, uaName.indexOf(';', pos))) : 0;


module.exports = function() {
	
	function hasKeyActive(cx, ev) {
		
		return ev.shiftKey || ev.ctrlKey || ev.altKey || ev.metaKey;
	}

	function hasPointerActive(cx, ev) {

		return 'buttonState' in cx ? cx.buttonState : ev.buttons !== 0;
	}


	function touchStartHandler(cx, ev) {

		cx.callback({ eventType:'down', eventTarget:ev.target, pointerActive:true, keyActive:false});
		
		cx.pressTimeout = setTimeout(function() {
		
			cx.callback({ eventType:'press', eventTarget:ev.target, pointerActive:true, keyActive:false});
		}, 1000);
	}
	
	function touchEndHandler(cx, ev) {

		if ( cx.pressTimeout !== undefined ) {
			
			clearTimeout(cx.pressTimeout);
			cx.pressTimeout = undefined;
		}
		
		cx.callback({ eventType:'up', eventTarget:ev.target, pointerActive:false, keyActive:false});
	}

	function touchMoveHandler(cx, ev) {
		
		if ( cx.pressTimeout !== undefined ) {
			
			clearTimeout(cx.pressTimeout);
			cx.pressTimeout = undefined;
		}
		
		ev.preventDefault();
		
		var eventTarget = document.elementFromPoint(ev.changedTouches[0].clientX, ev.changedTouches[0].clientY);
		cx.callback({ eventType:'over', eventTarget:eventTarget, pointerActive:true, keyActive:false});
	}
	
	function clickHandler(cx, ev) {
		
		cx.callback({ eventType:'tap', eventTarget:ev.target, pointerActive:false, keyActive:hasKeyActive(cx, ev)});
	}
	
	function dblclickHandler(cx, ev) {
		
		cx.callback({ eventType:'press', eventTarget:ev.target, pointerActive:false, keyActive:hasKeyActive(cx, ev)});
	}
	
	function mouseOverHandler(cx, ev) {
		
		cx.callback({ eventType:'over', eventTarget:ev.target, pointerActive:hasPointerActive(cx, ev), keyActive:hasKeyActive(cx, ev)});
	}
	
	function mouseDownHandler(cx, ev) {

		cx.callback({ eventType:'down', eventTarget:ev.target, pointerActive:true, keyActive:hasKeyActive(cx, ev)});
	}
	
	function mouseUpHandler(cx, ev) {

		cx.callback({ eventType:'up', eventTarget:ev.target, pointerActive:false, keyActive:hasKeyActive(cx, ev)});
	}
	
	
	function eventListener(el, eventName, handler) {
		
		el.addEventListener(eventName, handler);
		return el.removeEventListener.bind(el, eventName, handler);
	}

	return {
		bind: function(el, binding, vnode, oldVnode) {
			
			var cx = {
				el: el,
				callback: binding.value,
				offEvent: []
			}
			
			cx.offEvent.push( eventListener(el, 'click', clickHandler.bind(this, cx)) );
			cx.offEvent.push( eventListener(el, 'dblclick', dblclickHandler.bind(this, cx)) );

			// touch screen
			if ( hasTouchScreen ) {
				
				cx.offEvent.push( eventListener(el, 'touchstart', touchStartHandler.bind(this, cx)) );
				cx.offEvent.push( eventListener(el, 'touchmove', touchMoveHandler.bind(this, cx)) );
				cx.offEvent.push( eventListener(el, 'touchend', touchEndHandler.bind(this, cx)) );
			}
			
			if ( hasMouse ) {
				
				cx.offEvent.push( eventListener(el, 'mouseover', mouseOverHandler.bind(this, cx)) );
				cx.offEvent.push( eventListener(el, 'mousedown', mouseDownHandler.bind(this, cx)) );
				cx.offEvent.push( eventListener(el, 'mouseup', mouseUpHandler.bind(this, cx)) );
	
				if ( ieVer && ieVer === 9 ) {
					
					// IE9 does not update ev.buttons on mouseover event
					cx.buttonState = undefined;
					cx.offEvent.push( eventListener(document, 'mousedown', function(ev) { cx.buttonState = true } ) );
					cx.offEvent.push( eventListener(document, 'mouseup', function(ev) { cx.buttonState = false } ) );
				}
			}

			if ( !hasUserSelect )
				cx.offEvent.push( eventListener(el, 'selectstart', function(ev) { ev.preventDefault() } ) );

			el._onpointerCx = cx;
		},
		unbind: function(el, binding, vnode, oldVnode) {
			
			var cx = el._onpointerCx;
			while ( cx.offEvent.length !== 0 )
				cx.offEvent.pop()();
			el._onpointerCx = null;
		}
	}
}
