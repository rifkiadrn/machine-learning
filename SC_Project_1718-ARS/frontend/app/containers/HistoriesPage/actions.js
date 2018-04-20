/*
 *
 * HistoriesPage actions
 *
 */

import {
  GET_HISTORIES_REQUESTED,
  GET_HISTORIES_SUCCESS,
  GET_HISTORIES_ERROR,
} from './constants';

export function getHistories() {
  return {
    type: GET_HISTORIES_REQUESTED,
  };
}

export function receiveHistoriesSuccess(payload) {
  return {
    type: GET_HISTORIES_SUCCESS,
    payload,
  };
}

export function receiveHistoriesError(error) {
  return {
    type: GET_HISTORIES_ERROR,
    payload: { error },
  };
}
