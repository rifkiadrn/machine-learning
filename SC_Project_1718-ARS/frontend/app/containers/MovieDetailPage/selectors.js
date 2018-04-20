import { createSelector } from 'reselect';

/**
 * Direct selector to the movieDetailPage state domain
 */
const selectMovieDetailPageDomain = (state) => state.get('movieDetailPage');

/**
 * Other specific selectors
 */


/**
 * Default selector used by MovieDetailPage
 */

export const makeSelectMovieDetailPage = () => createSelector(
  selectMovieDetailPageDomain,
  (substate) => substate.toJS()
);

export const makeSelectMovieDetails = () => createSelector(
  makeSelectMovieDetailPage(),
  (substate) => substate.movie
);

export default makeSelectMovieDetailPage;
