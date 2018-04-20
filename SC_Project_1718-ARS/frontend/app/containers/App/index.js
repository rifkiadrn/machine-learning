/**
 *
 * App.js
 *
 * This component is the skeleton around the actual pages, and should only
 * contain code that should be seen on all pages. (e.g. navigation bar)
 *
 * NOTE: while this component should technically be a stateless functional
 * component (SFC), hot reloading does not currently support SFCs. If hot
 * reloading is not a necessity for you then you can refactor it and remove
 * the linting exception.
 */

import React from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';

import Layout from '../../components/Layout';
import HomePage from '../HomePage/Loadable';
import NotFoundPage from '../NotFoundPage/Loadable';
import PredictPage from '../PredictPage/Loadable';
import HistoriesPage from '../HistoriesPage/Loadable';
import MovieDetailPage from '../MovieDetailPage';

export default function App() {
  return (
    <Layout>
      <Switch>
        <Route
          exact
          path="/"
          render={() => (
            <Redirect to="/features" />
        )}
        />
        <Route exact path="/features" component={HomePage} />
        <Route exact path="/predict" component={PredictPage} />
        <Route exact path="/history" component={HistoriesPage} />
        <Route exact path="/movie/:movieId" component={MovieDetailPage} />
        <Route component={NotFoundPage} />
      </Switch>
    </Layout>
  );
}
