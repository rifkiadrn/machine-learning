import { takeLatest, call, put } from 'redux-saga/effects';
import { GET_HISTORIES_REQUESTED } from './constants';
import request from 'utils/request';
import { receiveHistoriesError, receiveHistoriesSuccess } from './actions';

export function* getHistories() {
  const requestURL = `http://localhost:8000/api/v1/history/`;

  try {
    const response = yield call(request, requestURL);
    yield put(receiveHistoriesSuccess(response));
  } catch (err) {
    yield put(receiveHistoriesError(err));
  }
}
// Individual exports for testing
export default function* defaultSaga() {
  yield [takeLatest(GET_HISTORIES_REQUESTED, getHistories)];
}
