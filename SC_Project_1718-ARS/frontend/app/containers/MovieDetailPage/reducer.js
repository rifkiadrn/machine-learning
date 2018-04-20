/*
 *
 * MovieDetailPage reducer
 *
 */

import { fromJS } from 'immutable';
import {
  GET_MOVIE_REQUESTED,
  GET_MOVIE_SUCCESS,
  GET_MOVIE_ERROR,
  GET_MOVIE_PREDICTION_REQUESTED,
  GET_MOVIE_PREDICTION_SUCCESS,
  GET_MOVIE_PREDICTION_ERROR,
  MOVIE_LOADING,
} from './constants';

const initialState = fromJS({
  movie: null,
  loading: "",
  loadingPredict: "",
  prediction: null,
});

function movieDetailPageReducer(state = initialState, action) {
  switch (action.type) {
    case GET_MOVIE_REQUESTED:
      return state.merge({
        loading: MOVIE_LOADING,
        movie: null,
      });
    case GET_MOVIE_SUCCESS:
      return state.merge({
        loading: "",
        movie: action.payload
      });
    case GET_MOVIE_ERROR:
      return state.merge({
        loading: "",
        movie: null,
      });
    case GET_MOVIE_PREDICTION_REQUESTED:
      return state.merge({
        loadingPredict: MOVIE_LOADING,
        prediction: null,
      });
    case GET_MOVIE_PREDICTION_SUCCESS:
      return state.merge({
        loadingPredict: "",
        prediction: action.payload
      });
    case GET_MOVIE_PREDICTION_ERROR:
      return state.merge({
        loadingPredict: "",
        prediction: null,
      });
    default:
      return state;
  }
}

export default movieDetailPageReducer;
