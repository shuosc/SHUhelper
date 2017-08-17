<template>
	<div class="calendar" :class="{ compact: compact, multiView: viewCount > 1 }" v-onpointer="pointerEvent">
		<div class="nav">
			<span class="prev" data-nav="-1"></span>
			<calendar-header v-if="viewCount === 1"></calendar-header>
			<span class="next" data-nav="1"></span>
		</div>
		<transition-group :name="animation" @after-enter="animation = ''" class="viewContainer">
			<calendar-view
				v-for="current in views(current, view, viewCount)"
				:key="viewId(current)"
				:style="{ width: (100/viewCount)+'%' }"
				
				:locale="locale"
				:compact="compact"
				:show-overlapping-days="showOverlappingDays !== undefined ? showOverlappingDays : viewCount === 1"
				:view="view"
				:current="current"
				:item-class="itemClass"
			>
				<template slot="header" scope="scope">
					<calendar-header v-if="viewCount > 1"></calendar-header>
				</template>
				<template scope="scope">
					<slot :item-range="scope.itemRange" :layout="scope.layout" ></slot>
				</template>
			</calendar-view>
		</transition-group>
	</div>
</template>

<style>

.calendar {
	position: relative;
	
	width: 20em;
	height: 16em;
	
	font-family: arial;
	font-size: 90%;

	display: inline-block;
	cursor: default;
	user-select: none;
	padding-top: 2.5em;
}

.calendar.compact {
	padding-top: 1.5em;
}


/* multi-view */

.calendar.multiView .viewContainer {
	position: absolute;
	top: 0;
}

.calendar.multiView .header {
	position: relative;
}

.calendar.multiView .content {
	margin-top: -2.5em; /* -header height, negative margin is legal */
	padding-top: 2.5em;
}

.calendar.compact.multiView .content {
	margin-top: -1.5em; /* -header height, negative margin is legal */
	padding-top: 1.5em;
}


/* calendar header & view header */

.calendar .header {
	height: 2em;
	padding-top: 0.5em;
	text-align: center;	
}


.calendar .header > span {
	cursor: pointer;
	padding: 0.5em;
}



.calendar.compact .header {
	height: 1.25em;
	padding-top: 0.25em;
}

.calendar.compact .header sup {
	vertical-align: initial;
}



/* nav */

.calendar .nav {
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	text-align: center;
}

.calendar .nav .prev,
.calendar .nav .next {
	position: absolute;
	top: 0;
	z-index: 1;
	font-size: 150%;
	padding: 0.3em 1em 0 1em;
	font-weight: bold;
	cursor: pointer;
}

.calendar .nav .prev {
	left: 0;
}

.calendar .nav .next {
	right: 0;
}

.calendar .nav .prev:before {
	content: '\2190';
}

.calendar .nav .next:before {
	content: '\2192';
}

.calendar.compact .nav .prev {
	padding: 0;
	left: 0.25em;
	top: -0.25em;
}

.calendar.compact .nav .next {
	padding: 0;
	right: 0.25em;
	top: -0.25em;
}



/* animations */

.calendar .viewContainer {
	display: block;
	position: relative;
	height: 100%;
	width: 100%;
	overflow: hidden;
	white-space: nowrap;
}

.calendar .view {
	transition-duration: .5s;
	transition-timing-function: ease-out;
	transition-property: transform, opacity;
}

.calendar .forwardSlide-leave-to,
.calendar .reverseSlide-enter {
	transform: translateX(-100%);
	opacity: 0;
}

.calendar .forwardSlide-enter,
.calendar .reverseSlide-leave-to {
	transform: translateX(100%);
	opacity: 0;
}

.calendar.multiView .reverseSlide-leave-to {
	transform: translateX(0);
}

.calendar .reverseSlide-leave-active,
.calendar .forwardSlide-leave-active {
	position: absolute;
}


.calendar .reverseScale-leave-to,
.calendar .forwardScale-enter {
	transform: scale(.5);
	opacity: 0;
}

.calendar .reverseScale-enter,
.calendar .forwardScale-leave-to {
	transform: scale(1.5);
	opacity: 0;
}

.calendar .reverseScale-leave-active,
.calendar .forwardScale-leave-active {
	position: absolute;
}


.calendar.multiView .view {
	border-left: 1px dotted lightgray;
}

.calendar.multiView .view:first-child {
	border-left: none;
}


/*
.calendar.multiView .view.reverseScale-leave-to,
.calendar.multiView .view.forwardSlide-leave-to {
	border-right: 1px solid silver;
}

.calendar.multiView .view:first-child,
.calendar.multiView .view.forwardSlide-leave-to + .view {
	border-left: none;
}


.calendar.multiView:not(.compact) .view {
	padding-left: 0.5em;
}

.calendar.multiView:not(.compact) .view:first-child,
.calendar.multiView:not(.compact) .forwardSlide-leave-to + .view {
	padding-left: 0;
}
*/


</style>

<script>
"use strict";

var calendarView = require('./calendarView.vue');
var calendarHeader = require('./calendarHeader.vue');

var df = require('date-fns'); // https://date-fns.org


var findDataAttr = require('./findDataAttr.js');

var isEq = require('./isEq.js');

var PERIOD = require('./period.js');

var mixin = require('./mixin.js');

module.exports = {
	mixins: [mixin],
	components: {
		calendarView: calendarView,
		calendarHeader: calendarHeader,
	},
	
	props: {
		initialView: {
			type: Number,
			default: PERIOD.MONTH,
			validator: function(value) {
				
				return value > PERIOD.HOUR && value < PERIOD.DECADE;
			}
		},
		initialCurrent: {
			type: [Date, String, Number],
			default: function() {
				return new Date
			},
			validator: function(value) {
				
				return df.isValid(df.parse(value));
			}
		},
		viewCount: {
			type: Number,
			default: 1,
			validator: function(value) {
				
				return value > 0;
			}
		},
		showOverlappingDays: {
			type: Boolean,
			default: undefined
		},
	},
	
	data: function() {
		return {
			animation: '',
			view: this.initialView,
			current: df.parse(this.initialCurrent),
		}
	},

	watch: {
		current: function(val, prev) {
			
			if ( !df.isEqual(val, prev) )
				this.animation = df.isAfter(val, prev) ? 'forwardSlide' : 'reverseSlide';
		},
		view: function(val, prev) {
			
			if ( val !== prev )
				this.animation = val > prev ? 'reverseScale' : 'forwardScale';
		},
	},
	
	methods: {
		
		views: function(current, type, count) {
			
			var views = [current];
			for ( var i = 1; i < count; ++i )
				views.push(this.dateAdd(current, type, i));
			return views;
		},
		
		viewId: function(current) {
			
			return String(this.view) + String(df.getTime(current));
		},

		pointerEvent: function(ev) {

			ev.dataAttr = findDataAttr(ev.eventTarget, this.$el);

			if ( ev.eventType === 'over' ) {
				
				if ( isEq(this.prevOverDataAttr, ev.dataAttr) )
					return;
				this.prevOverDataAttr = ev.dataAttr;
			} else {
				
				this.prevOverDataAttr = undefined;
			}

			if ( 'nav' in ev.dataAttr ) {
				
				var nav = Number(ev.dataAttr.nav);
				
				if ( ev.eventType === 'tap' )
					this.current = this.dateAdd(this.current, this.view, nav);

				if ( ev.eventType === 'over' && ev.pointerActive ) {

					var startMove = function(timeout) {

						this.current = this.dateAdd(this.current, this.view, nav);
						this._moveInterval = setTimeout(function() {
							
							startMove(Math.max(timeout * 0.8, 250));
						}, timeout);
					}.bind(this);
					
					startMove(750);
				}

			} else {
				
				if ( this._moveInterval !== undefined ) {
					
					clearInterval(this._moveInterval);
					this._moveInterval = undefined;
				}
			}
			
			if ( 'item' in ev.dataAttr ) {
				
				var value = JSON.parse(ev.dataAttr.item);
				ev.type = value[1];
				ev.range = this.getItemRange(df.parse(value[0]*10000), ev.type); // 10000: currently, min resolution is "minute"
			}
			

			if ( 'view' in ev.dataAttr && ev.eventType === 'tap' ) {
					
				this.view = Number(ev.dataAttr.view);
				return;
			}

			if ( !ev.keyActive && ((ev.eventType === 'tap' && ev.type >= PERIOD.MONTH) || (ev.eventType === 'press' && ev.type < PERIOD.MONTH && ev.type > PERIOD.MINUTE )) ) {
					
				this.view = ev.type;
				this.current = ev.range.start;
				return;
			}
			
			this.$emit('action', ev);
		}
	}
}


</script>