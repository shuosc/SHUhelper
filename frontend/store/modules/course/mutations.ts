import {MutationTree} from "vuex";
import {Course, State} from "./state";
import {Types} from "./types";
import {Course as SharedCourse} from "../../../../shared/model/course/course";
import {randomSelect} from "../../../../shared/tools/randomSelect";
import {BEAUTIFUL_LIGHT_COLOR} from "~/tools/color";

export const mutations: MutationTree<State> = {
    [Types.SET_COURSES]: (state: State, payload: any) => {
        state.courses = payload.data.map((it: SharedCourse): Course => {
            return {
                ...it,
                color: randomSelect(BEAUTIFUL_LIGHT_COLOR)
            }
        });
    }
};