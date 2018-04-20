/**
 *
 * MovieList
 *
 */

import React from 'react';
import MovieItem from 'containers/PredictPage/MovieItem';
import LoadingIndicator from 'components/LoadingIndicator';
import styled from 'styled-components';
import {NOT_FOUND_ERROR, MOVIE_LIST_LOADING} from '../constants';


class MovieList extends React.Component { // eslint-disable-line react/prefer-stateless-function
  render() {
    const { movies, error, loading } = this.props;
    const Wrapper = styled.div`
      background-color: #EDF2F4;
      
      & .container {
        padding-top: 1em;
        padding-bottom: 1em;
      }
    `;

    const EmptyHeader = styled.h2`
      opacity: .4;
    `;
    const Blank = () => {
      return (
        <EmptyHeader className="text-center">{error === NOT_FOUND_ERROR ? "Oops... Film Tidak Ditemukan :(" : "Silahkan Ketik Judul Film"}</EmptyHeader>
      )
    };

    return (
      <Wrapper className="container-fluid">
        <div className="container">
          {loading === MOVIE_LIST_LOADING ? <LoadingIndicator /> : (movies.length < 1 ? <Blank /> : movies.map((movie) => <MovieItem data={movie} key={movie.imdbID}/>))}
        </div>
      </Wrapper>
    );
  }
}

export default MovieList;
