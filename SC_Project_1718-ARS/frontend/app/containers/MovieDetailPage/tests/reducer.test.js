
import { fromJS } from 'immutable';
import movieDetailPageReducer from '../reducer';

describe('movieDetailPageReducer', () => {
  it('returns the initial state', () => {
    expect(movieDetailPageReducer(undefined, {})).toEqual(fromJS({}));
  });
});
