/*
 *
 * MovieDetailPage actions
 *
 */

import {
  GET_MOVIE_REQUESTED,
  GET_MOVIE_SUCCESS,
  GET_MOVIE_ERROR,
  GET_MOVIE_PREDICTION_REQUESTED,
  GET_MOVIE_PREDICTION_SUCCESS,
  GET_MOVIE_PREDICTION_ERROR,
} from './constants';

export function getMovieDetails(id) {
  return {
    type: GET_MOVIE_REQUESTED,
    payload: {
      id
    }
  }
}

export function receiveMovieDetailsSuccess(payload) {
  return {
    type: GET_MOVIE_SUCCESS,
    payload,
  }
}

export function receiveMovieDetailsError(error) {
  return {
    type: GET_MOVIE_ERROR,
    payload: {error},
  }
}


export function getPredictMovie() {
  return {
    type: GET_MOVIE_PREDICTION_REQUESTED,
  }
}


export function receivePredictMovieSuccess(payload) {
  return {
    type: GET_MOVIE_PREDICTION_SUCCESS,
    payload,
  }
}

export function receivePredictMovieError(error) {
  return {
    type: GET_MOVIE_PREDICTION_ERROR,
    payload: {error},
  }
}
