export interface State {
  day: number | null,
  term: number | null,
  week: number | null,
  year: number | null,
}

export const state = (): State => ({
  day: null,
  term: null,
  week: null,
  year: null
});
