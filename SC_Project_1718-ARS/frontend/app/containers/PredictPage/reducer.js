/*
 *
 * PredictPage reducer
 *
 */

import { fromJS } from 'immutable';
import {
  FETCH_MOVISLIST_REQUESTED,
  FETCH_MOVISLIST_SUCCESS,
  FETCH_MOVISLIST_FAILED,
  CHANGE_SEARCHBOX,
  MOVIE_LIST_LOADING,
} from './constants';

const initialState = fromJS({
  movies: [],
  text: "",
  error: "",
  loading: "",
});

function predictPageReducer(state = initialState, action) {
  switch (action.type) {
    case FETCH_MOVISLIST_REQUESTED:
      return state.merge({
        movies: [],
        error: "",
        loading: MOVIE_LIST_LOADING,
      });
    case FETCH_MOVISLIST_SUCCESS:
      return state.merge({
        movies: action.payload,
        error: "",
        loading: "",
      });
    case FETCH_MOVISLIST_FAILED:
      return state.merge({
        movies: [],
        error: action.payload.error,
        loading: "",
      });
    case CHANGE_SEARCHBOX:
      return state.set('text', action.payload.text);
    default:
      return state;
  }
}

export default predictPageReducer;
