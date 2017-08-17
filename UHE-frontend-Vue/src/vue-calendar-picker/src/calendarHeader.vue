<template>
	<div class="header">
		<span v-if="$parent.view <= $parent.PERIOD.YEAR" :data-view="$parent.PERIOD.DECADE" v-text="$parent.df.getYear($parent.current)"></span>
		<span v-if="$parent.view <= $parent.PERIOD.MONTH" :data-view="$parent.PERIOD.YEAR" v-text="$parent.format($parent.current, $parent.compact ? 'MMM' : 'MMMM')"></span>
		<span v-if="$parent.view === $parent.PERIOD.WEEK" :data-view="$parent.PERIOD.MONTH" v-text="'W'+$parent.df.getISOWeek($parent.current)"></span>
		<span v-if="$parent.view <= $parent.PERIOD.DAY" :data-view="$parent.PERIOD.MONTH" v-text="$parent.df.getDate($parent.current)"></span>
		<span v-if="$parent.view <= $parent.PERIOD.HOUR" :data-view="$parent.PERIOD.DAY">{{$parent.format($parent.current, 'HH')}}<sup>h</sup></span>
	</div>
</template>
