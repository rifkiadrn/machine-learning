import { createSelector } from 'reselect';

/**
 * Direct selector to the historiesPage state domain
 */
const selectHistoriesPageDomain = (state) => state.get('historiesPage');

/**
 * Other specific selectors
 */


/**
 * Default selector used by HistoriesPage
 */

const makeSelectHistoriesPage = () => createSelector(
  selectHistoriesPageDomain,
  (substate) => substate.toJS()
);

export default makeSelectHistoriesPage;
export {
  selectHistoriesPageDomain,
};
