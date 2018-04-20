import { createSelector } from 'reselect';

/**
 * Direct selector to the predictPage state domain
 */
const selectPredictPageDomain = (state) => state.get('predictPage');

/**
 * Other specific selectors
 */


/**
 * Default selector used by PredictPage
 */

export const makeSelectPredictPage = () => createSelector(
  selectPredictPageDomain,
  (substate) => substate.toJS()
);

export const makeSelectMovies = () => createSelector(
  makeSelectPredictPage(),
  (substate) => substate.movies
);

export const makeSelectText = () => createSelector(
  makeSelectPredictPage(),
  (substate) => substate.text
);
export const makeSelectError = () => createSelector(
  makeSelectPredictPage(),
  (substate) => substate.error
);
export const makeSelectLoading = () => createSelector(
  makeSelectPredictPage(),
  (substate) => substate.loading
);

export default makeSelectPredictPage;
