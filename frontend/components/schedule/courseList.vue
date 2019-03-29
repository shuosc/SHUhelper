<template>
    <v-card>
        <v-list-tile
                :key="class_.courseId+class_.beginSector"
                @click=""
                avatar
                v-for="class_ in allClasses">
            <v-list-tile-avatar>
                <v-icon :style="{background: course(class_.courseId).map(it => it.color).toNullable()}">class</v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
                <v-list-tile-title>{{course(class_.courseId).map(it => it.name).toNullable()}}</v-list-tile-title>
                <v-list-tile-sub-title>
                    <v-container class="class-info" grid-list-xs text-xs-left>
                        <v-layout row wrap>
                            <v-flex xs2>{{class_.beginSector}}-{{class_.endSector}}
                            </v-flex>
                            <v-flex xs10>
                                {{course(class_.courseId).map(it => it.place).toNullable()}}
                            </v-flex>
                        </v-layout>
                    </v-container>
                </v-list-tile-sub-title>
            </v-list-tile-content>
        </v-list-tile>
    </v-card>
</template>

<script lang="ts">

    import {namespace} from "vuex-class";
    import {Component, Prop, Vue} from "vue-property-decorator";
    import {Option} from "fp-ts/lib/Option";
    import {Semester} from "../../../shared/model/semester/semester";
    import {Course} from "~/store/modules/course";
    import {DateTimeInSemester} from "~/service/dateTimeInSemester.service";
    import {Class} from "../../../shared/model/course/class/class";

    const SemesterNamespace = namespace("semester");
    const CourseNamespace = namespace("course");

    @Component
    export default class CourseList extends Vue {
        @Prop({default: null})
        date!: Date;
        @SemesterNamespace.Getter semesterForDate!: (date: Date) => Option<Semester>;
        @SemesterNamespace.Action fetchSemester!: (payload: { forDate: Date }) => void;
        @CourseNamespace.Getter course!: (id: any) => Option<Course>;
        @CourseNamespace.Action fetchCourses!: () => void;
        @CourseNamespace.Getter classesForDate!: (dateInSemester: DateTimeInSemester) => Array<Class>;

        get semester() {
            return this.semesterForDate(this.date);
        }

        get currentDateInSemester(): Option<DateTimeInSemester> {
            return this.semester.map(semester => {
                return {
                    semester: semester,
                    dateTime: this.date
                }
            });
        }

        get allClasses(): Array<Class> {
            return this.currentDateInSemester
                .map(this.classesForDate)
                .getOrElse([])
                .sort((a: Class, b: Class) => a.beginSector - b.beginSector);
        }
    }
</script>

<style scoped>
    .class-info {
        padding: 0;
    }
</style>
