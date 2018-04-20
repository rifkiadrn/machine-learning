/*
 *
 * PredictPage actions
 *
 */

import {
  FETCH_MOVISLIST_REQUESTED, FETCH_MOVISLIST_SUCCESS, FETCH_MOVISLIST_FAILED, CHANGE_SEARCHBOX
} from './constants';

export function fetchMovies(title) {
  return {
    type: FETCH_MOVISLIST_REQUESTED,
    payload: {
      title
    }
  }
}

export function receiveMoviesSuccess(payload) {
  return {
    type: FETCH_MOVISLIST_SUCCESS,
    payload,
  }
}

export function receiveMoviesFailed(error) {
  return {
    type: FETCH_MOVISLIST_FAILED,
    payload: {error},
  }
}

export function changeSearchBox(text, dispatch = () => null) {
  if (text) {
    dispatch(fetchMovies(text));
  } else {
    dispatch(receiveMoviesFailed(""));
  }
  return {
    type: CHANGE_SEARCHBOX,
    payload: {text},
  }
}
