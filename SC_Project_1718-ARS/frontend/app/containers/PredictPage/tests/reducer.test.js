
import { fromJS } from 'immutable';
import predictPageReducer from '../reducer';

describe('predictPageReducer', () => {
  it('returns the initial state', () => {
    expect(predictPageReducer(undefined, {})).toEqual(fromJS({}));
  });
});
