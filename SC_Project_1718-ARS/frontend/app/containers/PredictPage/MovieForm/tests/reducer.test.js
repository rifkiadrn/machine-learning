
import { fromJS } from 'immutable';
import movieFormReducer from '../reducer';

describe('movieFormReducer', () => {
  it('returns the initial state', () => {
    expect(movieFormReducer(undefined, {})).toEqual(fromJS({}));
  });
});
