/**
 *
 * PredictPage
 *
 */

import React from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {Helmet} from 'react-helmet';
import {createStructuredSelector} from 'reselect';
import {compose} from 'redux';

import injectSaga from 'utils/injectSaga';
import injectReducer from 'utils/injectReducer';
import {fetchMovies, changeSearchBox} from './actions';
import makeSelectPredictPage, {makeSelectMovies, makeSelectText, makeSelectError, makeSelectLoading} from './selectors';
import reducer from './reducer';
import saga from './saga';

import Hero from 'components/Hero/Loadable';
import SearchBar from 'components/SearchBar';
import MovieList from './MovieList';

export class PredictPage extends React.Component { // eslint-disable-line react/prefer-stateless-function

  render() {
    const { text, onSearchClick, onChangeSearchBox, error, movies, loading} = this.props;
    const footer = (
      <div className="row justify-content-center">
        <div className="col-md-8 col-lg-6">
          <SearchBar text={text} onSearchClick={onSearchClick} onChangeSearchText={onChangeSearchBox}/>
        </div>
      </div>
    );
    return (
      <div>
        <Helmet>
          <title>PredictPage</title>
          <meta name="description" content="Description of PredictPage"/>
        </Helmet>
        <article>
          <section id="hero">
            <Hero footer={footer}/>
          </section>
          <section id="movie-list">
            <MovieList loading={loading} error={error} movies={movies}/>
          </section>
        </article>
      </div>
    );
  }
}

PredictPage.propTypes = {
  dispatch: PropTypes.func.isRequired,
};

const mapStateToProps = createStructuredSelector({
  predictPage: makeSelectPredictPage(),
  movies: makeSelectMovies(),
  text: makeSelectText(),
  error: makeSelectError(),
  loading: makeSelectLoading(),
});

function mapDispatchToProps(dispatch) {
  return {
    dispatch,
    onFetchMovies: (title) => dispatch(fetchMovies(title)),
    onChangeSearchBox: (text) => dispatch(changeSearchBox(text,dispatch)),
  };
}

const withConnect = connect(mapStateToProps, mapDispatchToProps);

const withReducer = injectReducer({key: 'predictPage', reducer});
const withSaga = injectSaga({key: 'predictPage', saga});

export default compose(
  withReducer,
  withSaga,
  withConnect,
)(PredictPage);
