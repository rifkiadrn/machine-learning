/**
 *
 * MovieDetailPage
 *
 */

import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { createStructuredSelector } from 'reselect';
import { compose } from 'redux';

import injectSaga from 'utils/injectSaga';
import injectReducer from 'utils/injectReducer';
import makeSelectMovieDetailPage, {
  makeSelectMovieDetails,
} from './selectors';
import reducer from './reducer';
import saga from './saga';
import { getMovieDetails, getPredictMovie } from './actions';

import MovieDetail from './MovieDetail';

export class MovieDetailPage extends React.Component {
  // eslint-disable-line react/prefer-stateless-function
  componentDidMount() {
    const { match, onGetMovieDetails } = this.props;
    onGetMovieDetails(match.params.movieId);
  }

  render() {
    return <MovieDetail {...this.props} />;
  }
}

MovieDetailPage.propTypes = {
  dispatch: PropTypes.func.isRequired,
};

const mapStateToProps = createStructuredSelector({
  moviedetailpage: makeSelectMovieDetailPage(),
  movie: makeSelectMovieDetails(),
});

function mapDispatchToProps(dispatch) {
  return {
    dispatch,
    onGetMovieDetails: id => dispatch(getMovieDetails(id)),
    onPredictMovie: id => dispatch(getPredictMovie(id)),
  };
}

const withConnect = connect(mapStateToProps, mapDispatchToProps);

const withReducer = injectReducer({ key: 'movieDetailPage', reducer });
const withSaga = injectSaga({ key: 'movieDetailPage', saga });

export default compose(withReducer, withSaga, withConnect)(MovieDetailPage);
