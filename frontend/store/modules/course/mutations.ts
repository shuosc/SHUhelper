import {MutationTree} from "vuex";
import {Course, State} from "./state";
import {Types} from "./types";
import {Course as SharedCourse} from "../../../../shared/model/course/course";
import {nextBeautifulLightColor} from "~/tools/color";

export const mutations: MutationTree<State> = {
    [Types.SET_COURSES]: (state: State, payload: any) => {
        state.courses = payload.data.map((it: SharedCourse): Course => {
            return {
                ...it,
                color: nextBeautifulLightColor()
            }
        });
    }
};