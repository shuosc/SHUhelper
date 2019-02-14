<template>
    <v-card class="pa-0">
        <v-card-title class="pa-0" primary-title>
            <v-container class="pa-3">
                <v-layout align-center row wrap>
                    <v-flex fill-height xs1>
                        <v-layout align-center justify-center>
                            <v-avatar :size="avatarSize() ">
                                <v-icon class="white--text red lighten-1" medium>directions_bus</v-icon>
                            </v-avatar>
                        </v-layout>
                    </v-flex>
                    <v-divider class="mx-3" inset vertical></v-divider>
                    <v-flex xs9>
                        <v-layout column>
                            <v-flex xs5>
                                距下一趟校车还有{{nextBusTime}}分钟
                            </v-flex>
                            <v-flex xs6>
                            <v-radio-group row v-model="day">
                                <v-radio label="工作日" value="工作日" color="primary"></v-radio>
                                <v-radio label="节假日" value="节假日" color="primary"></v-radio>
                            </v-radio-group>
                            </v-flex>
                        </v-layout>
                        <v-layout row wrap>
                            <v-flex xs7>
                                <v-select label="起始" :items="allStations" v-model="startStation"> 
                                </v-select>
                            </v-flex>
                            <v-flex xs7>
                                <v-select label="终点" :items="allStations" v-model="endStation">
                                </v-select>
                            </v-flex>
                        </v-layout>
                        <v-layout row>
                            <v-flex xs12>
                                <v-expansion-panel dark>
                                    <v-expansion-panel-content >
                                        <div slot="header" >查询所有时刻</div>
                                        <v-list>
                                            <v-list-tile v-for="item in showAllBusSchedule" :key="showAllBusSchedule.indexOf(item)">
                                                <v-list-tile-action>{{showAllBusSchedule.indexOf(item)+1}}</v-list-tile-action>
                                                <v-list-tile-content>{{item}}</v-list-tile-content>
                                            </v-list-tile>
                                        </v-list>
                                    </v-expansion-panel-content>
                                </v-expansion-panel>
                            </v-flex>
                        </v-layout>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-card-title>
    </v-card>
</template>

<script lang="ts">
import {avatarSize} from "~/tools/avatarSize";
import schoolBusSchedule from "~/store/modules/busSchedule/schoolBusSchedule.json";
import Component from "nuxt-class-component";
import {Watch, Vue} from 'vue-property-decorator';

@Component({
    methods:{
        avatarSize
    }
})

export default class busTimeInfo extends Vue{
    now = new Date();
    day:string = "工作日";
    nextBusTime:number = Infinity;
    startStation:string ="校本部";
    endStation:string = "延长校区北门";
    oldStartStation:string = "校本部";
    oldEndStation:string = "延长校区北门";
    showAllBusSchedule:Array<string> = (<any>schoolBusSchedule)["显示内容"][this.day][this.startStation][this.endStation]
    allBusSchedule:Array<string> = (<any>schoolBusSchedule)[this.day][this.startStation][this.endStation]
    @Watch('selectedStation',{immediate:true,deep:true})
    onSelectedStaionsChanged(){
        //判断起始和终点站是否相同
        if(this.startStation === this.endStation) {
            this.startStation =this.oldEndStation;
            this.endStation =this.oldStartStation;
        }
        this.oldStartStation =this.startStation;
        this.oldEndStation = this.endStation;
        this.allBusSchedule = (<any>schoolBusSchedule)[this.day][this.startStation][this.endStation];
        this.showAllBusSchedule = (<any>schoolBusSchedule)["显示内容"][this.day][this.startStation][this.endStation];
    }

    @Watch('nextBusTimeChanged',{immediate:true,deep:true})
    onNextBusTimeChangedChanged(){
        this.nextBusTime=Infinity;
        this.allBusSchedule.forEach(element => {
            let hours:string;
            let minutes:string;
            [hours,minutes]=element.split(":");
            let totalMinutes:number = parseInt(hours)*60+parseInt(minutes);
            let nowMinutes:number = this.now.getHours()*60+this.now.getMinutes();
            if(totalMinutes - nowMinutes < this.nextBusTime && totalMinutes - nowMinutes>=0) {
                this.nextBusTime = totalMinutes - nowMinutes;
            }
        });
    }


    mounted() {
        setInterval(() => {
            this.now = new Date();
        }, 1000);
    }

    get caculateNowTime() {
        let thisTime = this.now;
        let thisHour:string = thisTime.getHours()<10 ? "0".concat(thisTime.getHours().toString()) : "".concat(thisTime.getHours().toString());
        let thisMinutes:string = thisTime.getMinutes().toString();
        return thisHour.concat(":").concat(thisMinutes)
    }

    get allStations(): Array<string> {
        const stations = ["校本部", "延长校区北门", "嘉定校区南门"];
        return stations;
    }
    get selectedStation():Array<string> {
        return [this.startStation,this.endStation,this.day]
    }
    get nextBusTimeChanged():Array<any>{
        return [this.startStation,this.endStation,this.day,this.now]
    }

}
</script>

<style>

</style>

