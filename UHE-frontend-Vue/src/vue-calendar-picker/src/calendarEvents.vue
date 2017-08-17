<template>
	<calendar :locale="locale"
	          :compact="compact"
	          :view-count="viewCount"
	          :initial-view="initialView"
	          :initial-current="initialCurrent"
	          :item-class="thisItemClass"
	          :events="events"
	          :selection="selection"
	          @action="action">
		<template scope="scope">
			<div class="events">
				<div class="eventRange"
				     v-for="(event, index) in sortedEvents"
				     v-if="!df.isEqual(event.start, event.end) && df.areRangesOverlapping(event.start, event.end, scope.itemRange.start, scope.itemRange.end)"
				     :style="[ { backgroundColor: event.color }, eventStyle(event, scope.itemRange, scope.layout) ]"
				     :data-event="index"></div>
				<div class="eventAt"
				     v-for="(event, index) in sortedEvents"
				     v-if="df.isEqual(event.start, event.end) && df.isWithinRange(event.start, scope.itemRange.start, scope.itemRange.end) && !df.isEqual(event.end, scope.itemRange.end)"
				     :style="{ backgroundColor: event.color }"
				     :data-event="index"></div>
			</div>
		</template>
	</calendar>
</template>

<style>
/* events */

.calendar .view .events {
	display: inline-block;
}

.calendar .view .eventRange {
	display: inline-block;
}

.calendar .view .eventAt {
	display: inline-block;
	margin: 1px;
	width: 4px;
	height: 4px;
}



/* horizontal layout */

.calendar .horizontalLayout .events {
	width: 100%;
	vertical-align: top;
	text-align: center;
}

.calendar .horizontalLayout .eventRange {
	position: relative;
	display: block;
	margin: 2px 0;
	width: 100%;
	min-width: 1px;
	height: 2px;
}

.calendar .horizontalLayout .eventAt {
	vertical-align: top;
}



/* vertical layout */

.calendar .verticalLayout .events {
	height: 100%;
}

.calendar .verticalLayout .eventRange {
	position: relative;
	margin: 0 2px;
	width: 2px;
	height: 100%;
	min-height: 1px;
	vertical-align: top;
}

.calendar .verticalLayout .eventAt {
	vertical-align: middle;
}



/* selection */

.calendar .selection2 {
	background-color: #cde;
}

.calendar .selection1 {
	background-color: #def;
}


.calendar .horizontalLayout .selectionStart {
	border-top-left-radius: 0.5em;
	border-bottom-left-radius: 0.5em;
}

.calendar .horizontalLayout .selectionEnd {
	border-top-right-radius: 0.5em;
	border-bottom-right-radius: 0.5em;
}

.calendar .verticalLayout .selectionStart {
	border-top-left-radius: 0.5em;
	border-top-right-radius: 0.5em;
}

.calendar .verticalLayout .selectionEnd {
	border-bottom-left-radius: 0.5em;
	border-bottom-right-radius: 0.5em;
}
</style>

<script>
"use strict";

var df = require('date-fns'); // https://date-fns.org

var calendar = require('./calendar.vue');

module.exports = {
	components: {
		calendar: calendar,
	},
	props: {
		locale: {},
		compact: {},
		viewCount: {},
		initialView: {},
		initialCurrent: {},
		selection: {
			type: Object,
			default: function () {
				return {}
			}
		},
		itemClass: {
			type: Function,
			default: function () { },
		},
		events: {
			type: Array,
			default: []
		},
	},
	computed: {

		sortedEvents: function () {

			return this.events.slice().sort(function (b, a) {

				return (a.end - a.start) - (b.end - b.start);
			})
		}
	},
	methods: {

		thisItemClass: function (range, type) {

			var classlist = [this.itemClass(range, type)];

			var start = this.selection.start;
			var end = this.selection.end;
			var start = df.min(start, end);
			var end = df.max(start, end);


			if (!(df.isAfter(start, range.start) || df.isBefore(end, range.end))) {

				classlist.push('selection2');

				if (df.isEqual(start, range.start))
					classlist.push('selectionStart');

				if (df.isEqual(end, range.end))
					classlist.push('selectionEnd');

			} else
				if (df.areRangesOverlapping(start, end, range.start, range.end)) {

					classlist.push('selection1');

					if (df.isWithinRange(start, range.start, range.end))
						classlist.push('selectionStart');

					if (df.isWithinRange(end, range.start, range.end))
						classlist.push('selectionEnd');
				}



			return classlist;
		},

		eventStyle: function (event, itemRange, layout) {

			if (event.start < itemRange.start && event.end > itemRange.end)
				return null; // use default style aka 100%

			var itemLength = itemRange.end - itemRange.start;

			var start = df.max(event.start, itemRange.start);
			var end = df.min(event.end, itemRange.end);

			var offset = (start - itemRange.start) / itemLength;
			var size = (end - itemRange.start) / itemLength - offset;

			var uiOffset = offset * 100 + '%';
			var uiSize = size > 0.1 ? size * 100 + '%' : '2px';

			if (layout === 'horizontal')
				return { left: uiOffset, width: uiSize };
			else
				return { top: uiOffset, height: uiSize };
		},

		action: function (ev) {

			if ('event' in ev.dataAttr)
				ev.calendarEvent = this.events[ev.dataAttr.event];
			this.$emit('action', ev);
		}
	},
	created: function () {

		this.df = df;
	}
}
</script>