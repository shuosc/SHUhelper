var isEq = require('./isEq.js');

var df = require('date-fns'); // https://date-fns.org

var PERIOD = require('./period.js');

var pointerEventDirective = require('./pointerEventDirective.js');


function data(el, binding) {

	if ( isEq(binding.value, binding.oldValue) )
		return;
	// use setAttribute instead of dataset because IE[9, 10] does not reflect dataset into dom attributes.
	el.setAttribute('data-'+binding.arg, JSON.stringify(binding.value));
}


module.exports = {
	directives: {
		data: data,
		onpointer: pointerEventDirective(),
	},
	
	props: {
		locale: {
			type: String,
			default: (navigator.language || navigator.userLanguage).substr(0,2).toUpperCase(),
			validator: function(value) {
				
				return value === value.toUpperCase();
			}
		},
		compact: {
			type: Boolean,
			default: false,
		},
		
		itemClass: {
			type: Function,
			default: function() {},
		},

	},
	computed: {
		dateFnsLocale: function() {
			
			return require('date-fns/locale/'+this.locale.toLowerCase()+'/index.js');
		},

		firstDayOfTheWeek: function() {
					
			if (' GB AG AR AS AU BR BS BT BW BZ CA CN CO DM DO ET GT GU HK HN ID IE IL IN JM JP KE KH KR LA MH MM MO MT MX MZ NI NP NZ PA PE PH PK PR PY SA SG SV TH TN TT TW UM US VE VI WS YE ZA ZW '.indexOf(' '+this.locale+' ') !== -1 )
				return 0; // sun
			if (' AE AF BH DJ DZ EG IQ IR JO KW LY MA OM QA SD SY '.indexOf(' '+this.locale+' ') !== -1 )
				return 6; // sat
			if (' BD MV '.indexOf(' '+this.locale+' ') !== -1 )
				return 5; // fri
			return 1; // mon
		},

		dfOptions: function() {
			return { weekStartsOn: this.firstDayOfTheWeek };
		},
		
	},
	methods: {
		format: function(date, format) {

			return df.format(date, format, { locale: this.dateFnsLocale });
		},
		
		dateAdd: function(date, type, count) {
			
			switch ( type ) {
				case PERIOD.MINUTE: return df.addMinutes(date, count);
				case PERIOD.HOUR: return df.addHours(date, count);
				case PERIOD.DAY: return df.addDays(date, count);
				case PERIOD.WEEK: return df.addWeeks(date, count);
				case PERIOD.MONTH: return df.addMonths(date, count);
				case PERIOD.YEAR: return df.addYears(date, count);
				case PERIOD.DECADE: return df.addYears(date, 16 * count);
			}
		},
		
		getItemRange: function(date, type) {
			
			switch ( type ) {
				case PERIOD.MINUTE: return { start: df.startOfMinute(date), end: df.startOfMinute(df.addMinutes(date, 1)) };
				case PERIOD.HOUR: return { start: df.startOfHour(date), end: df.startOfHour(df.addHours(date, 1)) };
				case PERIOD.DAY: return { start: df.startOfDay(date), end: df.startOfDay(df.addDays(date, 1)) };
				case PERIOD.WEEK: return { start: df.startOfWeek(date, this.dfOptions), end: df.startOfWeek(df.addWeeks(date, 1), this.dfOptions) };
				case PERIOD.MONTH: return { start: df.startOfMonth(date), end: df.startOfMonth(df.addMonths(date, 1)) };
				case PERIOD.YEAR: return { start: df.startOfYear(date), end: df.startOfYear(df.addYears(date, 1)) };
			}
		},
		
	},
	
	created: function() {
		
		this.df = df;
		this.PERIOD = PERIOD;
	}
	
}
