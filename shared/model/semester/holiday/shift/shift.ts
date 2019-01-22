/**
 * 调休
 * 将 from 这一天的课调到 to 这一天上，from 这一天休息，to 这一天上 from 这一天的课
 */
export interface Shift {
    readonly from: Date;
    readonly to: Date;
}
