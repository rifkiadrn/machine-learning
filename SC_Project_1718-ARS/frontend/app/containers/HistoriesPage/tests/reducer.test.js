
import { fromJS } from 'immutable';
import historiesPageReducer from '../reducer';

describe('historiesPageReducer', () => {
  it('returns the initial state', () => {
    expect(historiesPageReducer(undefined, {})).toEqual(fromJS({}));
  });
});
