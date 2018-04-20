import { takeLatest, call, put, select } from 'redux-saga/effects';
import {
  GET_MOVIE_REQUESTED,
  GET_MOVIE_PREDICTION_REQUESTED,
} from './constants';
import request from 'utils/request';
import {
  receiveMovieDetailsError,
  receiveMovieDetailsSuccess,
  receivePredictMovieSuccess,
  receivePredictMovieError,
} from './actions';
import { makeSelectMovieDetails } from './selectors';

export function* getMovieDetails(action) {
  const requestURL = `http://localhost:8000/api/v1/movie_details/${
    action.payload.id
  }/`;
  // const requestURL = `https://private-e05a3-arest.apiary-mock.com/movie/${action.payload.id}`;

  try {
    const response = yield call(request, requestURL);
    yield put(receiveMovieDetailsSuccess(response.data));
  } catch (err) {
    yield put(receiveMovieDetailsError(err));
  }
}
export function* postPredictMovie(action) {
  const requestURL = `http://localhost:8000/api/v1/predict/`;
  const movie = yield select(makeSelectMovieDetails());

  try {
    const response = yield call(request, requestURL, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(movie),
    });
    yield put(receivePredictMovieSuccess(response.data));
  } catch (err) {
    yield put(receivePredictMovieError(err));
  }
}

// Individual exports for testing
export default function* defaultSaga() {
  yield [
    takeLatest(GET_MOVIE_REQUESTED, getMovieDetails),
    takeLatest(GET_MOVIE_PREDICTION_REQUESTED, postPredictMovie),
  ];
}
