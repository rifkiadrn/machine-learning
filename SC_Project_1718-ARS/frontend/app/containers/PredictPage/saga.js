import { takeLatest, call, put } from 'redux-saga/effects';
import request from 'utils/request';
import { receiveMoviesSuccess, receiveMoviesFailed } from './actions';
import {
  FETCH_MOVISLIST_REQUESTED,
  NOT_FOUND_ERROR,
} from './constants';

// Individual exports for testing
export function* getMovies(action) {
  const apiUrl = `http://localhost:8000/api/v1/search?m_name=${action.payload.title}/`;
  try {
    const response = yield call(request, apiUrl);
    yield put(receiveMoviesSuccess(response.data.movies));
  } catch (e) {
    yield put(receiveMoviesFailed(NOT_FOUND_ERROR));
  }
}

export default function* defaultSaga() {
  yield [
    takeLatest(FETCH_MOVISLIST_REQUESTED, getMovies)
  ];

}
;
