/*
 *
 * HistoriesPage reducer
 *
 */

import { fromJS } from 'immutable';
import {
  GET_HISTORIES_REQUESTED,
  GET_HISTORIES_SUCCESS,
  GET_HISTORIES_ERROR,
} from './constants';

const initialState = fromJS({});

function historiesPageReducer(state = initialState, action) {
  switch (action.type) {
    case GET_HISTORIES_REQUESTED:
      return state.merge({
        loading: 'Loading histories...',
        histories: null,
      });
    case GET_HISTORIES_SUCCESS:
      return state.merge({
        loading: '',
        histories: action.payload,
      });
    case GET_HISTORIES_ERROR:
      return state.merge({
        loading: '',
        histories: null,
      });
    default:
      return state;
  }
}

export default historiesPageReducer;
