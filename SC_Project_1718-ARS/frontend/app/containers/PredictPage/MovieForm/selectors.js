import { createSelector } from 'reselect';

/**
 * Direct selector to the movieForm state domain
 */
const selectMovieFormDomain = (state) => state.get('movieForm');

/**
 * Other specific selectors
 */


/**
 * Default selector used by MovieForm
 */

const makeSelectMovieForm = () => createSelector(
  selectMovieFormDomain,
  (substate) => substate.toJS()
);

export default makeSelectMovieForm;
export {
  selectMovieFormDomain,
};
