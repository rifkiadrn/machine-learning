/**
 *
 * Asynchronously loads the component for PredictPage
 *
 */

import React from 'react';
import Loadable from 'react-loadable';

import LoadingIndicator from '../../components/LoadingIndicator/index';

export default Loadable({
  loader: () => import('./index'),
  loading: LoadingIndicator,
  delay: 300,
});
