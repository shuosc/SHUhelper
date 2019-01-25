<template>
    <v-card>
        <v-list-tile
                :key="class_.courseId+class_.beginSector"
                @click=""
                avatar
                v-for="class_ in classes">
            <v-list-tile-avatar>
                <v-icon :style="{background: getCourse(class_.courseId).value.color}">class</v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
                <v-list-tile-title>{{ getCourse(class_.courseId).value.name }}</v-list-tile-title>
                <v-list-tile-sub-title>
                    <v-container class="class-info" grid-list-xs text-xs-left>
                        <v-layout row wrap>
                            <v-flex xs2>{{ class_.beginSector }}-{{class_.endSector }}
                            </v-flex>
                            <v-flex xs10>
                                {{getCourse(class_.courseId).value.place}}
                            </v-flex>
                        </v-layout>
                    </v-container>
                </v-list-tile-sub-title>
            </v-list-tile-content>
        </v-list-tile>
    </v-card>
</template>

<script lang="ts">
    import Component, {namespace} from 'nuxt-class-component';
    import {Prop, Vue} from 'vue-property-decorator';
    import {Class} from "../../../shared/model/course/class/class";
    import {Course} from "../../../shared/model/course/course";
    import * as courseModule from '~/store/modules/course';
    import * as semesterModule from '~/store/modules/semester';
    import {Maybe} from "../../../shared/tools/functools/maybe";
    import {Semester} from "../../../shared/model/semester/semester";
    import * as _ from "lodash";

    const CourseNamespace = namespace(courseModule.name);
    const SemesterNamespace = namespace(semesterModule.name);
    @Component
    export default class CourseList extends Vue {
        @Prop({default: null})
        date!: Date;

        @CourseNamespace.Getter getClassesForDate!: (semester: Semester, date: Date) => Array<Class>;
        @CourseNamespace.Getter getCourse!: (id: string) => Maybe<Course>;
        @SemesterNamespace.Getter getSemesterForDate!: (date: Date) => Maybe<Semester>;

        get classes(): Array<Class> {
            if (this.date === null) {
                return [];
            }
            const semester: Maybe<Semester> = this.getSemesterForDate(this.date);
            const getClassesForToday: (semester: Semester) => Array<Class> = _.partial(this.getClassesForDate, _, this.date);
            const classesForDate: Maybe<Array<Class>> = semester.map(getClassesForToday);
            const classTimeCompare = (classA: Class, classB: Class) => classA.beginSector - classB.beginSector;
            const classes = classesForDate.map(classes => classes.sort(classTimeCompare));
            if (classes.value === null) {
                return [];
            }
            return classes.value;
        }
    }
</script>

<style scoped>
    .class-info {
        padding: 0;
    }
</style>