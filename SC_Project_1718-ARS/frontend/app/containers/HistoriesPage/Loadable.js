/**
 *
 * Asynchronously loads the component for HistoriesPage
 *
 */

import Loadable from 'react-loadable';

export default Loadable({
  loader: () => import('./index'),
  loading: () => null,
});
