/**
 *
 * HistoriesPage
 *
 */

import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Helmet } from 'react-helmet';
import { createStructuredSelector } from 'reselect';
import { compose } from 'redux';

import injectSaga from 'utils/injectSaga';
import injectReducer from 'utils/injectReducer';
import makeSelectHistoriesPage from './selectors';
import reducer from './reducer';
import saga from './saga';
import { getHistories } from './actions';

import Hero from 'components/Hero/Loadable';
import MovieList from '../PredictPage/MovieList';

export class HistoriesPage extends React.Component {
  // eslint-disable-line react/prefer-stateless-function
  componentDidMount() {
    this.props.onGetHistories();
  }

  render() {
    const { histories } = this.props.historiespage;
    console.log('histories', histories);
    return (
      <div>
        <Helmet>
          <title>HistoriesPage</title>
          <meta name="description" content="Description of HistoriesPage" />
        </Helmet>
        <Hero noBottomLine />
        {this.props.historiespage.histories ? <MovieList
          movies={this.props.historiespage.histories.map(function(item) {
            const {
              movie_thumbnail,
              movie_name,
              movie_id,
              actual_rating,
              movie_rating,
              id,
            } = item;
            return {
              Poster: movie_thumbnail,
              Title: movie_name,
              Type: '',
              Year: '',
              imdbID: movie_id + movie_rating,
              rating: {
                actual: actual_rating,
                predicted: movie_rating,
              },
            };
          })}
        /> : "kosong"}
      </div>
    );
  }
}

HistoriesPage.propTypes = {
  dispatch: PropTypes.func.isRequired,
};

const mapStateToProps = createStructuredSelector({
  historiespage: makeSelectHistoriesPage(),
});

function mapDispatchToProps(dispatch) {
  return {
    dispatch,
    onGetHistories: () => dispatch(getHistories()),
  };
}

const withConnect = connect(mapStateToProps, mapDispatchToProps);

const withReducer = injectReducer({ key: 'historiesPage', reducer });
const withSaga = injectSaga({ key: 'historiesPage', saga });

export default compose(withReducer, withSaga, withConnect)(HistoriesPage);
